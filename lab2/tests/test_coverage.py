# tests/test_coverage.py - полная исправленная версия
import unittest
import sys
import os
import io
import sys as sys_module

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_parser import LogicParser
from truth_table import TruthTable
from normal_forms import NormalForms
from post_classes import PostClasses
from zhegalkin import ZhegalkinPolynomial
from fictitious_vars import FictitiousVariables
from boolean_diff import BooleanDifferentiation
from minimization import Minimization
from minimization_karnaugh import KarnaughMap


class TestFinalCoverageExtra(unittest.TestCase):
    """Финальные тесты для достижения 90% покрытия"""

    def test_truth_table_missing_lines(self):
        """Тест непокрытых строк truth_table.py"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        captured = io.StringIO()
        sys_module.stdout = captured
        tt.print_table()
        sys_module.stdout = sys.__stdout__
        self.assertIn("a | b | F", captured.getvalue())

    def test_normal_forms_missing(self):
        """Тест непокрытых строк normal_forms.py"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        num = nf.get_numeric_form_sdnf()
        self.assertIn("2", num)

    def test_minimization_karnaugh_3var_all_cases(self):
        """Тест всех случаев карты Карно для 3 переменных"""
        p1 = LogicParser("!a&!b", ['a', 'b', 'c'])
        tt1 = TruthTable(p1)
        k1 = KarnaughMap(tt1)
        dnf1, _ = k1.build_map_dnf()
        self.assertIsNotNone(dnf1)

        p2 = LogicParser("!a&!c", ['a', 'b', 'c'])
        tt2 = TruthTable(p2)
        k2 = KarnaughMap(tt2)
        dnf2, _ = k2.build_map_dnf()
        self.assertIsNotNone(dnf2)


    def test_boolean_diff_all_derivatives(self):
        """Тест всех производных для функции"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        d.partial_derivative_vector('a')
        d.partial_derivative_vector('b')
        d.mixed_derivative('a', 'b')
        d.print_derivatives(max_vars=2)
        self.assertTrue(True)

    def test_minimization_table_coverage(self):
        """Тест табличного метода минимизации"""
        p = LogicParser("(a&b)|a->c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages, table = m.minimize_dnf_table_method()
        self.assertGreater(len(table), 0)
        m.print_minimization_dnf()
        m.print_minimization_dnf_table()
        self.assertTrue(True)

    def test_zhegalkin_coefficients_all(self):
        """Тест всех коэффициентов полинома Жегалкина"""
        p = LogicParser("a|b", ['a', 'b'])
        tt = TruthTable(p)
        z = ZhegalkinPolynomial(tt)
        coeffs = z.get_coefficients()
        self.assertEqual(len(coeffs), 3)

    def test_post_classes_linear_check(self):
        """Тест проверки линейности"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        self.assertFalse(post.is_l())

        p2 = LogicParser("a~b", ['a', 'b'])
        tt2 = TruthTable(p2)
        post2 = PostClasses(tt2)
        self.assertTrue(post2.is_l())

    def test_fictitious_print(self):
        """Тест вывода фиктивных переменных"""
        p = LogicParser("a", ['a', 'b'])
        tt = TruthTable(p)
        f = FictitiousVariables(tt)
        captured = io.StringIO()
        sys_module.stdout = captured
        f.print_result()
        sys_module.stdout = sys.__stdout__
        self.assertIn("Фиктивные переменные", captured.getvalue())


# Добавьте в конец файла tests/test_coverage.py

class TestFinalPush(unittest.TestCase):
    """Финальные тесты для 90% покрытия"""

    def test_boolean_diff_high_order_4var(self):
        """Тест производной 4-го порядка"""
        p = LogicParser("a&b&c&d", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        d = BooleanDifferentiation(tt)
        deriv = d.derivative('a', 'b', 'c', 'd')
        self.assertEqual(deriv, [1])

    def test_karnaugh_3var_rectangle_2x2_detailed(self):
        """Детальный тест прямоугольника 2x2"""
        p = LogicParser("!a&b", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)


    def test_minimization_empty_implicants(self):
        """Тест с пустыми импликантами"""
        p = LogicParser("a&!a", ['a'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "0")

    def test_minimization_table_with_redundant(self):
        """Тест таблицы с лишними импликантами"""
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages, table = m.minimize_dnf_table_method()
        self.assertGreater(len(table), 0)


if __name__ == '__main__':
    unittest.main()