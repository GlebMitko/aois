# tests/test_part3_counter.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from part3_counter_up8 import UpCounter8


class TestUpCounter8(unittest.TestCase):

    def setUp(self):
        self.counter = UpCounter8()

    def test_next_state(self):
        """Проверка переходов состояний"""
        # 0 -> 1
        self.assertEqual(self.counter.next_state(0, 0, 0), (0, 0, 1))
        # 1 -> 2
        self.assertEqual(self.counter.next_state(0, 0, 1), (0, 1, 0))
        # 2 -> 3
        self.assertEqual(self.counter.next_state(0, 1, 0), (0, 1, 1))
        # 3 -> 4
        self.assertEqual(self.counter.next_state(0, 1, 1), (1, 0, 0))
        # 4 -> 5
        self.assertEqual(self.counter.next_state(1, 0, 0), (1, 0, 1))
        # 5 -> 6
        self.assertEqual(self.counter.next_state(1, 0, 1), (1, 1, 0))
        # 6 -> 7
        self.assertEqual(self.counter.next_state(1, 1, 0), (1, 1, 1))
        # 7 -> 0
        self.assertEqual(self.counter.next_state(1, 1, 1), (0, 0, 0))

    def test_t_input(self):
        """Проверка функции возбуждения T-триггера"""
        # Q=0, Q_next=0 -> T=0
        self.assertEqual(self.counter.t_input(0, 0), 0)
        # Q=0, Q_next=1 -> T=1
        self.assertEqual(self.counter.t_input(0, 1), 1)
        # Q=1, Q_next=0 -> T=1
        self.assertEqual(self.counter.t_input(1, 0), 1)
        # Q=1, Q_next=1 -> T=0
        self.assertEqual(self.counter.t_input(1, 1), 0)

    def test_truth_table_rows_count(self):
        """Таблица переходов должна содержать 8 строк (2^3)"""
        rows = self.counter.truth_table()
        self.assertEqual(len(rows), 8)

    def test_t0_values(self):
        """T0 всегда 1 для всех состояний"""
        rows = self.counter.truth_table()
        for row in rows:
            self.assertEqual(row['T0'], 1)

    def test_t1_values(self):
        """T1 = Q0"""
        rows = self.counter.truth_table()
        for row in rows:
            self.assertEqual(row['T1'], row['Q0'])

    def test_t2_values(self):
        """T2 = Q0 & Q1"""
        rows = self.counter.truth_table()
        for row in rows:
            expected = row['Q0'] & row['Q1']
            self.assertEqual(row['T2'], expected)

    def test_get_logisim_description(self):
        """Проверка описания для Logisim"""
        desc = self.counter.get_logisim_description()
        self.assertIsInstance(desc, str)
        self.assertIn("СЧЕТЧИК", desc.upper())
        self.assertIn("T2", desc)
        self.assertIn("T1", desc)
        self.assertIn("T0", desc)

    def test_print_info(self):
        """Тест вывода информации (не падает)"""
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        self.counter.print_info()
        sys.stdout = sys.__stdout__
        self.assertIn("T2", captured.getvalue())

    def test_to_not_and_or_method(self):
        """Тест метода преобразования в базис НЕ-И-ИЛИ"""
        # Метод называется _to_not_and_or (с подчеркиванием) в классе UpCounter8
        # Проверяем что он работает через публичный метод print_info
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        self.counter.print_info()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        # Проверяем что в выводе есть преобразование в базис НЕ-И-ИЛИ
        self.assertIn("НЕ-И-ИЛИ", output)


if __name__ == '__main__':
    unittest.main()