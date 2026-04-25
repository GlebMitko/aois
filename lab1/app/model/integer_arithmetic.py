"""Арифметика целых чисел в битовых кодах."""

from __future__ import annotations

from fractions import Fraction

from .bits import WORD_SIZE, add_bit_lists, format_bits, shift_left, unsigned_to_bits
from .common import decimal_division_string, fraction_to_decimal_string, parse_signed_int
from .integer_codes import IntegerCodeService, MAX_MAGNITUDE


def _to_magnitude_bits(value: int) -> list[int]:
    return unsigned_to_bits(value, WORD_SIZE - 1)


def _bits_to_int(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = value * 2 + bit
    return value


class IntegerArithmeticService:
    """Целочисленная арифметика для лабораторной работы."""

    @staticmethod
    def multiply_sign_magnitude(a: int, b: int) -> dict[str, object]:
        IntegerCodeService.validate_sign_magnitude_value(a)
        IntegerCodeService.validate_sign_magnitude_value(b)
        sign = 1 if (a < 0) ^ (b < 0) else 0
        left_magnitude = _to_magnitude_bits(abs(a))
        right_magnitude = _to_magnitude_bits(abs(b))
        accumulator = [0] * (WORD_SIZE - 1)

        for offset in range(WORD_SIZE - 2, -1, -1):
            if right_magnitude[offset] == 1:
                shift = (WORD_SIZE - 2) - offset
                shifted = shift_left(left_magnitude, shift)
                accumulator, _ = add_bit_lists(accumulator, shifted)

        decimal_result = abs(a) * abs(b)
        overflow = decimal_result > MAX_MAGNITUDE
        result_bits = [sign] + accumulator
        if decimal_result == 0:
            result_bits[0] = 0
        signed_decimal = -decimal_result if sign else decimal_result
        return {
            "left_bits": [1 if a < 0 else 0] + left_magnitude,
            "right_bits": [1 if b < 0 else 0] + right_magnitude,
            "result_bits": result_bits,
            "decimal_result": signed_decimal,
            "overflow": overflow,
        }

    @staticmethod
    def divide_sign_magnitude(a: int, b: int, fractional_bits: int = 16) -> dict[str, object]:
        if b == 0:
            raise ZeroDivisionError("Деление на ноль")
        IntegerCodeService.validate_sign_magnitude_value(a)
        IntegerCodeService.validate_sign_magnitude_value(b)

        sign = 1 if (a < 0) ^ (b < 0) else 0
        dividend = abs(a)
        divisor = abs(b)

        integer_part = dividend // divisor
        remainder = dividend % divisor
        integer_bits = unsigned_to_bits(integer_part, WORD_SIZE - 1)
        fractional: list[int] = []
        current = remainder
        for _ in range(fractional_bits):
            current *= 2
            if current >= divisor:
                fractional.append(1)
                current -= divisor
            else:
                fractional.append(0)

        binary_integer = ''.join(str(bit) for bit in integer_bits).lstrip('0') or '0'
        binary_fraction = ''.join(str(bit) for bit in fractional) or '0'
        binary_result = f"{'-' if sign and (integer_part != 0 or remainder != 0) else ''}{binary_integer}.{binary_fraction}"
        decimal_fraction = Fraction(a, b)
        return {
            "left_bits": IntegerCodeService.to_sign_magnitude(a),
            "right_bits": IntegerCodeService.to_sign_magnitude(b),
            "binary_result": binary_result,
            "decimal_result": fraction_to_decimal_string(decimal_fraction, precision=5),
        }

    @staticmethod
    def build_multiplication_report(left_text: str, right_text: str) -> str:
        a = parse_signed_int(left_text)
        b = parse_signed_int(right_text)
        data = IntegerArithmeticService.multiply_sign_magnitude(a, b)
        lines = [
            f"A (прямой код): {format_bits(data['left_bits'])}",
            f"B (прямой код): {format_bits(data['right_bits'])}",
            f"Результат:       {format_bits(data['result_bits'])}",
            f"В десятичном виде: {data['decimal_result']}",
        ]
        if data['overflow']:
            lines.append("Внимание: переполнение прямого кода.")
        return "\n".join(lines)

    @staticmethod
    def build_division_report(left_text: str, right_text: str) -> str:
        a = parse_signed_int(left_text)
        b = parse_signed_int(right_text)
        data = IntegerArithmeticService.divide_sign_magnitude(a, b)
        return (
            f"A (прямой код): {format_bits(data['left_bits'])}\n"
            f"B (прямой код): {format_bits(data['right_bits'])}\n"
            f"Частное в двоичном виде: {data['binary_result']}\n"
            f"Частное в десятичном виде: {data['decimal_result']}"
        )
