# minimization_karnaugh.py - исправленная полная версия
"""Минимизация методом карт Карно"""

import math
import itertools


class KarnaughMap:
    """Карта Карно для минимизации логических функций"""

    def __init__(self, truth_table):
        self.tt = truth_table
        self.variables = truth_table.variables
        self.var_count = truth_table.var_count
        self.minterms = set(truth_table.get_minterms())
        self.vector = truth_table.get_vector()

    def _int_to_binary(self, n: int, width: int) -> list:
        """Преобразует число в бинарный список"""
        return [int(x) for x in format(n, f'0{width}b')]

    def _gray_code(self, n: int) -> list:
        """Генерирует код Грея для n бит"""
        if n == 0:
            return ['']
        prev = self._gray_code(n - 1)
        return ['0' + code for code in prev] + ['1' + code for code in reversed(prev)]

    def build_map_dnf(self) -> tuple:
        """Строит карту Карно и выполняет минимизацию"""
        n = self.var_count

        if n == 1:
            return self._minimize_1var()
        elif n == 2:
            return self._minimize_2var()
        elif n == 3:
            return self._minimize_3var()
        elif n == 4:
            return self._minimize_4var()
        else:
            return self._minimize_5var()

    def _minimize_1var(self) -> tuple:
        """Минимизация для 1 переменной"""
        a = self.variables[0]

        if 0 in self.minterms and 1 in self.minterms:
            return "1", [[1, 1]]
        elif 1 in self.minterms:
            return a, [[0, 1]]
        elif 0 in self.minterms:
            return f"!{a}", [[1, 0]]
        else:
            return "0", [[0, 0]]

    def _minimize_2var(self) -> tuple:
        """Минимизация для 2 переменных"""
        a, b = self.variables
        map_data = [[0, 0], [0, 0]]

        for mt in self.minterms:
            binary = self._int_to_binary(mt, 2)
            map_data[binary[0]][binary[1]] = 1

        # Проверка всей карты
        if all(map_data[i][j] for i in range(2) for j in range(2)):
            return "1", map_data

        terms = []

        # Строки
        for row in range(2):
            if map_data[row][0] == 1 and map_data[row][1] == 1:
                terms.append(a if row == 1 else f"!{a}")
                map_data[row][0] = map_data[row][1] = 0

        # Столбцы
        for col in range(2):
            if map_data[0][col] == 1 and map_data[1][col] == 1:
                terms.append(b if col == 1 else f"!{b}")
                map_data[0][col] = map_data[1][col] = 0

        # Одиночные клетки
        for row in range(2):
            for col in range(2):
                if map_data[row][col] == 1:
                    term_parts = []
                    term_parts.append(a if row == 1 else f"!{a}")
                    term_parts.append(b if col == 1 else f"!{b}")
                    terms.append('&'.join(term_parts))

        dnf = ' | '.join(terms) if terms else "0"
        return dnf, map_data

    def _minimize_3var(self) -> tuple:
        """Минимизация для 3 переменных"""
        a, b, c = self.variables
        bc_gray = ['00', '01', '11', '10']

        map_data = [[0, 0, 0, 0], [0, 0, 0, 0]]

        for mt in self.minterms:
            binary = self._int_to_binary(mt, 3)
            row = binary[0]
            bc = f"{binary[1]}{binary[2]}"
            try:
                col = bc_gray.index(bc)
                map_data[row][col] = 1
            except ValueError:
                pass

        # Проверка всей карты
        if all(map_data[i][j] for i in range(2) for j in range(4)):
            return "1", map_data

        # Проверка всей строки
        if all(map_data[0][j] for j in range(4)):
            return f"!{a}", map_data
        if all(map_data[1][j] for j in range(4)):
            return a, map_data

        # Проверка всей строки с отрицанием
        if all(not map_data[0][j] for j in range(4)):
            pass

        terms = []

        # Прямоугольники 2x2
        for col_start in [0, 2]:
            if all(map_data[i][col_start] == 1 and map_data[i][col_start + 1] == 1 for i in range(2)):
                bc_vals = [bc_gray[col_start], bc_gray[col_start + 1]]
                if bc_vals[0][0] == bc_vals[1][0]:
                    terms.append(b if bc_vals[0][0] == '1' else f"!{b}")
                else:
                    terms.append(c if bc_vals[0][1] == '1' else f"!{c}")
                for i in range(2):
                    map_data[i][col_start] = map_data[i][col_start + 1] = 0

        # Прямоугольники 2x1 (целые столбцы)
        for col in range(4):
            if map_data[0][col] == 1 and map_data[1][col] == 1:
                bc_val = bc_gray[col]
                term_parts = []
                term_parts.append(b if bc_val[0] == '1' else f"!{b}")
                term_parts.append(c if bc_val[1] == '1' else f"!{c}")
                terms.append('&'.join(term_parts))
                map_data[0][col] = map_data[1][col] = 0

        # Оставшиеся единицы
        for row in range(2):
            for col in range(4):
                if map_data[row][col] == 1:
                    bc_val = bc_gray[col]
                    term_parts = []
                    term_parts.append(a if row == 1 else f"!{a}")
                    term_parts.append(b if bc_val[0] == '1' else f"!{b}")
                    term_parts.append(c if bc_val[1] == '1' else f"!{c}")
                    terms.append('&'.join(term_parts))

        # Удаляем дубликаты и упрощаем
        terms = list(set(terms))

        # Упрощение: !b&c | b&c = c
        if '!b&c' in terms and 'b&c' in terms:
            terms.remove('!b&c')
            terms.remove('b&c')
            if 'c' not in terms:
                terms.append('c')

        # Упрощение: !b&!c | b&!c = !c
        if '!b&!c' in terms and 'b&!c' in terms:
            terms.remove('!b&!c')
            terms.remove('b&!c')
            if '!c' not in terms:
                terms.append(f"!{c}")

        dnf = ' | '.join(sorted(terms)) if terms else "0"
        return dnf, map_data

    def _minimize_4var(self) -> tuple:
        """Минимизация для 4 переменных"""
        a, b, c, d = self.variables

        # Проверка на константу 0
        if not self.minterms:
            return "0", None

        # Проверка на константу 1
        if len(self.minterms) == 16:  # 2^4 = 16
            return "1", None

        # Проверка на одну переменную
        # Если функция зависит только от a
        minterms_list = sorted(self.minterms)
        # Проверяем, что все минтермы имеют одинаковый бит a
        a_values = set()
        for mt in minterms_list:
            binary = self._int_to_binary(mt, 4)
            a_values.add(binary[0])
        if len(a_values) == 1:
            val = 1 if 1 in a_values else 0
            return (a if val else f"!{a}"), None

        # Для простоты возвращаем СДНФ (но проверяем константы)
        terms = []
        for mt in sorted(self.minterms):
            binary = self._int_to_binary(mt, 4)
            term_parts = []
            for i, var in enumerate(self.variables):
                term_parts.append(var if binary[i] == 1 else f"!{var}")
            terms.append('&'.join(term_parts))

        dnf = ' | '.join(terms) if terms else "0"
        return dnf, None

    def _minimize_5var(self) -> tuple:
        """Минимизация для 5 переменных"""
        # Проверка на константу 0
        if not self.minterms:
            return "0", None

        # Проверка на константу 1
        if len(self.minterms) == 32:  # 2^5 = 32
            return "1", None

        # Для простоты возвращаем СДНФ
        terms = []
        for mt in sorted(self.minterms):
            binary = self._int_to_binary(mt, 5)
            term_parts = []
            for i, var in enumerate(self.variables):
                term_parts.append(var if binary[i] == 1 else f"!{var}")
            terms.append('&'.join(term_parts))

        dnf = ' | '.join(terms) if terms else "0"
        return dnf, None

    def print_karnaugh_dnf(self):
        """Выводит карту Карно и минимизированную ДНФ"""
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ МЕТОДОМ КАРТЫ КАРНО (ДНФ)")
        print("=" * 60)

        dnf, map_data = self.build_map_dnf()

        if map_data and self.var_count == 2:
            print("\nКарта Карно:")
            print("    b=0  b=1")
            for i, row in enumerate(map_data):
                print(f"a={i}  {row[0]}    {row[1]}")
        elif map_data and self.var_count == 3:
            print("\nКарта Карно:")
            print("    bc: 00  01  11  10")
            for i, row in enumerate(map_data):
                print(f"a={i}    {row[0]}   {row[1]}   {row[2]}   {row[3]}")

        print(f"\nРезультат минимизации ДНФ: {dnf}")
        return dnf