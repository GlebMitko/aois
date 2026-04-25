from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.model.common import ValidationError
from app.model.ieee754 import Float32Service, _round_fraction_to_int


class Float32Tests(unittest.TestCase):
    def _compact(self, bit_string: str) -> str:
        return bit_string.replace(" ", "")

    def test_round_fraction_to_int_lower_than_half(self) -> None:
        self.assertEqual(_round_fraction_to_int(Fraction(12, 10)), 1)

    def test_round_fraction_to_int_higher_than_half(self) -> None:
        self.assertEqual(_round_fraction_to_int(Fraction(16, 10)), 2)

    def test_round_fraction_to_int_tie_even(self) -> None:
        self.assertEqual(_round_fraction_to_int(Fraction(5, 2)), 2)
        self.assertEqual(_round_fraction_to_int(Fraction(7, 2)), 4)

    def test_from_decimal_one(self) -> None:
        value = Float32Service.from_decimal_text("1")
        self.assertEqual(self._compact(value.bit_string()), "00111111100000000000000000000000")
        self.assertEqual(value.decimal_string(), "1")

    def test_from_decimal_half(self) -> None:
        value = Float32Service.from_decimal_text("0.5")
        self.assertEqual(self._compact(value.bit_string()), "00111111000000000000000000000000")

    def test_from_decimal_negative(self) -> None:
        value = Float32Service.from_decimal_text("-2.5")
        self.assertEqual(self._compact(value.bit_string()), "11000000001000000000000000000000")

    def test_from_decimal_point_one(self) -> None:
        value = Float32Service.from_decimal_text("0.1")
        self.assertEqual(self._compact(value.bit_string()), "00111101110011001100110011001101")

    def test_zero(self) -> None:
        value = Float32Service.from_decimal_text("0")
        self.assertEqual(value.category, "zero")

    def test_subnormal(self) -> None:
        value = Float32Service.from_decimal_text("0.000000000000000000000000000000000000000000001")
        self.assertEqual(value.category, "subnormal")
        self.assertEqual(self._compact(value.bit_string()), "00000000000000000000000000000001")

    def test_tiny_value_rounds_to_zero(self) -> None:
        value = Float32Service.from_fraction(Fraction(1, 1 << 200))
        self.assertEqual(value.category, "zero")

    def test_huge_value_becomes_infinity(self) -> None:
        value = Float32Service.from_fraction(Fraction(1 << 200, 1))
        self.assertEqual(value.category, "inf")
        self.assertEqual(value.decimal_string(), "Infinity")

    def test_decode_bits_invalid_length(self) -> None:
        with self.assertRaises(ValidationError):
            Float32Service.decode_bits([0, 1])

    def test_decode_infinity(self) -> None:
        value = Float32Service.decode_bits([0] + [1] * 8 + [0] * 23)
        self.assertEqual(value.category, "inf")

    def test_decode_nan(self) -> None:
        value = Float32Service.decode_bits([0] + [1] * 8 + [1] + [0] * 22)
        self.assertEqual(value.category, "nan")
        self.assertEqual(value.decimal_string(), "NaN")

    def test_addition(self) -> None:
        data = Float32Service.operation("3.5", "-1.25", "+")
        self.assertEqual(data["result_decimal"], "2.25")

    def test_subtraction(self) -> None:
        data = Float32Service.operation("3.5", "1.25", "-")
        self.assertEqual(data["result_decimal"], "2.25")

    def test_multiplication(self) -> None:
        data = Float32Service.operation("1.5", "2", "*")
        self.assertEqual(data["result_decimal"], "3")

    def test_division(self) -> None:
        data = Float32Service.operation("7", "2", "/")
        self.assertEqual(data["result_decimal"], "3.5")

    def test_division_by_zero(self) -> None:
        data = Float32Service.operation("1", "0", "/")
        self.assertEqual(data["result_decimal"], "Infinity")

    def test_zero_divided_by_zero(self) -> None:
        data = Float32Service.operation("0", "0", "/")
        self.assertEqual(data["result_decimal"], "NaN")

    def test_invalid_operator(self) -> None:
        with self.assertRaises(ValidationError):
            Float32Service.operation("1", "1", "%")

    def test_conversion_report(self) -> None:
        report = Float32Service.build_conversion_report("3.5")
        self.assertIn("IEEE-754", report)
        self.assertIn("3.5", report)

    def test_operation_report(self) -> None:
        report = Float32Service.build_operation_report("3.5", "1.25", "+")
        self.assertIn("Результат (10): 4.75", report)


if __name__ == "__main__":
    unittest.main()
