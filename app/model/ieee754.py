"""Работа с IEEE-754 single precision без struct и готовых конвертеров."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .bits import format_bits
from .common import ValidationError, fraction_to_decimal_string, parse_decimal_fraction

EXPONENT_BITS = 8
MANTISSA_BITS = 23
EXPONENT_BIAS = 127
MAX_EXPONENT = 127
MIN_NORMAL_EXPONENT = -126
SUBNORMAL_SHIFT = 149


@dataclass(frozen=True)
class Float32Value:
    bits: list[int]
    category: str
    fraction_value: Fraction | None
    sign: int
    exponent_field: int
    mantissa_field: int

    def bit_string(self) -> str:
        return format_bits(self.bits, group=4)

    def decimal_string(self) -> str:
        if self.category == "nan":
            return "NaN"
        if self.category == "inf":
            return "-Infinity" if self.sign else "Infinity"
        assert self.fraction_value is not None
        return fraction_to_decimal_string(self.fraction_value, precision=10)


def _round_fraction_to_int(value: Fraction) -> int:
    floor_value = value.numerator // value.denominator
    remainder = value - floor_value
    half = Fraction(1, 2)
    if remainder > half:
        return floor_value + 1
    if remainder < half:
        return floor_value
    return floor_value + (floor_value % 2)


class Float32Service:
    """Сервис IEEE-754 single precision."""

    @staticmethod
    def from_decimal_text(text: str) -> Float32Value:
        fraction = parse_decimal_fraction(text)
        return Float32Service.from_fraction(fraction)

    @staticmethod
    def from_fraction(value: Fraction) -> Float32Value:
        sign = 1 if value < 0 else 0
        abs_value = -value if value < 0 else value

        if abs_value == 0:
            return Float32Value([sign] + [0] * 31, "zero", Fraction(0, 1), sign, 0, 0)

        exponent = 0
        normalized = abs_value
        while normalized >= 2:
            normalized /= 2
            exponent += 1
        while normalized < 1:
            normalized *= 2
            exponent -= 1

        if exponent > MAX_EXPONENT:
            bits = [sign] + [1] * EXPONENT_BITS + [0] * MANTISSA_BITS
            return Float32Value(bits, "inf", None, sign, 255, 0)

        if exponent < MIN_NORMAL_EXPONENT:
            scaled = abs_value * (1 << SUBNORMAL_SHIFT)
            mantissa = _round_fraction_to_int(scaled)
            if mantissa == 0:
                return Float32Value([sign] + [0] * 31, "zero", Fraction(0, 1), sign, 0, 0)
            if mantissa >= (1 << MANTISSA_BITS):
                exponent_field = 1
                mantissa = 0
                bits = [sign] + _int_to_bits(exponent_field, EXPONENT_BITS) + _int_to_bits(mantissa, MANTISSA_BITS)
                value_back = Float32Service.decode_bits(bits)
                return value_back
            bits = [sign] + [0] * EXPONENT_BITS + _int_to_bits(mantissa, MANTISSA_BITS)
            return Float32Service.decode_bits(bits)

        fraction_part = normalized - 1
        mantissa_fraction = fraction_part * (1 << MANTISSA_BITS)
        mantissa = _round_fraction_to_int(mantissa_fraction)
        if mantissa == (1 << MANTISSA_BITS):
            exponent += 1
            mantissa = 0
            if exponent > MAX_EXPONENT:
                bits = [sign] + [1] * EXPONENT_BITS + [0] * MANTISSA_BITS
                return Float32Value(bits, "inf", None, sign, 255, 0)

        exponent_field = exponent + EXPONENT_BIAS
        bits = [sign] + _int_to_bits(exponent_field, EXPONENT_BITS) + _int_to_bits(mantissa, MANTISSA_BITS)
        return Float32Service.decode_bits(bits)

    @staticmethod
    def decode_bits(bits: list[int]) -> Float32Value:
        if len(bits) != 32:
            raise ValidationError("IEEE-754 single precision должен содержать 32 бита")
        sign = bits[0]
        exponent_field = _bits_to_int(bits[1:9])
        mantissa_field = _bits_to_int(bits[9:])

        if exponent_field == 255:
            if mantissa_field == 0:
                return Float32Value(bits, "inf", None, sign, exponent_field, mantissa_field)
            return Float32Value(bits, "nan", None, sign, exponent_field, mantissa_field)

        if exponent_field == 0:
            if mantissa_field == 0:
                return Float32Value(bits, "zero", Fraction(0, 1), sign, exponent_field, mantissa_field)
            value = Fraction(mantissa_field, 1 << MANTISSA_BITS) * Fraction(1, 1 << 126)
        else:
            value = (Fraction(1, 1) + Fraction(mantissa_field, 1 << MANTISSA_BITS)) * (Fraction(1 << (exponent_field - EXPONENT_BIAS), 1) if exponent_field >= EXPONENT_BIAS else Fraction(1, 1 << (EXPONENT_BIAS - exponent_field)))

        if sign:
            value = -value
        category = "subnormal" if exponent_field == 0 else "normal"
        return Float32Value(bits, category, value, sign, exponent_field, mantissa_field)

    @staticmethod
    def operation(left_text: str, right_text: str, operator: str) -> dict[str, str]:
        left_value = Float32Service.from_decimal_text(left_text)
        right_value = Float32Service.from_decimal_text(right_text)
        left_fraction = left_value.fraction_value or Fraction(0, 1)
        right_fraction = right_value.fraction_value or Fraction(0, 1)

        if operator == "+":
            raw = left_fraction + right_fraction
        elif operator == "-":
            raw = left_fraction - right_fraction
        elif operator == "*":
            raw = left_fraction * right_fraction
        elif operator == "/":
            if right_fraction == 0:
                if left_fraction == 0:
                    result = Float32Value([0] + [1] * EXPONENT_BITS + [1] + [0] * (MANTISSA_BITS - 1), "nan", None, 0, 255, 1 << (MANTISSA_BITS - 1))
                    return Float32Service._pack_operation_result(left_value, right_value, result, operator)
                sign = 1 if (left_value.sign ^ right_value.sign) else 0
                result = Float32Value([sign] + [1] * EXPONENT_BITS + [0] * MANTISSA_BITS, "inf", None, sign, 255, 0)
                return Float32Service._pack_operation_result(left_value, right_value, result, operator)
            raw = left_fraction / right_fraction
        else:
            raise ValidationError("Неизвестная операция")

        result = Float32Service.from_fraction(raw)
        return Float32Service._pack_operation_result(left_value, right_value, result, operator)

    @staticmethod
    def _pack_operation_result(left: Float32Value, right: Float32Value, result: Float32Value, operator: str) -> dict[str, str]:
        return {
            "left_bits": left.bit_string(),
            "right_bits": right.bit_string(),
            "result_bits": result.bit_string(),
            "left_decimal": left.decimal_string(),
            "right_decimal": right.decimal_string(),
            "result_decimal": result.decimal_string(),
            "operator": operator,
        }

    @staticmethod
    def build_conversion_report(number_text: str) -> str:
        value = Float32Service.from_decimal_text(number_text)
        return (
            f"IEEE-754 (32 бита): {value.bit_string()}\n"
            f"Категория: {value.category}\n"
            f"В десятичном виде после нормализации: {value.decimal_string()}"
        )

    @staticmethod
    def build_operation_report(left_text: str, right_text: str, operator: str) -> str:
        data = Float32Service.operation(left_text, right_text, operator)
        return (
            f"A: {data['left_decimal']}\n"
            f"A (IEEE-754): {data['left_bits']}\n"
            f"B: {data['right_decimal']}\n"
            f"B (IEEE-754): {data['right_bits']}\n"
            f"Операция: A {data['operator']} B\n"
            f"Результат (IEEE-754): {data['result_bits']}\n"
            f"Результат (10): {data['result_decimal']}"
        )


def _int_to_bits(value: int, width: int) -> list[int]:
    bits = [0] * width
    index = width - 1
    current = value
    while current > 0 and index >= 0:
        bits[index] = current % 2
        current //= 2
        index -= 1
    return bits


def _bits_to_int(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = value * 2 + bit
    return value
