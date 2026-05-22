# logisim_export.py
"""Экспорт инструкций для сборки схем в Logisim (без XML глюков)"""

import os


class LogisimExporter:
    """Экспорт инструкций для ручной сборки в Logisim"""

    @staticmethod
    def export_8bit_adder(filename="logisim/adder_8bit.txt"):
        os.makedirs("logisim", exist_ok=True)

        content = '''
============================================================
8-БИТНЫЙ СУММАТОР
============================================================

СХЕМА В LOGISIM:

1. Создайте новый проект (File -> New)

2. Создайте субсхему FullAdder (Project -> Add Circuit, назовите "FullAdder")

3. В схеме FullAdder (1 бит) соберите:

   ВХОДЫ: A, B, Cin (Pin, Output? No)
   ВЫХОДЫ: Sum, Cout (Pin, Output? Yes)

   ИСПОЛЬЗУЙТЕ ВЕНТИЛИ:
   - XOR (для Sum)
   - AND (3 штуки) и OR (2 штуки) для Cout

   ФОРМУЛЫ:
   Sum = A XOR B XOR Cin
   Cout = (A AND B) OR (A AND Cin) OR (B AND Cin)

   ИЛИ по СКНФ (вариант для твоего задания):
   Sum = (A|B|Cin) & (A|!B|!Cin) & (!A|B|!Cin) & (!A|!B|Cin)
   Cout = (A|B) & (A|Cin) & (B|Cin)

4. Перейдите в основную схему "main"

5. Добавьте 8 копий FullAdder (правый клик -> Copy/Paste)

6. Соедините каскадно:
   - Cin первого = 0 (провод к Ground или Pin=0)
   - Cout0 -> Cin1
   - Cout1 -> Cin2
   - ...
   - Cout7 -> Overflow (выход)

7. Добавьте входные пины:
   - A0..A7 (8 штук)
   - B0..B7 (8 штук)

8. Добавьте выходные пины:
   - S0..S7 (результат)
   - Overflow (переполнение)

9. Запустите симуляцию (Ctrl+T или Simulation -> Enable)

ПРИМЕР: 8 + 6 = 14
A = 00001000 (A7=0,A6=0,A5=0,A4=0,A3=1,A2=0,A1=0,A0=0)
B = 00000110 (B7=0,B6=0,B5=0,B4=0,B3=0,B2=1,B1=1,B0=0)
Результат S = 00001110 (14)
'''

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Создан {filename}")

    @staticmethod
    def export_excess3_plus1(filename="logisim/excess3_plus1.txt"):
        os.makedirs("logisim", exist_ok=True)

        from part2_excess3_n1 import Excess3Plus1
        from utils import build_sdnf

        converter = Excess3Plus1(n=1)
        rows = converter.truth_table()
        valid_rows = [r for r in rows if r['Y8'] != '-']
        var_names = converter.vars

        formulas = {}
        for out in converter.outputs:
            minterms = [i for i, r in enumerate(valid_rows) if r[out] == 1]
            formulas[out] = build_sdnf(minterms, var_names) if minterms else "0"

        content = f'''
============================================================
ПРЕОБРАЗОВАТЕЛЬ EXCESS-3 → EXCESS-3+1 (n=1)
============================================================

СХЕМА В LOGISIM:

1. Создайте новую схему (Project -> Add Circuit, назовите "Excess3Plus1")

2. Добавьте входные пины:
   - X8, X4, X2, X1 (Pin)

3. Добавьте выходные пины:
   - Y8, Y4, Y2, Y1, Carry (Pin, Output? Yes)

4. Поставьте вентили AND, OR, NOT

5. Соедините по формулам (после минимизации):

Y8 = {formulas['Y8']}
Y4 = {formulas['Y4']}
Y2 = {formulas['Y2']}
Y1 = {formulas['Y1']}
Carry = {formulas['Carry']}

ПРИМЕРЫ РАБОТЫ:
X=0011 (0) -> Y=0100 (1), Carry=0
X=0100 (1) -> Y=0101 (2), Carry=0
X=1000 (5) -> Y=1001 (6), Carry=0
X=1100 (9) -> Y=0000 (0), Carry=1
'''

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Создан {filename}")

    @staticmethod
    def export_counter_up8(filename="logisim/counter_up8.txt"):
        os.makedirs("logisim", exist_ok=True)

        from part3_counter_up8 import UpCounter8
        from utils import build_sdnf, to_not_and_or

        counter = UpCounter8()
        rows = counter.truth_table()
        var_names = counter.state_vars

        formulas = {}
        for trig in counter.triggers:
            minterms = [i for i, r in enumerate(rows) if r[trig] == 1]
            expr_sdnf = build_sdnf(minterms, var_names)
            formulas[trig] = to_not_and_or(expr_sdnf)

        content = f'''
============================================================
СЧЕТЧИК НАКАПЛИВАЮЩЕГО ТИПА НА 8 СОСТОЯНИЙ
Т-триггеры, базис НЕ-И-ИЛИ
============================================================

СХЕМА В LOGISIM:

СОСТОЯНИЯ: 000 → 001 → 010 → 011 → 100 → 101 → 110 → 111 → 000

ФУНКЦИИ ВОЗБУЖДЕНИЯ (базис НЕ-И-ИЛИ):

T2 = {formulas['T2']}
T1 = {formulas['T1']}
T0 = {formulas['T0']}

ПОСТРОЕНИЕ:

1. Добавьте 3 T-триггера (Memory → T Flip-Flop)
   - Назовите их Q2, Q1, Q0

2. Соедините:
   - Выходы Q2,Q1,Q0 → входы комбинационной схемы
   - Комбинационная схема → входы T2,T1,T0 триггеров
   - Clock (такт) → на все триггеры

3. Комбинационная схема (по формулам выше):
   - Используйте вентили NAND, AND, NOT
   - По формуле T2 = {formulas['T2']}
   - По формуле T1 = {formulas['T1']}
   - По формуле T0 = {formulas['T0']}

4. Начальное состояние: 000 (можно сделать сброс)

5. Запустите симуляцию:
   - Каждый такт значение увеличивается на 1
   - После 111 -> сброс в 000
'''

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Создан {filename}")

    @staticmethod
    def export_all():
        LogisimExporter.export_8bit_adder()
        LogisimExporter.export_excess3_plus1()
        LogisimExporter.export_counter_up8()
        print("\n✅ Инструкции для Logisim в папке logisim/")
        print("   Откройте .txt файлы и соберите схемы по инструкции")


if __name__ == "__main__":
    LogisimExporter.export_all()