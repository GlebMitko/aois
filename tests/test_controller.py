from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.controller import AppController
from app.model.integer_codes import MAX_TWOS, MIN_TWOS


class ControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = AppController()

    def test_integer_codes(self) -> None:
        report = self.controller.integer_codes("-13")
        self.assertIn("Прямой код", report)

    def test_integer_add(self) -> None:
        report = self.controller.integer_add("12", "-5")
        self.assertIn("Сумма (10): 7", report)

    def test_integer_add_overflow(self) -> None:
        report = self.controller.integer_add(str(MAX_TWOS), "1")
        self.assertIn("переполнение", report)

    def test_integer_subtract(self) -> None:
        report = self.controller.integer_subtract("12", "5")
        self.assertIn("Разность (10): 7", report)

    def test_integer_subtract_overflow(self) -> None:
        report = self.controller.integer_subtract("0", str(MIN_TWOS))
        self.assertIn("переполнение", report)

    def test_integer_multiply(self) -> None:
        report = self.controller.integer_multiply("3", "5")
        self.assertIn("15", report)

    def test_integer_divide(self) -> None:
        report = self.controller.integer_divide("7", "2")
        self.assertIn("3.5", report)

    def test_float_convert(self) -> None:
        report = self.controller.float_convert("3.5")
        self.assertIn("Категория", report)

    def test_float_operation(self) -> None:
        report = self.controller.float_operation("3.5", "1.25", "+")
        self.assertIn("4.75", report)

    def test_bcd_add(self) -> None:
        report = self.controller.bcd_add("74", "87", "8421")
        self.assertIn("161", report)


if __name__ == "__main__":
    unittest.main()
