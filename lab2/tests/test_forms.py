# tests/test_forms.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_parser import LogicParser
from truth_table import TruthTable
from normal_forms import NormalForms
from post_classes import PostClasses
from zhegalkin import ZhegalkinPolynomial


class TestNormalForms(unittest.TestCase):
    def test_sdnf_and(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        self.assertEqual(nf.build_sdnf(), "(a&b)")

    def test_sdnf_or(self):
        p = LogicParser("a|b", ['a', 'b'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        self.assertEqual(nf.build_sdnf(), "(!a&b)|(a&!b)|(a&b)")

    def test_sknf_and(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        self.assertEqual(nf.build_sknf(), "(a|b)&(a|!b)&(!a|b)")

    def test_numeric_forms(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        self.assertEqual(nf.get_numeric_form_sdnf(), "2 (3)")
        self.assertEqual(nf.get_numeric_form_sknf(), "2 (0 , 1 , 2)")


class TestPostClasses(unittest.TestCase):
    def test_t0_t1(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        self.assertTrue(post.is_t0())
        self.assertTrue(post.is_t1())

    def test_self_dual(self):
        p = LogicParser("!a", ['a'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        self.assertTrue(post.is_s())

        p2 = LogicParser("a&b", ['a', 'b'])
        tt2 = TruthTable(p2)
        post2 = PostClasses(tt2)
        self.assertFalse(post2.is_s())

    def test_monotone(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        self.assertTrue(post.is_m())

        p2 = LogicParser("!a", ['a'])
        tt2 = TruthTable(p2)
        post2 = PostClasses(tt2)
        self.assertFalse(post2.is_m())

    def test_linear(self):
        p = LogicParser("a~!b", ['a', 'b'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        self.assertTrue(post.is_l())

        p2 = LogicParser("a&b", ['a', 'b'])
        tt2 = TruthTable(p2)
        post2 = PostClasses(tt2)
        self.assertFalse(post2.is_l())


class TestZhegalkin(unittest.TestCase):
    def test_and(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        z = ZhegalkinPolynomial(tt)
        self.assertEqual(z.build(), "a&b")

    def test_not(self):
        p = LogicParser("!a", ['a'])
        tt = TruthTable(p)
        z = ZhegalkinPolynomial(tt)
        self.assertEqual(z.build(), "1 ⊕ a")

    def test_equivalence(self):
        p = LogicParser("a~b", ['a', 'b'])
        tt = TruthTable(p)
        z = ZhegalkinPolynomial(tt)
        poly = z.build()
        self.assertIn("1", poly)
        self.assertIn("a", poly)
        self.assertIn("b", poly)


# tests/test_forms.py - добавляем в конец файла

class TestNormalFormsExtra(unittest.TestCase):
    def test_sdnf_3var_complex(self):
        # Функция большинства: (a&b)|(a&c)|(b&c)
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a','b','c'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        sdnf = nf.build_sdnf()
        # Проверяем, что СДНФ содержит все 4 единичных набора
        self.assertIn("a&b&c", sdnf)
        self.assertIn("a&b&!c", sdnf)
        self.assertIn("a&!b&c", sdnf)
        self.assertIn("!a&b&c", sdnf)

    def test_index_form_several(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        idx = nf.get_index_form()
        self.assertIsInstance(idx, str)

    def test_numeric_form_string(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        num_sdnf = nf.get_numeric_form_sdnf()
        num_sknf = nf.get_numeric_form_sknf()
        self.assertTrue(num_sdnf.startswith("2"))
        self.assertTrue(num_sknf.startswith("2"))


class TestPostClassesExtra(unittest.TestCase):
    def test_t0_false(self):
        p = LogicParser("a|!a", ['a'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        self.assertFalse(post.is_t0())

    def test_t1_false(self):
        p = LogicParser("a&!a", ['a'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        self.assertFalse(post.is_t1())

    def test_self_dual_xor(self):
        # XOR для 2 переменных не самодвойственен
        p = LogicParser("a~!b", ['a', 'b'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        self.assertFalse(post.is_s())

    def test_monotone_check(self):
        p = LogicParser("a->b", ['a', 'b'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        # импликация не монотонна
        self.assertFalse(post.is_m())

    def test_linear_equivalence(self):
        p = LogicParser("a~b", ['a', 'b'])
        tt = TruthTable(p)
        post = PostClasses(tt)
        # эквивалентность линейна: 1⊕a⊕b
        self.assertTrue(post.is_l())


class TestZhegalkinExtra(unittest.TestCase):
    def test_or_polynomial_full(self):
        p = LogicParser("a|b", ['a', 'b'])
        tt = TruthTable(p)
        z = ZhegalkinPolynomial(tt)
        poly = z.build()
        self.assertIn("a", poly)
        self.assertIn("b", poly)
        self.assertIn("a&b", poly)

    def test_coefficients_dict(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        z = ZhegalkinPolynomial(tt)
        coeffs = z.get_coefficients()
        self.assertEqual(len(coeffs), 1)
        self.assertIn("a&b", coeffs)

    def test_xor_polynomial(self):
        p = LogicParser("(a&!b)|(!a&b)", ['a', 'b'])
        tt = TruthTable(p)
        z = ZhegalkinPolynomial(tt)
        poly = z.build()
        self.assertIn("a", poly)
        self.assertIn("b", poly)

    def test_sdnf_3var_majority(self):
        """Тест СДНФ для мажоритарной функции"""
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        sdnf = nf.build_sdnf()
        self.assertIn("a&b&c", sdnf)

    def test_sknf_3var_majority(self):
        """Тест СКНФ для мажоритарной функции"""
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        sknf = nf.build_sknf()
        self.assertIsNotNone(sknf)

    def test_index_form_constant(self):
        p = LogicParser("1", ['a'])
        tt = TruthTable(p)
        nf = NormalForms(tt)
        idx = nf.get_index_form()
        self.assertIsInstance(idx, str)

if __name__ == '__main__':
    unittest.main()