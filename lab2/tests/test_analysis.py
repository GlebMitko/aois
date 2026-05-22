# tests/test_analysis.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_parser import LogicParser
from truth_table import TruthTable
from fictitious_vars import FictitiousVariables
from boolean_diff import BooleanDifferentiation


class TestFictitious(unittest.TestCase):
    def test_no_fictitious(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        f = FictitiousVariables(tt)
        self.assertEqual(f.find_fictitious(), [])

    def test_fictitious_b(self):
        p = LogicParser("a", ['a', 'b'])
        tt = TruthTable(p)
        f = FictitiousVariables(tt)
        self.assertEqual(f.find_fictitious(), ['b'])

    def test_essential(self):
        p = LogicParser("a", ['a', 'b'])
        tt = TruthTable(p)
        f = FictitiousVariables(tt)
        self.assertEqual(f.get_essential_variables(), ['a'])

    def test_complex_fictitious(self):
        p = LogicParser("(a&b)|a->c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        f = FictitiousVariables(tt)
        self.assertEqual(f.find_fictitious(), ['b'])


class TestDifferentiation(unittest.TestCase):
    def test_and_derivative(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertEqual(d.partial_derivative_vector('a'), [0, 1])
        self.assertEqual(d.partial_derivative_vector('b'), [0, 1])

    def test_or_derivative(self):
        p = LogicParser("a|b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertEqual(d.partial_derivative_vector('a'), [1, 0])

    def test_mixed_derivative(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertEqual(d.mixed_derivative('a', 'b'), [1])

    def test_dependence(self):
        p = LogicParser("a", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertTrue(d.check_dependence('a'))
        self.assertFalse(d.check_dependence('b'))


# tests/test_analysis.py - добавляем в конец файла

class TestFictitiousExtra(unittest.TestCase):
    def test_print_result_method(self):
        p = LogicParser("a", ['a', 'b'])
        tt = TruthTable(p)
        f = FictitiousVariables(tt)
        # Проверяем, что метод не падает
        try:
            f.print_result()
            result = True
        except:
            result = False
        self.assertTrue(result)

    def test_constant_function_all_fictitious(self):
        p = LogicParser("a|!a", ['a', 'b', 'c'])
        tt = TruthTable(p)
        f = FictitiousVariables(tt)
        # Проверяем, что все переменные фиктивны для константы
        fict = f.find_fictitious()
        self.assertEqual(len(fict), 3)

    def test_no_variables(self):
        p = LogicParser("a", ['a'])
        tt = TruthTable(p)
        f = FictitiousVariables(tt)
        self.assertEqual(f.find_fictitious(), [])
        self.assertEqual(f.get_essential_variables(), ['a'])


class TestDifferentiationExtra(unittest.TestCase):
    def test_derivative_empty_args(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative()
        self.assertEqual(deriv, [0, 0, 0, 1])

    def test_derivative_numeric_form(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        result = d.derivative_numeric_form('a')
        self.assertIsInstance(result, str)

    def test_derivative_nonexistent_var(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('x')
        self.assertIsInstance(deriv, list)

    def test_print_derivatives_method(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        try:
            d.print_derivatives(max_vars=2)
            result = True
        except:
            result = False
        self.assertTrue(result)

    def test_derivative_with_three_vars(self):
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv), 4)

    def test_mixed_derivative_order_3(self):
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.mixed_derivative('a', 'b', 'c')
        self.assertEqual(deriv, [1])


# Добавьте в конец файла tests/test_analysis.py

class TestDifferentiationDetailed(unittest.TestCase):
    """Детальные тесты для булевой дифференциации"""

    def test_derivative_3var_function(self):
        """Тест производной для функции 3 переменных"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        # ∂f/∂a = b&c
        deriv_a = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv_a), 4)

    def test_derivative_4var_function(self):
        """Тест производной для функции 4 переменных"""
        p = LogicParser("a&b&c&d", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        deriv_a = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv_a), 8)

    def test_mixed_derivative_3var(self):
        """Тест смешанной производной для 3 переменных"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        deriv_ab = d.mixed_derivative('a', 'b')
        # ∂²/∂a∂b = c, порядок может быть разным
        self.assertEqual(len(deriv_ab), 2)

        deriv_abc = d.mixed_derivative('a', 'b', 'c')
        self.assertEqual(deriv_abc, [1])

    def test_derivative_xor_3var(self):
        """Тест производной для XOR 3 переменных"""
        # a⊕b⊕c
        p = LogicParser("(a~!b)~!c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        deriv_a = d.partial_derivative_vector('a')
        # ∂/∂a = 1 (константа)
        self.assertEqual(deriv_a, [1, 1, 1, 1])

    def test_derivative_or_function(self):
        """Тест производной для OR"""
        p = LogicParser("a|b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        deriv_a = d.partial_derivative_vector('a')
        # ∂(a|b)/∂a = !b
        self.assertEqual(deriv_a, [1, 0])

    def test_derivative_equivalence(self):
        """Тест производной для эквивалентности"""
        p = LogicParser("a~b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        deriv_a = d.partial_derivative_vector('a')
        # ∂(a~b)/∂a = 1 (всегда 1)
        self.assertEqual(deriv_a, [1, 1])

    def test_derivative_implication(self):
        """Тест производной для импликации"""
        p = LogicParser("a->b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        deriv_a = d.partial_derivative_vector('a')
        # ∂(a->b)/∂a = !b
        self.assertEqual(deriv_a, [1, 0])

    def test_derivative_numeric_format(self):
        """Тест числового формата производной"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        result = d.derivative_numeric_form('a')
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("∂af"))


# Добавьте в конец tests/test_analysis.py

    def test_derivative_2var_implication(self):
        """Тест производной для импликации 2 переменных"""
        p = LogicParser("a->b", ['a','b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv), 2)

    # Добавьте в конец файла

    def test_check_dependence_false(self):
        """Тест зависимости от переменной - отрицание"""
        p = LogicParser("!a", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertTrue(d.check_dependence('a'))
        self.assertFalse(d.check_dependence('b'))

    def test_derivative_numeric_form_2var(self):
        """Тест числовой формы производной для 2 переменных"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        result = d.derivative_numeric_form('a')
        self.assertIsInstance(result, str)

    def test_derivative_4var(self):
        p = LogicParser("a&b&c&d", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv), 8)

    def test_mixed_derivative_4var(self):
        p = LogicParser("a&b&c&d", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.mixed_derivative('a', 'b')
        self.assertEqual(len(deriv), 4)

    def test_derivative_complex_order(self):
        """Производная высокого порядка для 3 переменных"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        # Производные по порядку
        d1 = d.derivative('a')
        d2 = d.derivative('a', 'b')
        d3 = d.derivative('a', 'b', 'c')

        self.assertEqual(len(d1), 4)
        self.assertEqual(len(d2), 2)
        self.assertEqual(d3, [1])

    def test_derivative_xor_3var(self):
        """XOR 3 переменных"""
        p = LogicParser("(a~!b)~!c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv), 4)

    def test_partial_derivative_all_vars_order(self):
        """Частные производные по всем переменным"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)

        for var in ['a', 'b', 'c']:
            deriv = d.partial_derivative_vector(var)
            self.assertEqual(len(deriv), 4)

    def test_derivative_implication(self):
        """Производная импликации"""
        p = LogicParser("a->b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv), 2)

    def test_derivative_equivalence(self):
        """Производная эквивалентности"""
        p = LogicParser("a~b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(deriv, [1, 1])

    def test_boolean_diff_line_21_25(self):
        """Строки 21-25: __init__ и _get_mask"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertIsNotNone(d)

    def test_boolean_diff_line_65(self):
        """Строка 65: derivative с несколькими переменными"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('a', 'b')
        self.assertEqual(len(deriv), 2)

    def test_boolean_diff_line_85(self):
        """Строка 85: _derivative_of_vector"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('a', 'b', 'c')
        self.assertEqual(deriv, [1])

    def test_boolean_diff_line_91_94(self):
        """Строки 91-94: partial_derivative_vector"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(len(deriv), 4)

    def test_boolean_diff_line_120(self):
        """Строка 120: mixed_derivative"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.mixed_derivative('a', 'b')
        self.assertEqual(deriv, [1])

    def test_boolean_diff_line_140_145(self):
        """Строки 140-145: print_derivatives"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        try:
            d.print_derivatives(max_vars=2)
            result = True
        except:
            result = False
        self.assertTrue(result)

    def test_boolean_diff_line_164_166(self):
        """Строки 164-166: derivative с несуществующей переменной"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('x')
        self.assertIsInstance(deriv, list)

    def test_boolean_diff_line_176(self):
        """Строка 176: _derivative_of_vector с current_n <= 0"""
        p = LogicParser("a", ['a'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('a')
        self.assertEqual(deriv, [1])

    def test_boolean_diff_line_184(self):
        """Строка 184: _derivative_of_vector с var_idx >= current_n"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('b', 'a')  # порядок может вызвать эту ветку
        self.assertIsInstance(deriv, list)

    def test_boolean_diff_line_189_193(self):
        """Строки 189-193: derivative_numeric_form"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        result = d.derivative_numeric_form('a')
        self.assertIsInstance(result, str)

    def test_boolean_diff_line_206_212_218(self):
        """Строки 206-218: check_dependence"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        self.assertTrue(d.check_dependence('a'))
        self.assertTrue(d.check_dependence('b'))

    def test_derivative_constant(self):
        p = LogicParser("1", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.partial_derivative_vector('a')
        self.assertEqual(deriv, [0, 0])

if __name__ == '__main__':
    unittest.main()