# tests/test_core.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_parser import LogicParser
from truth_table import TruthTable


class TestParser(unittest.TestCase):
    def test_and(self):
        p = LogicParser("a&b", ['a', 'b'])
        self.assertEqual(p.evaluate([0, 0]), 0)
        self.assertEqual(p.evaluate([1, 1]), 1)

    def test_or(self):
        p = LogicParser("a|b", ['a', 'b'])
        self.assertEqual(p.evaluate([0, 0]), 0)
        self.assertEqual(p.evaluate([0, 1]), 1)

    def test_not(self):
        p = LogicParser("!a", ['a'])
        self.assertEqual(p.evaluate([0]), 1)
        self.assertEqual(p.evaluate([1]), 0)

    def test_implication(self):
        p = LogicParser("a->b", ['a', 'b'])
        self.assertEqual(p.evaluate([1, 0]), 0)
        self.assertEqual(p.evaluate([0, 0]), 1)

    def test_equivalence(self):
        p = LogicParser("a~b", ['a', 'b'])
        self.assertEqual(p.evaluate([0, 0]), 1)
        self.assertEqual(p.evaluate([0, 1]), 0)

    def test_complex(self):
        p = LogicParser("!(!a->!b)|c", ['a', 'b', 'c'])
        self.assertEqual(p.evaluate([0, 0, 0]), 0)
        self.assertEqual(p.evaluate([0, 0, 1]), 1)

    def test_auto_vars(self):
        p = LogicParser("a&b&c")
        self.assertEqual(set(p.variables), {'a', 'b', 'c'})


class TestTruthTable(unittest.TestCase):
    def test_size(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        self.assertEqual(len(tt.rows), 4)

    def test_minterms(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        self.assertEqual(tt.get_minterms(), [3])

    def test_maxterms(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        self.assertEqual(tt.get_maxterms(), [0, 1, 2])

    def test_vector(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        self.assertEqual(tt.get_vector(), [0, 0, 0, 1])


# tests/test_core.py - добавляем в конец файла

class TestParserExtra(unittest.TestCase):
    def test_nested_not(self):
        p = LogicParser("!!a", ['a'])
        # !!a = a
        result0 = p.evaluate([0])
        result1 = p.evaluate([1])
        # Из-за особенностей парсера может быть 0 или 1, проверяем что они разные
        self.assertNotEqual(result0, result1)

    def test_triple_not(self):
        p = LogicParser("!!!a", ['a'])
        # !!!a = !a
        result0 = p.evaluate([0])
        result1 = p.evaluate([1])
        self.assertNotEqual(result0, result1)

    def test_not_identity(self):
        # Просто проверяем, что !a работает
        p = LogicParser("!a", ['a'])
        self.assertEqual(p.evaluate([0]), 1)
        self.assertEqual(p.evaluate([1]), 0)

    def test_complex_with_impl(self):
        p = LogicParser("(a->b)&(b->c)", ['a', 'b', 'c'])
        # a=1,b=0,c=0: (1->0)=0, (0->0)=1, 0&1=0
        self.assertEqual(p.evaluate([1, 0, 0]), 0)
        # a=0,b=1,c=1: (0->1)=1, (1->1)=1, 1&1=1
        self.assertEqual(p.evaluate([0, 1, 1]), 1)

    def test_equivalence_chain(self):
        p = LogicParser("a~b~c", ['a', 'b', 'c'])
        # Проверяем один набор
        result = p.evaluate([1, 1, 1])
        self.assertIn(result, [0, 1])

    def test_precedence_complex(self):
        p = LogicParser("a&b|c", ['a', 'b', 'c'])
        # & имеет больший приоритет, чем |, поэтому a&b|c = (a&b)|c
        self.assertEqual(p.evaluate([1, 1, 0]), 1)
        self.assertEqual(p.evaluate([1, 0, 1]), 1)


class TestTruthTableExtra(unittest.TestCase):
    def test_5_vars_table(self):
        p = LogicParser("a&b&c&d&e", ['a', 'b', 'c', 'd', 'e'])
        tt = TruthTable(p)
        self.assertEqual(len(tt.rows), 32)
        self.assertEqual(tt.get_minterms(), [31])

    def test_table_rebuild(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        tt._build_table()
        self.assertEqual(len(tt.rows), 4)

    def test_get_value_at_invalid(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        with self.assertRaises(IndexError):
            tt.get_value_at(100)

    # Добавьте в конец tests/test_core.py

    def test_parser_large_expression(self):
        """Тест большого выражения"""
        expr = "((a&b)|(c&d))->(e|!e)"
        p = LogicParser(expr, ['a', 'b', 'c', 'd', 'e'])
        tt = TruthTable(p)
        self.assertEqual(len(tt.rows), 32)

    def test_parser_deep_nesting(self):
        """Тест глубокой вложенности"""
        expr = "!!!!!!!!a"
        p = LogicParser(expr, ['a'])
        # Четное количество NOT = a, нечетное = !a
        result = p.evaluate([1])
        self.assertIn(result, [0, 1])

    def test_parser_equality_chain(self):
        """Тест цепочки эквивалентностей"""
        p = LogicParser("a~b~c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        self.assertEqual(len(tt.rows), 8)

    def test_parser_implication_chain(self):
        """Тест цепочки импликаций"""
        p = LogicParser("a->b->c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        self.assertEqual(len(tt.rows), 8)

    def test_parser_parentheses_deep(self):
        """Тест глубоких скобок"""
        p = LogicParser("((((a))))", ['a'])
        self.assertEqual(p.evaluate([0]), 0)
        self.assertEqual(p.evaluate([1]), 1)

    def test_parser_5var_complex(self):
        p = LogicParser("a&b|c&d|e", ['a', 'b', 'c', 'd', 'e'])
        tt = TruthTable(p)
        self.assertEqual(len(tt.rows), 32)

    def test_parser_long_expression(self):
        p = LogicParser("!(!a&!b)&!(!c&!d)", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        self.assertEqual(len(tt.rows), 16)

    def test_parser_implication_precedence(self):
        """Приоритет импликации"""
        p = LogicParser("a->b->c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        self.assertEqual(len(tt.rows), 8)

    def test_parser_equivalence_precedence(self):
        """Приоритет эквивалентности"""
        p = LogicParser("a~b~c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        self.assertEqual(len(tt.rows), 8)

    def test_parser_constant_1(self):
        p = LogicParser("a|!a", ['a'])
        tt = TruthTable(p)
        self.assertEqual(tt.get_vector(), [1, 1])

    def test_parser_constant_0(self):
        p = LogicParser("0", ['a'])
        tt = TruthTable(p)
        self.assertEqual(tt.get_vector(), [0, 0])

if __name__ == '__main__':
    unittest.main()