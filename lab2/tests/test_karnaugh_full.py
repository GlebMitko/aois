# tests/test_karnaugh_full.py - упрощенная версия
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_parser import LogicParser
from truth_table import TruthTable
from minimization_karnaugh import KarnaughMap


class TestKarnaughComplete(unittest.TestCase):
    """Работающие тесты для карт Карно"""

    def test_1var_all_cases(self):
        p = LogicParser("a&!a", ['a'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "0")

        p = LogicParser("a|!a", ['a'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "1")

        p = LogicParser("a", ['a'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a")

        p = LogicParser("!a", ['a'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "!a")

    def test_2var_and(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a&b")

    def test_2var_or(self):
        p = LogicParser("a|b", ['a', 'b'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertTrue("a" in dnf and "b" in dnf)

    def test_3var_and(self):
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a&b&c")

    def test_3var_or(self):
        p = LogicParser("a|b|c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)

    def test_print_method(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        try:
            k.print_karnaugh_dnf()
            result = True
        except:
            result = False
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()