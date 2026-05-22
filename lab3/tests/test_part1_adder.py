# tests/test_part1_adder.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from part1_adder_sknf import FullAdderSKNF


class TestFullAdderSKNF(unittest.TestCase):

    def setUp(self):
        self.adder = FullAdderSKNF()

    def test_truth_table_rows_count(self):
        """Таблица истинности должна содержать 8 строк (2^3)"""
        rows = self.adder.truth_table()
        self.assertEqual(len(rows), 8)

    def test_truth_table_values(self):
        """Проверка всех комбинаций таблицы истинности"""
        rows = self.adder.truth_table()

        # (0,0,0) -> sum=0, cout=0
        self.assertEqual(rows[0]['Sum'], 0)
        self.assertEqual(rows[0]['Cout'], 0)

        # (0,0,1) -> sum=1, cout=0
        self.assertEqual(rows[1]['Sum'], 1)
        self.assertEqual(rows[1]['Cout'], 0)

        # (0,1,0) -> sum=1, cout=0
        self.assertEqual(rows[2]['Sum'], 1)
        self.assertEqual(rows[2]['Cout'], 0)

        # (0,1,1) -> sum=0, cout=1
        self.assertEqual(rows[3]['Sum'], 0)
        self.assertEqual(rows[3]['Cout'], 1)

        # (1,0,0) -> sum=1, cout=0
        self.assertEqual(rows[4]['Sum'], 1)
        self.assertEqual(rows[4]['Cout'], 0)

        # (1,0,1) -> sum=0, cout=1
        self.assertEqual(rows[5]['Sum'], 0)
        self.assertEqual(rows[5]['Cout'], 1)

        # (1,1,0) -> sum=0, cout=1
        self.assertEqual(rows[6]['Sum'], 0)
        self.assertEqual(rows[6]['Cout'], 1)

        # (1,1,1) -> sum=1, cout=1
        self.assertEqual(rows[7]['Sum'], 1)
        self.assertEqual(rows[7]['Cout'], 1)

    def test_get_sum_sknf(self):
        """Проверка СКНФ для суммы"""
        sknf = self.adder.get_sum_sknf()
        # Должна содержать 4 терма
        self.assertEqual(sknf.count('&'), 3)  # 3 оператора & для 4 термов
        self.assertIn("A | B | Cin", sknf)
        self.assertIn("A | !B | !Cin", sknf)
        self.assertIn("!A | B | !Cin", sknf)
        self.assertIn("!A | !B | Cin", sknf)

    def test_get_cout_sknf(self):
        """Проверка СКНФ для переноса"""
        sknf = self.adder.get_cout_sknf()
        self.assertIn("A | B | Cin", sknf)
        self.assertIn("A | B | !Cin", sknf)
        self.assertIn("A | !B | Cin", sknf)
        self.assertIn("!A | B | Cin", sknf)

    def test_vars_list(self):
        """Проверка списка переменных"""
        self.assertEqual(self.adder.vars, ['A', 'B', 'Cin'])

    def test_outputs_list(self):
        """Проверка списка выходов"""
        self.assertEqual(self.adder.outputs, ['Sum', 'Cout'])

    def test_8bit_adder_description(self):
        """Проверка описания 8-битного сумматора"""
        desc = self.adder.get_8bit_adder_description()
        self.assertIsInstance(desc, str)
        self.assertIn("8-БИТНЫЙ СУММАТОР", desc)
        self.assertIn("8 + 6 = 14", desc)

    def test_print_info(self):
        """Тест вывода информации (не падает)"""
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        self.adder.print_info()
        sys.stdout = sys.__stdout__
        self.assertIn("СКНФ", captured.getvalue())

    def test_get_8bit_adder_description_contains_example(self):
        """Проверка наличия примера 8+6 в описании"""
        desc = self.adder.get_8bit_adder_description()
        self.assertIn("8", desc)
        self.assertIn("6", desc)
        self.assertIn("14", desc)


if __name__ == '__main__':
    unittest.main()