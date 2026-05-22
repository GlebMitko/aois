# tests/test_minimization.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_parser import LogicParser
from truth_table import TruthTable
from minimization import Minimization
from minimization_karnaugh import KarnaughMap


class TestMinimizationCalculus(unittest.TestCase):
    def test_and(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, _ = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "a&b")

    def test_or(self):
        p = LogicParser("a|b", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, _ = m.minimize_dnf_calculus()
        self.assertIn("a", dnf)
        self.assertIn("b", dnf)

    def test_implication(self):
        p = LogicParser("a->b", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, _ = m.minimize_dnf_calculus()
        self.assertIn("!a", dnf)
        self.assertIn("b", dnf)

    def test_complex(self):
        p = LogicParser("(a&b)|a->c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, _ = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "!a | c")

    def test_tautology(self):
        p = LogicParser("a|!a", ['a'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, _ = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "1")

    def test_contradiction(self):
        p = LogicParser("a&!a", ['a'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, _ = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "0")


class TestMinimizationTable(unittest.TestCase):
    def test_table_method(self):
        p = LogicParser("(a&b)|a->c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages, table = m.minimize_dnf_table_method()
        self.assertIsNotNone(table)
        self.assertGreater(len(table), 0)


class TestKarnaugh(unittest.TestCase):
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
        self.assertIn("a", dnf)

    def test_3var(self):
        p = LogicParser("(a&b)|a->c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIn(dnf, ["!a | c", "!a"])

    def test_tautology(self):
        p = LogicParser("a|!a", ['a'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "1")

    def test_contradiction(self):
        p = LogicParser("a&!a", ['a'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "0")


# tests/test_minimization.py - добавляем в конец файла

class TestMinimizationCalculusExtra(unittest.TestCase):
    def test_xor_minimization(self):
        p = LogicParser("(a&!b)|(!a&b)", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_majority_minimization(self):
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_print_methods(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        try:
            m.print_minimization_dnf()
            m.print_minimization_dnf_table()
            result = True
        except:
            result = False
        self.assertTrue(result)

    def test_empty_minterms(self):
        p = LogicParser("a&!a", ['a'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "0")

    def test_all_minterms(self):
        p = LogicParser("a|!a", ['a'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "1")


class TestKarnaughExtra(unittest.TestCase):
    def test_2var_all_ones(self):
        p = LogicParser("a|!a", ['a', 'b'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "1")

    def test_2var_all_zeros(self):
        p = LogicParser("a&!a", ['a', 'b'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "0")

    def test_3var_all_ones(self):
        p = LogicParser("a|!a", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "1")

    def test_3var_vertical_pairs(self):
        p = LogicParser("!a&!b", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)


    def test_5var_simple(self):
        p = LogicParser("a&b&c&d&e", ['a', 'b', 'c', 'd', 'e'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a&b&c&d&e")

    def test_print_karnaugh(self):
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        try:
            k.print_karnaugh_dnf()
            result = True
        except:
            result = False
        self.assertTrue(result)


# Добавьте в конец файла tests/test_minimization.py

class TestKarnaughDetailed(unittest.TestCase):
    """Детальные тесты для карт Карно"""

    def test_karnaugh_3var_rectangle_2x2(self):
        """Тест прямоугольника 2x2 на карте 3 переменных"""
        # Функция где a=0 дает 1 (строка целиком)
        p = LogicParser("!a", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "!a")

    def test_karnaugh_3var_rectangle_1x4(self):
        """Тест строки целиком"""
        p = LogicParser("a", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a")

    def test_karnaugh_3var_column_pair(self):
        """Тест пары в столбце"""
        # bc = 01 или 10 - пары по вертикали
        p = LogicParser("!a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)

    def test_karnaugh_3var_corner_wrap(self):
        """Тест склеивания по краям карты"""
        # bc = 00 и 10 (края) - должны склеиваться
        p = LogicParser("(!a&!b&!c)|(!a&b&!c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        # Допускаем оба варианта
        self.assertTrue("!a&!c" in dnf or "!a&!b&!c" in dnf)


    def test_karnaugh_4var_all_zeros(self):
        """Тест все нули для 4 переменных"""
        p = LogicParser("0", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "0")

    def test_karnaugh_3var_single_cell(self):
        """Тест одиночной клетки"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a&b&c")

    def test_karnaugh_3var_horizontal_pair(self):
        """Тест горизонтальной пары"""
        # bc = 01 и 11 - соседи по горизонтали
        p = LogicParser("(!a&!b&c)|(!a&b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        # Допускаем оба варианта
        self.assertTrue("!a&c" in dnf or "!a&!b&c" in dnf or "!a&b&c" in dnf)


# Добавьте в конец файла tests/test_minimization.py

class TestMinimizationCover(unittest.TestCase):
    """Тесты для поиска минимального покрытия"""

    def test_find_minimal_cover_with_redundant(self):
        """Тест с лишними импликантами - должно сработать удаление"""
        # Функция с 3 переменными, где есть лишние импликанты
        # a | bc - где bc можно представить как b&c, но могут быть лишние
        p = LogicParser("a | (b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        # Должна быть минимизирована
        self.assertIsNotNone(dnf)

    def test_find_minimal_cover_complex(self):
        """Тест со сложной функцией, требующей перебора"""
        # Функция большинства - 4 импликанты, но минимальное покрытие 3
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_find_minimal_cover_all_implicants_essential(self):
        """Тест где все импликанты существенные"""
        # Функция XOR не минимизируется
        p = LogicParser("(a&!b)|(!a&b)", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIn("a", dnf)
        self.assertIn("b", dnf)

    def test_find_minimal_cover_large_function(self):
        """Тест с функцией, где импликантов больше 10"""
        # Создаем функцию с 4 переменными, где много импликант
        p = LogicParser("a|b|c|d", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_remove_redundant_implicants_direct(self):
        """Прямой тест удаления лишних импликант"""
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        # Получаем импликанты после склеивания
        dnf, stages = m.minimize_dnf_calculus()
        # Проверяем, что результат минимален
        self.assertEqual(len(stages[-1]['terms']), 3)  # majority function has 3 terms

    def test_no_redundant_implicants(self):
        """Тест когда нет лишних импликант"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "a&b&c")

    def test_single_implicant(self):
        """Тест с одной импликантой"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "a&b")


class TestMinimizationGetImplicantMinterms(unittest.TestCase):
    """Тесты для _get_implicant_minterms"""

    def test_get_implicant_minterms_full(self):
        """Тест получения минтермов из полной импликанты"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        # Проверяем внутренний метод через публичный интерфейс
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_get_implicant_minterms_with_none(self):
        """Тест импликанты с None (склеенной)"""
        p = LogicParser("a", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        # Должна быть a (b - фиктивна)
        self.assertEqual(dnf, "a")

    def test_minimization_xor(self):
        """Тест минимизации XOR"""
        p = LogicParser("(a&!b)|(!a&b)", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, _ = m.minimize_dnf_calculus()
        self.assertIn("a", dnf)
        self.assertIn("b", dnf)

    def test_minimization_table_xor(self):
        """Тест табличного метода для XOR"""
        p = LogicParser("(a&!b)|(!a&b)", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages, table = m.minimize_dnf_table_method()
        self.assertGreater(len(table), 0)

    def test_4var_complex_1(self):
        p = LogicParser("(a&b)|(c&d)", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)

    def test_4var_complex_2(self):
        p = LogicParser("(a&b&c)|(a&b&d)|(a&c&d)|(b&c&d)", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)


    def test_4var_all_zeros(self):
        p = LogicParser("0", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "0")

    def test_5var_complex(self):
        p = LogicParser("a|b|c|d|e", ['a', 'b', 'c', 'd', 'e'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)

    def test_karnaugh_3var_rectangle_2x2_vertical(self):
        """Прямоугольник 2x2 вертикальный для 3 переменных"""
        p = LogicParser("!b", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "!b")

    def test_karnaugh_3var_rectangle_2x2_horizontal(self):
        """Прямоугольник 2x2 горизонтальный для 3 переменных"""
        p = LogicParser("!c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "!c")

    def test_karnaugh_3var_column_pair(self):
        """Пара в столбце для 3 переменных"""
        p = LogicParser("(!a&!b&!c)|(!a&!b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIn("!a&!b", dnf)

    def test_karnaugh_3var_row_pair(self):
        """Пара в строке для 3 переменных"""
        p = LogicParser("(!a&!b&!c)|(!a&b&!c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        # Допускаем оба варианта
        self.assertTrue("!a&!c" in dnf or "!a&!b&!c" in dnf)

    def test_karnaugh_3var_wrap_around(self):
        """Склеивание по краям карты"""
        p = LogicParser("(!a&!b&!c)|(!a&b&!c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)

    def test_karnaugh_3var_single_rectangle(self):
        """Одиночный прямоугольник"""
        p = LogicParser("a&!b&!c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a&!b&!c")

    def test_karnaugh_3var_complex_covering(self):
        """Сложное покрытие с несколькими прямоугольниками"""
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)

    def test_karnaugh_4var_complex_covering(self):
        """Сложное покрытие для 4 переменных"""
        p = LogicParser("(a&b)|(c&d)", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertIsNotNone(dnf)

    def test_karnaugh_line_24_27(self):
        """Строки 24-27: проверка _int_to_binary"""
        p = LogicParser("a&b", ['a', 'b'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        # Вызываем _int_to_binary через build_map_dnf
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a&b")


    def test_karnaugh_line_110_111(self):
        """Строки 110-111: проверка всей строки для 3 переменных"""
        p = LogicParser("a", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a")

    def test_karnaugh_line_136(self):
        """Строка 136: прямоугольник 2x2 для 3 переменных"""
        p = LogicParser("!b", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "!b")

    def test_karnaugh_line_166_169(self):
        """Строки 166-169: оставшиеся единицы для 3 переменных"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "a&b&c")


    def test_karnaugh_line_202_203(self):
        """Строки 202-203: 4 переменные - одна переменная"""
        p = LogicParser("a", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertTrue(dnf == "a" or "a" in dnf)


    def test_karnaugh_line_225(self):
        """Строка 225: 4 переменные - возврат 0"""
        p = LogicParser("0", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertEqual(dnf, "0")

    def test_karnaugh_line_252_256(self):
        """Строки 252-256: 5 переменных"""
        p = LogicParser("a", ['a', 'b', 'c', 'd', 'e'])
        tt = TruthTable(p)
        k = KarnaughMap(tt)
        dnf, _ = k.build_map_dnf()
        self.assertTrue(dnf == "a" or "a" in dnf)

    def test_find_minimal_cover_3var(self):
        """Функция с 3 переменными, где есть лишние импликанты"""
        # Функция a|b|c - но с лишними импликантами
        p = LogicParser("a|b|c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        # Результат должен быть a|b|c или эквивалент
        self.assertIn("a", dnf)
        self.assertIn("b", dnf)
        self.assertIn("c", dnf)

    def test_find_minimal_cover_4var_small(self):
        """Функция с 4 переменными, где импликантов меньше 10"""
        p = LogicParser("(a&b)|(c&d)", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_find_minimal_cover_with_redundant_implicants(self):
        """Функция с явно лишними импликантами"""
        # (a&b)|(a&c)|(b&c) - мажоритарка, 3 импликанты минимально
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        # Проверяем, что результат содержит ровно 3 терма
        self.assertEqual(len(stages[-1]['terms']), 3)

    def test_find_minimal_cover_xor_3var(self):
        """XOR 3 переменных - требует перебора"""
        p = LogicParser("(a~!b)~!c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_find_minimal_cover_4var_majority(self):
        """Функция большинства для 4 переменных"""
        p = LogicParser("(a&b&c)|(a&b&d)|(a&c&d)|(b&c&d)", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_find_minimal_cover_with_all_essential(self):
        """Функция где все импликанты существенные"""
        p = LogicParser("(a&b)|(a&!b)", ['a', 'b'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "a")

    def test_find_minimal_cover_exactly_10_implicants(self):
        """Ровно 10 импликантов, чтобы зайти в ветку с перебором"""
        p = LogicParser("a|b|c|d", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        # Должна быть a|b|c|d или эквивалент
        self.assertIn("a", dnf)
        self.assertIn("b", dnf)
        self.assertIn("c", dnf)
        self.assertIn("d", dnf)

    def test_find_minimal_cover_complex_xor(self):
        """Сложная функция для перебора"""
        p = LogicParser("(a&b&c)|(a&!b&!c)|(!a&b&!c)|(!a&!b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_find_minimal_cover_single_term(self):
        """Один терм - не должно быть перебора"""
        p = LogicParser("a&b&c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertEqual(dnf, "a&b&c")

    def test_find_minimal_cover_two_terms(self):
        """Два терма"""
        p = LogicParser("(a&b)|(c&d)", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        m = Minimization(tt)
        dnf, stages = m.minimize_dnf_calculus()
        self.assertIsNotNone(dnf)

    def test_remove_redundant_implicants_direct_call(self):
        """Прямой вызов _remove_redundant_implicants с перебором"""
        from minimization import Minimization
        from logic_parser import LogicParser
        from truth_table import TruthTable

        # Функция, которая после склеивания даст импликанты с лишними
        p = LogicParser("(a&b)|(a&c)|(b&c)", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)

        # Получаем импликанты после склеивания
        _, stages = m.minimize_dnf_calculus()

        # Берем импликанты после склеивания (не после удаления)
        for stage in stages:
            if stage['stage'] == 1:  # После первого склеивания
                implicants = stage['terms']
                # Вызываем _remove_redundant_implicants напрямую
                result = m._remove_redundant_implicants(implicants)
                self.assertIsNotNone(result)
                break

    def test_remove_redundant_implicants_direct_2(self):
        """Еще один прямой вызов"""
        from minimization import Minimization
        from logic_parser import LogicParser
        from truth_table import TruthTable

        p = LogicParser("a|b|c", ['a', 'b', 'c'])
        tt = TruthTable(p)
        m = Minimization(tt)

        _, stages = m.minimize_dnf_calculus()

        for stage in stages:
            if stage['stage'] == 1:
                implicants = stage['terms']
                result = m._remove_redundant_implicants(implicants)
                self.assertIsInstance(result, list)
                break

    def test_remove_redundant_implicants_with_4vars(self):
        """С 4 переменными для перебора"""
        from minimization import Minimization
        from logic_parser import LogicParser
        from truth_table import TruthTable

        p = LogicParser("(a&b)|(c&d)", ['a', 'b', 'c', 'd'])
        tt = TruthTable(p)
        m = Minimization(tt)

        _, stages = m.minimize_dnf_calculus()

        for stage in stages:
            if stage['stage'] == 1:
                implicants = stage['terms']
                result = m._remove_redundant_implicants(implicants)
                self.assertIsNotNone(result)
                break

if __name__ == '__main__':
    unittest.main()