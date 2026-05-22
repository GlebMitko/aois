# part1_adder_sknf.py
"""ОДС-3 (полный сумматор) с представлением выходных функций в СКНФ"""

from utils import print_truth_table, get_maxterms, build_sknf


class FullAdderSKNF:
    """1-битный полный сумматор - вывод в СКНФ"""

    def __init__(self):
        self.vars = ['A', 'B', 'Cin']
        self.outputs = ['Sum', 'Cout']

    def truth_table(self) -> list:
        """Таблица истинности"""
        rows = []
        for a in [0, 1]:
            for b in [0, 1]:
                for cin in [0, 1]:
                    s = a ^ b ^ cin
                    cout = (a & b) | (a & cin) | (b & cin)
                    rows.append({
                        'A': a, 'B': b, 'Cin': cin,
                        'Sum': s, 'Cout': cout
                    })
        return rows

    def get_8bit_adder_description(self) -> str:
        """Описание 8-битного сумматора для Logisim"""
        return """
        8-БИТНЫЙ СУММАТОР (КАСКАДНОЕ СОЕДИНЕНИЕ)

        Схема: 8 полных сумматоров (Full Adder), соединенных последовательно.

        Полный сумматор (1 бит) в СКНФ:
        - Sum = (A|B|Cin) & (A|!B|!Cin) & (!A|B|!Cin) & (!A|!B|Cin)
        - Cout = (A|B) & (A|Cin) & (B|Cin)

        Каскад для 8 бит:
        - A7-A0: первое число
        - B7-B0: второе число
        - Cin0 = 0
        - Cout0 → Cin1 → Cout1 → Cin2 → ... → Cout7

        Результат: S7-S0
        Переполнение: Cout7

        Пример: 8 + 6 = 14
        8  = 00001000
        6  = 00000110
        14 = 00001110
        """

    def get_sum_sknf(self) -> str:
        """СКНФ для суммы"""
        rows = self.truth_table()
        maxterms = get_maxterms(rows, 'Sum', 3)
        return build_sknf(maxterms, self.vars)

    def get_cout_sknf(self) -> str:
        """СКНФ для переноса"""
        rows = self.truth_table()
        maxterms = get_maxterms(rows, 'Cout', 3)
        return build_sknf(maxterms, self.vars)

    def print_info(self):
        """Вывод информации"""
        print("\n" + "=" * 60)
        print("ЧАСТЬ 1: ОДС-3 (ПОЛНЫЙ СУММАТОР) - ВЫХОД В СКНФ")
        print("=" * 60)

        rows = self.truth_table()
        print("\nТаблица истинности:")
        print_truth_table(self.vars, rows, self.outputs)

        print(f"\nСКНФ для SUM:")
        print(f"  {self.get_sum_sknf()}")

        print(f"\nСКНФ для COUT:")
        print(f"  {self.get_cout_sknf()}")

    def get_8bit_adder_description(self) -> str:
        """Описание 8-битного сумматора для Logisim"""
        return """
        ============================================================
        8-БИТНЫЙ СУММАТОР (КАСКАДНОЕ СОЕДИНЕНИЕ)
        ============================================================

        Схема: 8 полных сумматоров (Full Adder), соединенных последовательно.

        Полный сумматор (1 бит):
        - Входы: A, B, Cin
        - Выходы: Sum, Cout
        - Функции в СКНФ:
          Sum = (A|B|Cin) & (A|!B|!Cin) & (!A|B|!Cin) & (!A|!B|Cin)
          Cout = (A|B) & (A|Cin) & (B|Cin)

        Каскад для 8 бит:
        - A7-A0: первое число
        - B7-B0: второе число
        - Cin0 = 0
        - Cout0 → Cin1
        - Cout1 → Cin2
        - ...
        - Cout7 = переполнение (Overflow)

        Результат: S7-S0

        Пример: 8 + 6 = 14
        8  = 00001000
        6  = 00000110
        14 = 00001110
        """