# normal_forms.py
"""Построение СДНФ и СКНФ, числовые формы"""

from truth_table import TruthTable


class NormalForms:
    """Класс для работы с нормальными формами"""

    def __init__(self, truth_table: TruthTable):
        self.tt = truth_table
        self.variables = truth_table.variables

    def _int_to_binary(self, n: int, width: int) -> list:
        """Преобразует число в бинарный список фиксированной ширины"""
        return [int(x) for x in format(n, f'0{width}b')]

    def _get_literal(self, var: str, value: int) -> str:
        """Возвращает литерал (переменную или её отрицание)"""
        if value == 1:
            return var
        return f"!{var}"

    def build_sdnf(self) -> str:
        """Построение СДНФ"""
        minterms = self.tt.get_minterms()
        if not minterms:
            return "0"

        terms = []
        for idx in minterms:
            values = self._int_to_binary(idx, len(self.variables))
            literals = [self._get_literal(self.variables[i], values[i])
                        for i in range(len(self.variables))]
            terms.append(f"({'&'.join(literals)})")

        return '|'.join(terms)

    def build_sknf(self) -> str:
        """Построение СКНФ"""
        maxterms = self.tt.get_maxterms()
        if not maxterms:
            return "1"

        terms = []
        for idx in maxterms:
            values = self._int_to_binary(idx, len(self.variables))
            literals = [self._get_literal(self.variables[i], 1 - values[i])
                        for i in range(len(self.variables))]
            terms.append(f"({'|'.join(literals)})")

        return '&'.join(terms)

    def get_numeric_form_sdnf(self) -> str:
        """Числовая форма СДНФ"""
        minterms = self.tt.get_minterms()
        return f"{len(self.variables)} ({' , '.join(map(str, minterms))})"

    def get_numeric_form_sknf(self) -> str:
        """Числовая форма СКНФ"""
        maxterms = self.tt.get_maxterms()
        return f"{len(self.variables)} ({' , '.join(map(str, maxterms))})"

    def get_index_form(self) -> str:
        """Индексная форма функции"""
        vector = self.tt.get_vector()
        # Преобразуем вектор в число в двоичной системе
        num = 0
        for i, bit in enumerate(reversed(vector)):
            if bit:
                num += (1 << i)
        return f"F = {num} ({self._vector_to_hex(vector)})"

    def _vector_to_hex(self, vector: list) -> str:
        """Преобразует вектор в шестнадцатеричную строку"""
        # Группируем по 4 бита
        binary_str = ''.join(map(str, vector))
        # Дополняем до кратности 4
        while len(binary_str) % 4 != 0:
            binary_str = '0' + binary_str
        # Преобразуем в hex
        hex_str = ''
        for i in range(0, len(binary_str), 4):
            hex_str += format(int(binary_str[i:i + 4], 2), 'X')
        return hex_str