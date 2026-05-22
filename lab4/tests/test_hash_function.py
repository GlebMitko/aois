# tests/test_hash_function.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hash_function import char_to_num, calculate_v, hash_function


class TestCharToNum(unittest.TestCase):

    def test_a_is_zero(self):
        self.assertEqual(char_to_num('А'), 0)

    def test_b_is_one(self):
        self.assertEqual(char_to_num('Б'), 1)

    def test_ya_is_32(self):
        self.assertEqual(char_to_num('Я'), 32)

    def test_lowercase(self):
        self.assertEqual(char_to_num('а'), 0)

    def test_non_russian_letter(self):
        self.assertEqual(char_to_num('Z'), 0)


class TestCalculateV(unittest.TestCase):

    def test_two_letters(self):
        # В=2, Я=32: 2*33 + 32 = 66 + 32 = 98
        self.assertEqual(calculate_v("ВЯ"), 2 * 33 + 32)

    def test_real_word_vyatkin(self):
        # Вяткин: В=2, Я=32 → 98
        self.assertEqual(calculate_v("Вяткин"), 2 * 33 + 32)

    def test_real_word_tretyak(self):
        # Третьяк: Т=19, Р=17 → 19*33 + 17 = 627 + 17 = 644
        self.assertEqual(calculate_v("Третьяк"), 19 * 33 + 17)

    def test_one_letter(self):
        # А: 0*33 = 0
        self.assertEqual(calculate_v("А"), 0)

    def test_empty_string(self):
        self.assertEqual(calculate_v(""), 0)

    def test_case_insensitive(self):
        self.assertEqual(calculate_v("вяткин"), calculate_v("ВЯТКИН"))


class TestHashFunction(unittest.TestCase):

    def test_hash_vyatkin(self):
        # V=98, size=20: 98 % 20 = 18
        self.assertEqual(hash_function("Вяткин", 20), 98 % 20)

    def test_hash_tretyak(self):
        # V=644, size=20: 644 % 20 = 4
        self.assertEqual(hash_function("Третьяк", 20), 644 % 20)

    def test_hash_with_base(self):
        self.assertEqual(hash_function("Вяткин", 20, 10), 98 % 20 + 10)

    def test_hash_empty(self):
        self.assertEqual(hash_function("", 20), 0)


if __name__ == '__main__':
    unittest.main()