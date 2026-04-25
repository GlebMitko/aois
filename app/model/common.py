"""Общие функции для работы с десятичными строками и дробями."""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction


class ValidationError(ValueError):
    """Ошибка валидации пользовательского ввода."""


DIGITS = "0123456789"


def parse_signed_int(text: str) -> int:
    """Преобразует строку десятичного целого числа в int без int(text)."""
    if text is None:
        raise ValidationError("Пустое значение")

    cleaned = text.strip()
    if not cleaned:
        raise ValidationError("Пустое значение")

    sign = 1
    if cleaned[0] in "+-":
        sign = -1 if cleaned[0] == "-" else 1
        cleaned = cleaned[1:]

    if not cleaned:
        raise ValidationError("Некорректное целое число")

    value = 0
    for char in cleaned:
        if char not in DIGITS:
            raise ValidationError(f"Некорректный символ: {char}")
        value = value * 10 + (ord(char) - ord("0"))
    return sign * value


def parse_unsigned_int(text: str) -> int:
    value = parse_signed_int(text)
    if value < 0:
        raise ValidationError("Ожидалось неотрицательное число")
    return value


def parse_decimal_fraction(text: str) -> Fraction:
    """Преобразует десятичную строку в Fraction без float(text)."""
    if text is None:
        raise ValidationError("Пустое значение")

    cleaned = text.strip().replace(",", ".")
    if not cleaned:
        raise ValidationError("Пустое значение")

    sign = 1
    if cleaned[0] in "+-":
        sign = -1 if cleaned[0] == "-" else 1
        cleaned = cleaned[1:]

    if cleaned.count(".") > 1:
        raise ValidationError("Слишком много десятичных точек")

    if "." in cleaned:
        int_part, frac_part = cleaned.split(".", 1)
    else:
        int_part, frac_part = cleaned, ""

    if not int_part and not frac_part:
        raise ValidationError("Некорректное вещественное число")

    if int_part:
        integer_value = parse_unsigned_int(int_part)
    else:
        integer_value = 0

    denominator = 1
    fractional_value = 0
    for char in frac_part:
        if char not in DIGITS:
            raise ValidationError(f"Некорректный символ: {char}")
        fractional_value = fractional_value * 10 + (ord(char) - ord("0"))
        denominator *= 10

    result = Fraction(integer_value * denominator + fractional_value, denominator)
    return sign * result


def fraction_to_decimal_string(value: Fraction, precision: int = 10) -> str:
    """Формирует десятичную строку с заданной точностью."""
    getcontext().prec = max(precision + 15, 30)
    dec = Decimal(value.numerator) / Decimal(value.denominator)
    quant = Decimal(1).scaleb(-precision)
    rendered = format(dec.quantize(quant), "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    if rendered == "-0":
        return "0"
    return rendered


def decimal_string_add(a: str, b: str) -> str:
    """Складывает два неотрицательных десятичных числа-строки."""
    a_clean = a.strip()
    b_clean = b.strip()
    if not a_clean or not b_clean:
        raise ValidationError("Пустое число")
    for char in a_clean + b_clean:
        if char not in DIGITS:
            raise ValidationError("BCD-сложение поддерживает только неотрицательные целые числа")

    i = len(a_clean) - 1
    j = len(b_clean) - 1
    carry = 0
    result: list[str] = []

    while i >= 0 or j >= 0 or carry:
        da = ord(a_clean[i]) - ord("0") if i >= 0 else 0
        db = ord(b_clean[j]) - ord("0") if j >= 0 else 0
        total = da + db + carry
        result.append(chr(ord("0") + (total % 10)))
        carry = total // 10
        i -= 1
        j -= 1

    return "".join(reversed(result)).lstrip("0") or "0"


def decimal_division_string(dividend: int, divisor: int, digits_after_point: int = 5) -> str:
    """Делит два целых и формирует десятичную строку с нужной точностью."""
    if divisor == 0:
        raise ZeroDivisionError("Деление на ноль")

    sign = "-" if (dividend < 0) ^ (divisor < 0) else ""
    dividend = abs(dividend)
    divisor = abs(divisor)

    integer_part = dividend // divisor
    remainder = dividend % divisor

    if digits_after_point <= 0:
        return f"{sign}{integer_part}"

    digits: list[str] = []
    for _ in range(digits_after_point):
        remainder *= 10
        digits.append(chr(ord("0") + (remainder // divisor)))
        remainder %= divisor

    return f"{sign}{integer_part}.{' '.join(digits).replace(' ', '')}"
