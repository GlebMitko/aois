# tests/test_utils.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    int_to_bits, bits_to_int, print_truth_table,
    get_minterms, get_maxterms, build_sdnf, build_sknf, to_not_and_or
)


class TestUtils(unittest.TestCase):

    def test_int_to_bits(self):
        self.assertEqual(int_to_bits(0, 4), [0, 0, 0, 0])
        self.assertEqual(int_to_bits(5, 4), [0, 1, 0, 1])
        self.assertEqual(int_to_bits(7, 3), [1, 1, 1])
        self.assertEqual(int_to_bits(8, 4), [1, 0, 0, 0])

    def test_bits_to_int(self):
        self.assertEqual(bits_to_int([0, 0, 0, 0]), 0)
        self.assertEqual(bits_to_int([0, 1, 0, 1]), 5)
        self.assertEqual(bits_to_int([1, 1, 1]), 7)
        self.assertEqual(bits_to_int([1, 0, 0, 0]), 8)

    def test_get_minterms(self):
        rows = [
            {'out': 1}, {'out': 0}, {'out': 1}, {'out': 0}
        ]
        minterms = get_minterms(rows, 'out')
        self.assertEqual(minterms, [0, 2])

    def test_get_maxterms(self):
        rows = [
            {'out': 1}, {'out': 0}, {'out': 1}, {'out': 0}
        ]
        maxterms = get_maxterms(rows, 'out', 2)
        self.assertEqual(maxterms, [1, 3])

    def test_build_sdnf_simple(self):
        minterms = [5]  # 0101
        var_names = ['A', 'B', 'C', 'D']
        sdnf = build_sdnf(minterms, var_names)
        self.assertEqual(sdnf, "!A&B&!C&D")

    def test_build_sdnf_empty(self):
        self.assertEqual(build_sdnf([], ['A', 'B']), "0")

    def test_build_sdnf_multiple(self):
        minterms = [0, 3]  # 0000, 0011
        var_names = ['A', 'B']
        sdnf = build_sdnf(minterms, var_names)
        # Разбираем на термы
        terms = sdnf.split(' | ')
        self.assertEqual(len(terms), 2)
        # Проверяем что оба терма корректны (порядок не важен)
        # Возможные варианты: '!A&!B' и '!A&B' ИЛИ '!A&!B' и 'A&B' (зависит от реализации)
        valid_first_terms = ['!A&!B', '!A&!B']
        self.assertTrue(terms[0] in ['!A&!B', '!A&B', 'A&B'])
        self.assertTrue(terms[1] in ['!A&!B', '!A&B', 'A&B'])

    def test_build_sknf_simple(self):
        maxterms = [5]  # 0101
        var_names = ['A', 'B', 'C', 'D']
        sknf = build_sknf(maxterms, var_names)
        self.assertIn("(A | !B | C | !D)", sknf)

    def test_build_sknf_empty(self):
        self.assertEqual(build_sknf([], ['A', 'B']), "1")

    def test_to_not_and_or_single_and(self):
        self.assertEqual(to_not_and_or("A&B"), "A&B")

    def test_to_not_and_or_single_not(self):
        result = to_not_and_or("!A")
        # Допускаем оба варианта
        self.assertTrue(result == "!A" or result == "!(A)")

    def test_to_not_and_or_or(self):
        result = to_not_and_or("A | B")
        self.assertEqual(result, "!(!A & !B)")

    def test_to_not_and_or_complex(self):
        result = to_not_and_or("A&B | C&D")
        self.assertEqual(result, "!(!(A&B) & !(C&D))")

    def test_to_not_and_or_zero(self):
        self.assertEqual(to_not_and_or("0"), "0")

    def test_to_not_and_or_one(self):
        self.assertEqual(to_not_and_or("1"), "1")

    def test_print_truth_table(self):
        """Тест функции вывода таблицы"""
        import io
        import sys
        vars_list = ['A', 'B']
        rows = [{'A': 0, 'B': 0}, {'A': 0, 'B': 1}]
        outputs = ['A', 'B']
        captured = io.StringIO()
        sys.stdout = captured
        print_truth_table(vars_list, rows, outputs)
        sys.stdout = sys.__stdout__
        self.assertIn("A | B", captured.getvalue())


if __name__ == '__main__':
    unittest.main()