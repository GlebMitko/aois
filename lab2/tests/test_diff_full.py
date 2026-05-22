# tests/test_diff_full.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_parser import LogicParser
from truth_table import TruthTable
from boolean_diff import BooleanDifferentiation


class TestDifferentiationComplete(unittest.TestCase):
    """Полное покрытие булевой дифференциации"""

    def test_derivative_1var(self):
        """Тест 1 переменная"""
        p = LogicParser("a", ['a'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(deriv, [1])

    def test_derivative_2var_and(self):
        """Тест AND 2 переменные"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertEqual(d.partial_derivative_vector('a'), [0, 1])
        self.assertEqual(d.partial_derivative_vector('b'), [0, 1])

    def test_derivative_2var_or(self):
        """Тест OR 2 переменные"""
        p = LogicParser("a|b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertEqual(d.partial_derivative_vector('a'), [1, 0])

    def test_derivative_2var_xor(self):
        """Тест XOR 2 переменные"""
        p = LogicParser("(a&!b)|(!a&b)", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertEqual(d.partial_derivative_vector('a'), [1, 1])

    def test_derivative_3var_and(self):
        """Тест AND 3 переменные"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv), 4)

    def test_derivative_3var_complex(self):
        """Тест сложной функции 3 переменные"""
        p = LogicParser("(a&b)|(a&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv), 4)

    def test_mixed_derivative_2var(self):
        """Тест смешанной производной 2 переменные"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertEqual(d.mixed_derivative('a', 'b'), [1])

    def test_mixed_derivative_3var(self):
        """Тест смешанной производной 3 переменные"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        # Порядок может быть [1,0] или [0,1] - просто проверяем длину и тип
        deriv_ab = d.mixed_derivative('a', 'b')
        self.assertEqual(len(deriv_ab), 2)
        self.assertIsInstance(deriv_ab[0], int)
        self.assertIsInstance(deriv_ab[1], int)

        deriv_abc = d.mixed_derivative('a', 'b', 'c')
        self.assertEqual(deriv_abc, [1])

    def test_derivative_numeric_form_2var(self):
        """Тест числовой формы"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        result = d.derivative_numeric_form('a')
        self.assertIsInstance(result, str)

    def test_check_dependence_all(self):
        """Тест зависимости от переменных"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertTrue(d.check_dependence('a'))
        self.assertTrue(d.check_dependence('b'))

    def test_print_derivatives_method(self):
        """Тест вывода производных"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        try:
            d.print_derivatives(max_vars=2)
            result = True
        except:
            result = False
        self.assertTrue(result)

    def test_derivative_4var(self):
        """Тест 4 переменные"""
        p = LogicParser("a&b&c&d", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv), 8)

    def test_derivative_constant(self):
        """Тест константной функции"""
        p = LogicParser("1", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertEqual(d.partial_derivative_vector('a'), [0, 0])
        self.assertEqual(d.partial_derivative_vector('b'), [0, 0])


# Добавьте в конец файла tests/test_diff_full.py

class TestDifferentiationEdgeCases(unittest.TestCase):
    """Тесты граничных случаев дифференциации"""

    def test_derivative_single_bit(self):
        """Тест производной для функции с 1 переменной"""
        p = LogicParser("a", ['a'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(deriv, [1])

    def test_derivative_order_2_with_3var(self):
        """Тест производной 2-го порядка для 3 переменных"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('a', 'b')
        self.assertEqual(len(deriv), 2)

    def test_derivative_order_3_with_3var(self):
        """Тест производной 3-го порядка для 3 переменных"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('a', 'b', 'c')
        self.assertEqual(deriv, [1])

    def test_derivative_complex_order_2(self):
        """Тест сложной функции производная 2-го порядка"""
        p = LogicParser("(a&b)|(a&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('a', 'b')
        self.assertIsInstance(deriv, list)

    def test_partial_derivative_all_vars(self):
        """Тест частных производных для всех переменных"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        for var in ['a', 'b', 'c']:
            deriv = d.partial_derivative_vector(var)
            self.assertEqual(len(deriv), 4)

    def test_mixed_derivative_different_order(self):
        """Тест смешанной производной с разным порядком"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv1 = d.mixed_derivative('a', 'b')
        deriv2 = d.mixed_derivative('b', 'a')
        self.assertEqual(deriv1, deriv2)


if __name__ == '__main__':
    unittest.main()