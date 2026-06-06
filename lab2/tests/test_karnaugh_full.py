# tests/test_karnaugh_full.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_parser import LogicParser
from truth_table import TruthTable
from minimization_karnaugh import KarnaughMap


class TestKarnaughComplete(unittest.TestCase):
    """Проверка основных контрактов обновленного класса Карно"""

    def test_basic_dnf_cnf_execution(self):
        p = LogicParser("(a & b) | c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)

        dnf, _ = k.minimize_dnf()
        cnf, _ = k.minimize_cnf()

        self.assertIsNotNone(dnf)
        self.assertIsNotNone(cnf)
        self.assertIsInstance(dnf, str)
        self.assertIsInstance(cnf, str)


if __name__ == '__main__':
    unittest.main()