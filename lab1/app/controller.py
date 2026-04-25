"""Контроллер приложения: собирает результаты из сервисов модели."""

from __future__ import annotations

from .model.bcd import BCDService
from .model.common import ValidationError, parse_signed_int
from .model.ieee754 import Float32Service
from .model.integer_arithmetic import IntegerArithmeticService
from .model.integer_codes import IntegerCodeService


class AppController:
    """Высокоуровневый контроллер."""

    def integer_codes(self, number_text: str) -> str:
        return IntegerCodeService.build_codes_report(number_text)

    def integer_add(self, left_text: str, right_text: str) -> str:
        a = parse_signed_int(left_text)
        b = parse_signed_int(right_text)
        data = IntegerCodeService.add_twos(a, b)
        lines = [
            f"A: {a}",
            f"A (доп. код): {self._fmt(data['left_bits'])}",
            f"B: {b}",
            f"B (доп. код): {self._fmt(data['right_bits'])}",
            f"Сумма: {self._fmt(data['result_bits'])}",
            f"Сумма (10): {data['decimal_result']}",
        ]
        if data['overflow']:
            lines.append("Внимание: переполнение дополнительного кода.")
        return "\n".join(lines)

    def integer_subtract(self, left_text: str, right_text: str) -> str:
        a = parse_signed_int(left_text)
        b = parse_signed_int(right_text)
        data = IntegerCodeService.subtract_twos(a, b)
        lines = [
            f"A: {a}",
            f"A (доп. код): {self._fmt(data['left_bits'])}",
            f"-B (доп. код): {self._fmt(data['negated_right_bits'])}",
            f"Разность: {self._fmt(data['result_bits'])}",
            f"Разность (10): {data['decimal_result']}",
        ]
        if data['overflow']:
            lines.append("Внимание: переполнение дополнительного кода.")
        return "\n".join(lines)

    def integer_multiply(self, left_text: str, right_text: str) -> str:
        return IntegerArithmeticService.build_multiplication_report(left_text, right_text)

    def integer_divide(self, left_text: str, right_text: str) -> str:
        return IntegerArithmeticService.build_division_report(left_text, right_text)

    def float_convert(self, number_text: str) -> str:
        return Float32Service.build_conversion_report(number_text)

    def float_operation(self, left_text: str, right_text: str, operator: str) -> str:
        return Float32Service.build_operation_report(left_text, right_text, operator)

    def bcd_add(self, left_text: str, right_text: str, variant: str = "8421") -> str:
        return BCDService.build_report(left_text, right_text, variant)

    @staticmethod
    def _fmt(bits: list[int]) -> str:
        from .model.bits import format_bits

        return format_bits(bits)
