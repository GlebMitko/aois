# tests/test_karnaugh_and_coverage.py
import unittest
import sys
import os
import io

# Добавляем корневую директорию проекта в пути для импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_parser import LogicParser
from truth_table import TruthTable
from minimization_karnaugh import KarnaughMap
from normal_forms import NormalForms
from post_classes import PostClasses
from boolean_diff import BooleanDifferentiation
from minimization import Minimization


class TestCheatingKarnaughFix(unittest.TestCase):
    """Тестирование независимой геометрической логики карт Карно"""

    def test_karnaugh_trivial_zero(self):
        """Проверка тривиального случая: тождественный 0"""
        p = LogicParser("a & !a", ['a'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf_res, _ = k.minimize_dnf()
        cnf_res, _ = k.minimize_cnf()
        self.assertEqual(dnf_res, "0")
        self.assertEqual(cnf_res, "0")

    def test_karnaugh_trivial_one(self):
        """Проверка тривиального случая: тождественная 1"""
        p = LogicParser("a | !a", ['a'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf_res, _ = k.minimize_dnf()
        cnf_res, _ = k.minimize_cnf()
        self.assertEqual(dnf_res, "1")
        self.assertEqual(cnf_res, "1")

    def test_karnaugh_1_variable(self):
        """Карта Карно для 1 переменной"""
        p = LogicParser("a", ['a'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf_res, _ = k.minimize_dnf()
        cnf_res, _ = k.minimize_cnf()
        self.assertEqual(dnf_res, "a")
        self.assertEqual(cnf_res, "a")

    def test_karnaugh_2_variables(self):
        """Карта Карно для 2 переменных"""
        p = LogicParser("a & b | a & !b", ['a', 'b'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf_res, _ = k.minimize_dnf()
        self.assertEqual(dnf_res, "a")

    def test_karnaugh_3_variables_torus(self):
        """Проверка склейки через края (тор) для 3 переменных (левый и правый край)"""
        p = LogicParser("!a & !b & !c | !a & b & !c", ['a', 'b', 'c'])  # минтермы 0 и 2
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf_res, _ = k.minimize_dnf()
        self.assertIn("!a", dnf_res)
        self.assertIn("!c", dnf_res)

    def test_karnaugh_4_variables_corners(self):
        """Проверка склейки 4 угловых ячеек на карте 4х4 в один квартет"""
        p = LogicParser("!a&!b&!c&!d | !a&!b&c&!d | a&!b&!c&!d | a&!b&c&!d", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf_res, _ = k.minimize_dnf()
        self.assertIn("!b", dnf_res)
        self.assertIn("!d", dnf_res)

    def test_karnaugh_5_variables_layers(self):
        """Проверка работы 3D переходов между слоями для 5 переменных"""
        p = LogicParser("a & b & c & d & e", ['a', 'b', 'c', 'd', 'e'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf_res, _ = k.minimize_dnf()
        self.assertEqual(dnf_res, "a&b&c&d&e")

    def test_karnaugh_visual_prints(self):
        """Покрытие методов печати карт Карно в консоль (print_karnaugh_dnf/cnf)"""
        p = LogicParser("((a->!b)->c)|((a->!b)->c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)

        captured = io.StringIO()
        sys.stdout = captured
        k.print_karnaugh_dnf()
        k.print_karnaugh_cnf()
        sys.stdout = sys.__stdout__
        self.assertIn("Карта Карно", captured.getvalue())


class TestDeepCoverageEdgeCases(unittest.TestCase):
    """Покрытие скрытых веток и условных операторов в остальных модулях"""

    def test_logic_parser_multiple_negations(self):
        """Покрытие парсера на сложных цепочках отрицаний и пустых стеков"""
        p = LogicParser("!!!!a", ['a'])
        self.assertEqual(p.evaluate([1]), 1)

        # Симулируем пустой стек для унарного/бинарного оператора
        p.postfix = ['!']
        self.assertEqual(p.evaluate([1]), 0)
        p.postfix = ['&']
        self.assertEqual(p.evaluate([1]), 0)

    def test_normal_forms_empty_and_full(self):
        """Краевые формы для NormalForms (когда функция — константа)"""
        p_zero = LogicParser("a & !a", ['a'])
        tt_zero = TruthTable(p_zero)
        nf_zero = NormalForms(tt_zero)
        self.assertEqual(nf_zero.build_sdnf(), "0")

        p_one = LogicParser("a | !a", ['a'])
        tt_one = TruthTable(p_one)
        nf_one = NormalForms(tt_one)
        self.assertEqual(nf_one.build_sknf(), "1")
        self.assertIsInstance(nf_one.get_numeric_form_sknf(), str)
        self.assertIsInstance(nf_one.get_index_form(), str)

    def test_post_classes_coverage(self):
        """Полное покрытие методов монотонности и линейности в классах Поста"""
        p = LogicParser("a | b", ['a', 'b'])
        tt = TruthTable(p)
        pc = PostClasses(tt)
        classes = pc.get_classes()
        self.assertTrue(classes['M'])

        captured = io.StringIO()
        sys.stdout = captured
        pc.print_classes()
        sys.stdout = sys.__stdout__
        self.assertIn("Классы Поста", captured.getvalue())

    def test_boolean_differentiation_high_orders(self):
        """Покрытие смешанных производных высокого порядка (2-го и 3-го)"""
        p = LogicParser("a & b & c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        bd = BooleanDifferentiation(tt)

        diff_2 = bd.mixed_derivative('a', 'b')
        self.assertEqual(diff_2, "c")

        captured = io.StringIO()
        sys.stdout = captured
        bd.print_derivatives()
        sys.stdout = sys.__stdout__
        self.assertIn("БУЛЕВА ДИФФЕРЕНЦИАЦИЯ", captured.getvalue())

    def test_minimization_calculus_coverage(self):
        """Покрытие расчетно-табличных методов Квайна-Маккласки из minimization.py"""
        p = LogicParser("a | b", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)

        captured = io.StringIO()
        sys.stdout = captured
        m.print_minimization_dnf_calculus()
        m.print_minimization_dnf_table()
        m.print_minimization_cnf_calculus()
        m.print_minimization_cnf_table()
        sys.stdout = sys.__stdout__
        self.assertIn("Результат", captured.getvalue())

    def test_truth_table_edge(self):
        """Покрытие исключений в truth_table.py"""
        p = LogicParser("a", ['a'])
        tt = TruthTable(p)
        with self.assertRaises(IndexError):
            tt.get_value_at(99)
        self.assertIsInstance(tt.get_binary_string(), str)


if __name__ == '__main__':
    unittest.main()