# part2_excess3_n1.py
"""Преобразователь Excess-3 → Excess-3+1 (n=1)"""

from utils import print_truth_table, get_minterms, build_sdnf


class Excess3Plus1:
    """Excess-3 + 1 преобразователь"""

    def __init__(self, n=1):
        self.n = n
        self.vars = ['X8', 'X4', 'X2', 'X1']
        self.outputs = ['Y8', 'Y4', 'Y2', 'Y1', 'Carry']

    def excess3_to_int(self, bits: list) -> int:
        """Excess-3 → число"""
        val = bits[0] * 8 + bits[1] * 4 + bits[2] * 2 + bits[3]
        return val - 3

    def int_to_excess3(self, num: int) -> list:
        """Число → Excess-3"""
        val = num + 3
        return [(val >> 3) & 1, (val >> 2) & 1, (val >> 1) & 1, val & 1]

    def truth_table(self) -> list:
        """Таблица истинности"""
        rows = []
        for x8 in [0, 1]:
            for x4 in [0, 1]:
                for x2 in [0, 1]:
                    for x1 in [0, 1]:
                        val = self.excess3_to_int([x8, x4, x2, x1])

                        if 0 <= val <= 9:
                            result = val + self.n
                            if result <= 9:
                                y8, y4, y2, y1 = self.int_to_excess3(result)
                                carry = 0
                            else:
                                y8, y4, y2, y1 = 0, 0, 0, 0
                                carry = 1
                            rows.append({
                                'X8': x8, 'X4': x4, 'X2': x2, 'X1': x1,
                                'Y8': y8, 'Y4': y4, 'Y2': y2, 'Y1': y1,
                                'Carry': carry
                            })
                        else:
                            rows.append({
                                'X8': x8, 'X4': x4, 'X2': x2, 'X1': x1,
                                'Y8': '-', 'Y4': '-', 'Y2': '-', 'Y1': '-',
                                'Carry': '-'
                            })
        return rows

    def print_info(self):
        """Вывод информации"""
        print("\n" + "=" * 60)
        print(f"ЧАСТЬ 2: ПРЕОБРАЗОВАТЕЛЬ EXCESS-3 → EXCESS-3+{self.n}")
        print("=" * 60)

        rows = self.truth_table()

        print("\nТаблица истинности:")
        print(" X8 X4 X2 X1 | число | Y8 Y4 Y2 Y1 | Carry")
        print("-" * 50)

        valid_rows = []
        for r in rows:
            if r['Y8'] != '-':
                val = self.excess3_to_int([r['X8'], r['X4'], r['X2'], r['X1']])
                print(
                    f"  {r['X8']}  {r['X4']}  {r['X2']}  {r['X1']}   |   {val}   |   {r['Y8']}  {r['Y4']}  {r['Y2']}  {r['Y1']}   |    {r['Carry']}")
                valid_rows.append(r)

        print("\n" + "=" * 60)
        print("МИНИМИЗИРОВАННЫЕ ФУНКЦИИ (СДНФ)")
        print("=" * 60)

        for out in self.outputs:
            minterms = [i for i, r in enumerate(valid_rows) if r[out] == 1]
            if minterms:
                expr = build_sdnf(minterms, self.vars)
                print(f"\n{out} = {expr}")
            else:
                print(f"\n{out} = 0")

    def get_logisim_description(self) -> str:
        """Описание для Logisim"""
        rows = self.truth_table()
        valid_rows = [r for r in rows if r['Y8'] != '-']

        desc = "\n" + "=" * 60
        desc += f"\nПРЕОБРАЗОВАТЕЛЬ EXCESS-3 → EXCESS-3+{self.n} ДЛЯ LOGISIM"
        desc += "\n" + "=" * 60
        desc += "\n\nВходы: X8, X4, X2, X1 (Excess-3 код)"
        desc += "\nВыходы: Y8, Y4, Y2, Y1 (Excess-3+1), Carry (переполнение)"
        desc += "\n\nЛогические выражения (СДНФ):\n"

        for out in self.outputs:
            minterms = [i for i, r in enumerate(valid_rows) if r[out] == 1]
            if minterms:
                expr = build_sdnf(minterms, self.vars)
                desc += f"\n{out} = {expr}"
            else:
                desc += f"\n{out} = 0"

        desc += "\n\nКак собрать в Logisim:"
        desc += "\n1. Добавить входные пины: X8, X4, X2, X1"
        desc += "\n2. Добавить выходные пины: Y8, Y4, Y2, Y1, Carry"
        desc += "\n3. Поставить вентили AND, OR, NOT по формулам выше"
        desc += "\n4. Соединить по формулам"

        return desc