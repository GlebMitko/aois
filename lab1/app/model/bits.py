"""Низкоуровневые операции над битовыми массивами."""

from __future__ import annotations

from .common import ValidationError

WORD_SIZE = 32


BitList = list[int]


def ensure_bit_list(bits: BitList, width: int = WORD_SIZE) -> BitList:
    if len(bits) != width:
        raise ValidationError(f"Ожидалось {width} бит")
    for bit in bits:
        if bit not in (0, 1):
            raise ValidationError("Массив должен содержать только 0 и 1")
    return list(bits)


def zero_bits(width: int = WORD_SIZE) -> BitList:
    return [0] * width


def unsigned_to_bits(value: int, width: int = WORD_SIZE) -> BitList:
    if value < 0:
        raise ValidationError("Ожидалось неотрицательное число")
    limit = 1 << width
    if value >= limit:
        raise OverflowError(f"Число {value} не помещается в {width} бит")
    bits = [0] * width
    remaining = value
    index = width - 1
    while remaining > 0 and index >= 0:
        bits[index] = remaining % 2
        remaining //= 2
        index -= 1
    return bits


def bits_to_unsigned(bits: BitList) -> int:
    checked = ensure_bit_list(bits, len(bits))
    value = 0
    for bit in checked:
        value = value * 2 + bit
    return value


def invert_bits(bits: BitList) -> BitList:
    return [1 - bit for bit in bits]


def add_bit_lists(left: BitList, right: BitList) -> tuple[BitList, int]:
    if len(left) != len(right):
        raise ValidationError("Слагаемые должны иметь одинаковую длину")

    result = [0] * len(left)
    carry = 0
    for index in range(len(left) - 1, -1, -1):
        total = left[index] + right[index] + carry
        result[index] = total % 2
        carry = total // 2
    return result, carry


def add_one(bits: BitList) -> tuple[BitList, int]:
    return add_bit_lists(bits, [0] * (len(bits) - 1) + [1])


def twos_complement_negation(bits: BitList) -> BitList:
    inverted = invert_bits(bits)
    negated, _ = add_one(inverted)
    return negated


def shift_left(bits: BitList, count: int = 1) -> BitList:
    checked = ensure_bit_list(bits, len(bits))
    if count < 0:
        raise ValidationError("Сдвиг должен быть неотрицательным")
    if count == 0:
        return checked
    if count >= len(bits):
        return [0] * len(bits)
    return checked[count:] + [0] * count


def format_bits(bits: BitList, group: int = 4) -> str:
    checked = ensure_bit_list(bits, len(bits))
    if group <= 0:
        return "".join(str(bit) for bit in checked)
    chunks = []
    for index in range(0, len(checked), group):
        chunks.append("".join(str(bit) for bit in checked[index:index + group]))
    return " ".join(chunks)


def trim_leading_zeroes(bits: BitList) -> BitList:
    checked = ensure_bit_list(bits, len(bits))
    index = 0
    while index < len(checked) - 1 and checked[index] == 0:
        index += 1
    return checked[index:]
