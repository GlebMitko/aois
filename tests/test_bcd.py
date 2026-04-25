from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.model.bcd import BCDService
from app.model.common import ValidationError


class BCDTests(unittest.TestCase):
    def test_encode_number_8421(self) -> None:
        self.assertEqual(BCDService.encode_number("74", "8421"), "0111 0100")

    def test_encode_number_2421(self) -> None:
        self.assertEqual(BCDService.encode_number("59", "2421"), "1011 1111")

    def test_encode_number_excess3(self) -> None:
        self.assertEqual(BCDService.encode_number("09", "EXCESS-3"), "0011 1100")

    def test_add_numbers(self) -> None:
        data = BCDService.add_numbers("74", "87", "8421")
        self.assertEqual(data["decimal_result"], "161")
        self.assertEqual(data["result_bcd"], "0001 0110 0001")

    def test_build_report(self) -> None:
        report = BCDService.build_report("74", "87", "8421")
        self.assertIn("8421 BCD", report)
        self.assertIn("161", report)

    def test_invalid_digit(self) -> None:
        with self.assertRaises(ValidationError):
            BCDService.encode_number("-5", "8421")

    def test_empty_number(self) -> None:
        with self.assertRaises(ValidationError):
            BCDService.encode_number("", "8421")

    def test_invalid_variant(self) -> None:
        with self.assertRaises(ValidationError):
            BCDService.encode_number("5", "BAD")


if __name__ == "__main__":
    unittest.main()
