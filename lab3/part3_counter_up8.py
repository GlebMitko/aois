# part3_counter_up8.py
"""Двоичный счетчик накапливающего типа на 8 состояний (Т-триггер, базис НЕ-И-ИЛИ)"""

from utils import print_truth_table, build_sdnf, to_not_and_or


class UpCounter8:
    """Счетчик 0→1→2→3→4→5→6→7→0"""

    def __init__(self):
        self.state_vars = ['Q2', 'Q1', 'Q0']
        self.triggers = ['T2', 'T1', 'T0']

    def next_state(self, q2: int, q1: int, q0: int) -> tuple:
        """Следующее состояние (инкремент)"""
        current = (q2 << 2) | (q1 << 1) | q0
        next_val = (current + 1) % 8
        return ((next_val >> 2) & 1, (next_val >> 1) & 1, next_val & 1)

    def t_input(self, q: int, q_next: int) -> int:
        """Функция возбуждения T-триггера: T = Q ⊕ Q_next"""
        return q ^ q_next

    def truth_table(self) -> list:
        """Таблица переходов и функций возбуждения"""
        rows = []
        for q2 in [0, 1]:
            for q1 in [0, 1]:
                for q0 in [0, 1]:
                    q2n, q1n, q0n = self.next_state(q2, q1, q0)
                    rows.append({
                        'Q2': q2, 'Q1': q1, 'Q0': q0,
                        'T2': self.t_input(q2, q2n),
                        'T1': self.t_input(q1, q1n),
                        'T0': self.t_input(q0, q0n)
                    })
        return rows

    def print_info(self):
        """Вывод информации"""
        print("\n" + "=" * 60)
        print("ЧАСТЬ 3: СЧЕТЧИК НАКАПЛИВАЮЩЕГО ТИПА НА 8 СОСТОЯНИЙ")
        print("Т-триггеры, базис НЕ-И-ИЛИ")
        print("=" * 60)

        rows = self.truth_table()

        print("\nТаблица переходов и функций возбуждения:")
        print_truth_table(self.state_vars, rows, self.triggers)

        print("\n" + "=" * 60)
        print("ФУНКЦИИ ВОЗБУЖДЕНИЯ Т-ТРИГГЕРОВ")
        print("=" * 60)

        var_names = self.state_vars

        for trig in self.triggers:
            minterms = [i for i, r in enumerate(rows) if r[trig] == 1]
            expr_sdnf = build_sdnf(minterms, var_names)
            expr_nand = to_not_and_or(expr_sdnf)

            print(f"\n{trig} (минтермы: {minterms}):")
            print(f"  СДНФ: {expr_sdnf}")
            print(f"  В базисе НЕ-И-ИЛИ: {expr_nand}")

    def get_logisim_description(self) -> str:
        """Описание для Logisim"""
        rows = self.truth_table()
        var_names = self.state_vars

        desc = "\n" + "=" * 60
        desc += "\nСЧЕТЧИК НАКАПЛИВАЮЩЕГО ТИПА НА 8 СОСТОЯНИЙ ДЛЯ LOGISIM"
        desc += "\nТ-триггеры, базис НЕ-И-ИЛИ"
        desc += "\n" + "=" * 60

        for trig in self.triggers:
            minterms = [i for i, r in enumerate(rows) if r[trig] == 1]
            expr_sdnf = build_sdnf(minterms, var_names)
            expr_nand = to_not_and_or(expr_sdnf)
            desc += f"\n\n{trig} = {expr_nand}"

        desc += "\n\nКак собрать в Logisim:"
        desc += "\n1. Добавить 3 T-триггера (Memory → T Flip-Flop)"
        desc += "\n2. Соединить выходы Q2,Q1,Q0 с входами комбинационной схемы"
        desc += "\n3. Комбинационная схема вычисляет T2,T1,T0 по формулам выше"
        desc += "\n4. Подать тактовый сигнал (Clock) на все триггеры"
        desc += "\n5. Начальное состояние: 000"
        desc += "\n6. Счет: 000 → 001 → 010 → 011 → 100 → 101 → 110 → 111 → 000"

        return desc