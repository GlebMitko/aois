from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.model.integer_codes import IntegerCodeService, MAX_TWOS, MIN_TWOS


class IntegerCodeTests(unittest.TestCase):
    def test_sign_magnitude_positive(self) -> None:
        bits = IntegerCodeService.to_sign_magnitude(13)
        self.assertEqual(bits[0], 0)
        self.assertEqual(IntegerCodeService.from_sign_magnitude(bits), 13)

    def test_sign_magnitude_negative(self) -> None:
        bits = IntegerCodeService.to_sign_magnitude(-13)
        self.assertEqual(bits[0], 1)
        self.assertEqual(IntegerCodeService.from_sign_magnitude(bits), -13)

    def test_ones_complement_negative(self) -> None:
        bits = IntegerCodeService.to_ones_complement(-5)
        self.assertEqual(IntegerCodeService.from_ones_complement(bits), -5)

    def test_twos_complement_negative(self) -> None:
        bits = IntegerCodeService.to_twos_complement(-13)
        self.assertEqual(IntegerCodeService.from_twos_complement(bits), -13)

    def test_add_twos(self) -> None:
        data = IntegerCodeService.add_twos(12, -5)
        self.assertEqual(data["decimal_result"], 7)
        self.assertFalse(data["overflow"])

    def test_add_twos_overflow(self) -> None:
        data = IntegerCodeService.add_twos(MAX_TWOS, 1)
        self.assertTrue(data["overflow"])

    def test_subtract_twos(self) -> None:
        data = IntegerCodeService.subtract_twos(12, 5)
        self.assertEqual(data["decimal_result"], 7)

    def test_subtract_twos_min_value(self) -> None:
        data = IntegerCodeService.subtract_twos(0, MIN_TWOS)
        self.assertTrue(data["overflow"])

    def test_build_codes_report(self) -> None:
        report = IntegerCodeService.build_codes_report("-13")
        self.assertIn("Прямой код", report)
        self.assertIn("Обратный код", report)
        self.assertIn("Дополнительный код", report)


if __name__ == "__main__":
    unittest.main()
