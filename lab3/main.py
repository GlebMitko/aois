# main.py
"""Лабораторная работа 3 - Синтез комбинационных схем и автоматов"""

from part1_adder_sknf import FullAdderSKNF
from part2_excess3_n1 import Excess3Plus1
from part3_counter_up8 import UpCounter8
from logisim_export import LogisimExporter


def main():
    print("\n" + "=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА 3")
    print("СИНТЕЗ КОМБИНАЦИОННЫХ СХЕМ И АВТОМАТОВ")
    print("=" * 70)

    # Часть 1: ОДС-3 в СКНФ
    adder = FullAdderSKNF()
    adder.print_info()

    # Часть 2: Excess-3 + 1
    converter = Excess3Plus1(n=1)
    converter.print_info()

    # Часть 3: Счетчик на 8 состояний
    counter = UpCounter8()
    counter.print_info()

    # Экспорт в Logisim (.circ файлы)
    print("\n" + "=" * 70)
    print("ЭКСПОРТ В LOGISIM")
    print("=" * 70)
    LogisimExporter.export_all()

    print("\n" + "=" * 70)
    print("ГОТОВО!")
    print("Файлы .circ в папке logisim/ можно открыть в Logisim")
    print("=" * 70)


if __name__ == "__main__":
    main()