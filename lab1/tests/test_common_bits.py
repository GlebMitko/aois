from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.model.bits import (
    add_bit_lists,
    add_one,
    bits_to_unsigned,
    ensure_bit_list,
    format_bits,
    invert_bits,
    shift_left,
    trim_leading_zeroes,
    twos_complement_negation,
    unsigned_to_bits,
    zero_bits,
)
from app.model.common import (
    ValidationError,
    decimal_division_string,
    decimal_string_add,
    fraction_to_decimal_string,
    parse_decimal_fraction,
    parse_signed_int,
    parse_unsigned_int,
)


class ParseTests(unittest.TestCase):
    def test_parse_signed_int_positive(self) -> None:
        self.assertEqual(parse_signed_int("12345"), 12345)

    def test_parse_signed_int_negative(self) -> None:
        self.assertEqual(parse_signed_int("-77"), -77)

    def test_parse_signed_int_invalid(self) -> None:
        with self.assertRaises(ValidationError):
            parse_signed_int("12a")

    def test_parse_signed_int_none(self) -> None:
        with self.assertRaises(ValidationError):
            parse_signed_int(None)

    def test_parse_signed_int_empty(self) -> None:
        with self.assertRaises(ValidationError):
            parse_signed_int("   ")

    def test_parse_signed_int_sign_only(self) -> None:
        with self.assertRaises(ValidationError):
            parse_signed_int("-")

    def test_parse_unsigned_negative(self) -> None:
        with self.assertRaises(ValidationError):
            parse_unsigned_int("-1")

    def test_parse_decimal_fraction(self) -> None:
        self.assertEqual(parse_decimal_fraction("-12.75"), Fraction(-51, 4))

    def test_parse_decimal_fraction_none(self) -> None:
        with self.assertRaises(ValidationError):
            parse_decimal_fraction(None)

    def test_parse_decimal_fraction_empty(self) -> None:
        with self.assertRaises(ValidationError):
            parse_decimal_fraction("  ")

    def test_parse_decimal_fraction_invalid_dots(self) -> None:
        with self.assertRaises(ValidationError):
            parse_decimal_fraction("1.2.3")

    def test_parse_decimal_fraction_dot_only(self) -> None:
        with self.assertRaises(ValidationError):
            parse_decimal_fraction(".")

    def test_parse_decimal_fraction_without_integer_part(self) -> None:
        self.assertEqual(parse_decimal_fraction(".5"), Fraction(1, 2))

    def test_parse_decimal_fraction_invalid_char(self) -> None:
        with self.assertRaises(ValidationError):
            parse_decimal_fraction("1.a")

    def test_decimal_string_add(self) -> None:
        self.assertEqual(decimal_string_add("74", "87"), "161")

    def test_decimal_string_add_empty(self) -> None:
        with self.assertRaises(ValidationError):
            decimal_string_add("", "1")

    def test_decimal_string_add_invalid(self) -> None:
        with self.assertRaises(ValidationError):
            decimal_string_add("1", "-2")

    def test_decimal_division_string(self) -> None:
        self.assertEqual(decimal_division_string(7, 2, 5), "3.50000")

    def test_decimal_division_string_zero_digits(self) -> None:
        self.assertEqual(decimal_division_string(-7, 2, 0), "-3")

    def test_decimal_division_string_zero_divisor(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            decimal_division_string(1, 0, 5)

    def test_fraction_to_decimal_string(self) -> None:
        self.assertEqual(fraction_to_decimal_string(Fraction(7, 2), 5), "3.5")

    def test_fraction_to_decimal_string_negative_zero(self) -> None:
        self.assertEqual(fraction_to_decimal_string(Fraction(-1, 1000), 0), "0")


class BitsTests(unittest.TestCase):
    def test_ensure_bit_list_invalid_length(self) -> None:
        with self.assertRaises(ValidationError):
            ensure_bit_list([0, 1], 4)

    def test_ensure_bit_list_invalid_value(self) -> None:
        with self.assertRaises(ValidationError):
            ensure_bit_list([0, 2, 1], 3)

    def test_zero_bits(self) -> None:
        self.assertEqual(zero_bits(4), [0, 0, 0, 0])

    def test_unsigned_to_bits_and_back(self) -> None:
        bits = unsigned_to_bits(13, 8)
        self.assertEqual(bits, [0, 0, 0, 0, 1, 1, 0, 1])
        self.assertEqual(bits_to_unsigned(bits), 13)

    def test_unsigned_to_bits_negative(self) -> None:
        with self.assertRaises(ValidationError):
            unsigned_to_bits(-1, 4)

    def test_unsigned_to_bits_overflow(self) -> None:
        with self.assertRaises(OverflowError):
            unsigned_to_bits(16, 4)

    def test_add_bit_lists(self) -> None:
        result, carry = add_bit_lists([0, 1, 1, 1], [0, 0, 0, 1])
        self.assertEqual(result, [1, 0, 0, 0])
        self.assertEqual(carry, 0)

    def test_add_bit_lists_mismatch(self) -> None:
        with self.assertRaises(ValidationError):
            add_bit_lists([1, 0], [1])

    def test_add_one(self) -> None:
        result, carry = add_one([1, 1, 1, 1])
        self.assertEqual(result, [0, 0, 0, 0])
        self.assertEqual(carry, 1)

    def test_invert_bits(self) -> None:
        self.assertEqual(invert_bits([1, 0, 1, 0]), [0, 1, 0, 1])

    def test_twos_complement_negation(self) -> None:
        self.assertEqual(twos_complement_negation([0, 0, 0, 1]), [1, 1, 1, 1])

    def test_shift_left(self) -> None:
        self.assertEqual(shift_left([0, 0, 1, 1], 1), [0, 1, 1, 0])

    def test_shift_left_zero(self) -> None:
        self.assertEqual(shift_left([0, 1, 1, 0], 0), [0, 1, 1, 0])

    def test_shift_left_large(self) -> None:
        self.assertEqual(shift_left([0, 1, 1, 0], 5), [0, 0, 0, 0])

    def test_shift_left_negative(self) -> None:
        with self.assertRaises(ValidationError):
            shift_left([0, 1, 1, 0], -1)

    def test_format_bits(self) -> None:
        self.assertEqual(format_bits([1, 0, 1, 0, 1, 0, 1, 0], 4), "1010 1010")

    def test_format_bits_without_groups(self) -> None:
        self.assertEqual(format_bits([1, 0, 1, 0], 0), "1010")

    def test_trim_leading_zeroes(self) -> None:
        self.assertEqual(trim_leading_zeroes([0, 0, 1, 0]), [1, 0])


if __name__ == "__main__":
    unittest.main()
