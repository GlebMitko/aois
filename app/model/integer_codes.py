"""Представление целых чисел в прямом, обратном и дополнительном кодах."""

from __future__ import annotations

from .bits import WORD_SIZE, add_bit_lists, format_bits, invert_bits, twos_complement_negation, unsigned_to_bits
from .common import ValidationError, parse_signed_int

MAGNITUDE_BITS = WORD_SIZE - 1
MAX_MAGNITUDE = (1 << MAGNITUDE_BITS) - 1
MIN_TWOS = -(1 << MAGNITUDE_BITS)
MAX_TWOS = (1 << MAGNITUDE_BITS) - 1


class IntegerCodeService:
    """Сервис работы с целочисленными кодами."""

    @staticmethod
    def validate_sign_magnitude_value(value: int) -> None:
        if abs(value) > MAX_MAGNITUDE:
            raise OverflowError(f"Число {value} не помещается в прямой/обратный код из {WORD_SIZE} бит")

    @staticmethod
    def validate_twos_value(value: int) -> None:
        if value < MIN_TWOS or value > MAX_TWOS:
            raise OverflowError(f"Число {value} не помещается в дополнительный код из {WORD_SIZE} бит")

    @staticmethod
    def to_sign_magnitude(value: int) -> list[int]:
        IntegerCodeService.validate_sign_magnitude_value(value)
        sign = 1 if value < 0 else 0
        magnitude = unsigned_to_bits(abs(value), MAGNITUDE_BITS)
        return [sign] + magnitude

    @staticmethod
    def from_sign_magnitude(bits: list[int]) -> int:
        sign = bits[0]
        magnitude = 0
        for bit in bits[1:]:
            magnitude = magnitude * 2 + bit
        return -magnitude if sign else magnitude

    @staticmethod
    def to_ones_complement(value: int) -> list[int]:
        IntegerCodeService.validate_sign_magnitude_value(value)
        if value >= 0:
            return [0] + unsigned_to_bits(value, MAGNITUDE_BITS)
        positive = [0] + unsigned_to_bits(abs(value), MAGNITUDE_BITS)
        return invert_bits(positive)

    @staticmethod
    def from_ones_complement(bits: list[int]) -> int:
        if bits[0] == 0:
            return IntegerCodeService.from_sign_magnitude(bits)
        restored = invert_bits(bits)
        return -IntegerCodeService.from_sign_magnitude(restored)

    @staticmethod
    def to_twos_complement(value: int) -> list[int]:
        IntegerCodeService.validate_twos_value(value)
        if value >= 0:
            return unsigned_to_bits(value, WORD_SIZE)
        positive = unsigned_to_bits(abs(value), WORD_SIZE)
        return twos_complement_negation(positive)

    @staticmethod
    def from_twos_complement(bits: list[int]) -> int:
        if bits[0] == 0:
            value = 0
            for bit in bits:
                value = value * 2 + bit
            return value
        negated = twos_complement_negation(bits)
        value = 0
        for bit in negated:
            value = value * 2 + bit
        return -value

    @staticmethod
    def add_twos(a: int, b: int) -> dict[str, object]:
        IntegerCodeService.validate_twos_value(a)
        IntegerCodeService.validate_twos_value(b)
        left = IntegerCodeService.to_twos_complement(a)
        right = IntegerCodeService.to_twos_complement(b)
        result_bits, carry = add_bit_lists(left, right)
        result_value = IntegerCodeService.from_twos_complement(result_bits)
        exact_sum = a + b
        overflow = exact_sum < MIN_TWOS or exact_sum > MAX_TWOS
        return {
            "left_bits": left,
            "right_bits": right,
            "result_bits": result_bits,
            "carry": carry,
            "decimal_result": result_value,
            "overflow": overflow,
        }

    @staticmethod
    def subtract_twos(a: int, b: int) -> dict[str, object]:
        IntegerCodeService.validate_twos_value(a)
        IntegerCodeService.validate_twos_value(b)
        left = IntegerCodeService.to_twos_complement(a)
        right = IntegerCodeService.to_twos_complement(b)
        negated_b = twos_complement_negation(right)
        result_bits, carry = add_bit_lists(left, negated_b)
        result_value = IntegerCodeService.from_twos_complement(result_bits)
        exact_difference = a - b
        overflow = exact_difference < MIN_TWOS or exact_difference > MAX_TWOS
        return {
            "left_bits": left,
            "negated_right_bits": negated_b,
            "result_bits": result_bits,
            "carry": carry,
            "decimal_result": result_value,
            "overflow": overflow,
        }

    @staticmethod
    def build_codes_report(number_text: str) -> str:
        value = parse_signed_int(number_text)
        sign_magnitude = IntegerCodeService.to_sign_magnitude(value)
        ones = IntegerCodeService.to_ones_complement(value)
        twos = IntegerCodeService.to_twos_complement(value)
        return (
            f"Число: {value}\n"
            f"Прямой код:        {format_bits(sign_magnitude)}\n"
            f"Обратный код:      {format_bits(ones)}\n"
            f"Дополнительный код:{format_bits(twos)}"
        )
