# truth_table.py
"""Построение таблицы истинности"""

import itertools
from logic_parser import LogicParser


class TruthTable:
    """Таблица истинности логической функции"""

    def __init__(self, parser: LogicParser):
        """
        Инициализация таблицы истинности

        Args:
            parser: экземпляр LogicParser
        """
        self.parser = parser
        self.variables = parser.variables
        self.var_count = len(self.variables)
        self.rows = []
        self._build_table()

    def _build_table(self):
        """Построение таблицы истинности"""
        self.rows = []
        for bits in itertools.product([0, 1], repeat=self.var_count):
            result = self.parser.evaluate(list(bits))
            self.rows.append({
                'values': list(bits),
                'result': result
            })

    def get_minterms(self) -> list:
        """Возвращает номера наборов, где функция = 1"""
        return [i for i, row in enumerate(self.rows) if row['result'] == 1]

    def get_maxterms(self) -> list:
        """Возвращает номера наборов, где функция = 0"""
        return [i for i, row in enumerate(self.rows) if row['result'] == 0]

    def get_vector(self) -> list:
        """Возвращает вектор функции (столбец значений)"""
        return [row['result'] for row in self.rows]

    def get_value_at(self, index: int) -> int:
        """Возвращает значение функции на наборе с заданным индексом"""
        if 0 <= index < len(self.rows):
            return self.rows[index]['result']
        raise IndexError("Индекс вне диапазона")

    def get_binary_string(self) -> str:
        """Возвращает вектор функции в виде строки из 0 и 1"""
        return ''.join(str(row['result']) for row in self.rows)

    def print_table(self):
        """Вывод таблицы истинности"""
        print("Таблица истинности:")
        header = self.variables + ['F']
        print(" | ".join(header))
        print("-" * (len(header) * 4 - 2))
        for i, row in enumerate(self.rows):
            values = [str(v) for v in row['values']] + [str(row['result'])]
            print(f"{i:2d}: " + " | ".join(values))