from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.model.integer_arithmetic import IntegerArithmeticService


class IntegerArithmeticTests(unittest.TestCase):
    def test_multiply_sign_magnitude_positive(self) -> None:
        data = IntegerArithmeticService.multiply_sign_magnitude(3, 5)
        self.assertEqual(data["decimal_result"], 15)
        self.assertFalse(data["overflow"])

    def test_multiply_sign_magnitude_negative(self) -> None:
        data = IntegerArithmeticService.multiply_sign_magnitude(-3, 5)
        self.assertEqual(data["decimal_result"], -15)
        self.assertEqual(data["result_bits"][0], 1)

    def test_divide_sign_magnitude(self) -> None:
        data = IntegerArithmeticService.divide_sign_magnitude(7, 2)
        self.assertEqual(data["decimal_result"], "3.5")
        self.assertTrue(data["binary_result"].startswith("11.1"))

    def test_divide_sign_magnitude_negative(self) -> None:
        data = IntegerArithmeticService.divide_sign_magnitude(-9, 2)
        self.assertEqual(data["decimal_result"], "-4.5")
        self.assertTrue(data["binary_result"].startswith("-100.1"))

    def test_divide_by_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            IntegerArithmeticService.divide_sign_magnitude(1, 0)

    def test_multiplication_report(self) -> None:
        report = IntegerArithmeticService.build_multiplication_report("3", "5")
        self.assertIn("В десятичном виде: 15", report)

    def test_division_report(self) -> None:
        report = IntegerArithmeticService.build_division_report("7", "2")
        self.assertIn("Частное в десятичном виде: 3.5", report)


if __name__ == "__main__":
    unittest.main()
