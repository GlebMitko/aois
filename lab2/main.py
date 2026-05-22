# main.py
"""Главный модуль лабораторной работы 2"""

import sys
import re
from logic_parser import LogicParser
from truth_table import TruthTable
from normal_forms import NormalForms
from post_classes import PostClasses
from zhegalkin import ZhegalkinPolynomial
from fictitious_vars import FictitiousVariables
from boolean_diff import BooleanDifferentiation
from minimization import Minimization
from minimization_karnaugh import KarnaughMap


def extract_variables(expression: str) -> list:
    """Извлекает все переменные из выражения"""
    # Находим все буквы (a-e) и возвращаем уникальные отсортированные
    variables = sorted(set(re.findall(r'[a-e]', expression)))
    return variables


def print_menu():
    """Выводит меню программы"""
    print("\n" + "=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА 2: ПОСТРОЕНИЕ СКНФ И СДНФ")
    print("=" * 70)
    print("\nПоддерживаемые операции:")
    print("  & - конъюнкция (И)")
    print("  | - дизъюнкция (ИЛИ)")
    print("  ! - отрицание (НЕ)")
    print("  -> - импликация (следует)")
    print("  ~ - эквивалентность")
    print("  Переменные: a, b, c, d, e (до 5 переменных)")
    print("\nПримеры функций:")
    print("  !(!a->!b)|c")
    print("  (a&b)|(!a&c)")
    print("  a->b")
    print("  a~b")
    print("  a&b&c|!a&!b&!c")
    print("-" * 70)


class Lab2:
    """Основной класс лабораторной работы"""

    def __init__(self, expression: str, variables: list = None):
        """
        Инициализация

        Args:
            expression: логическое выражение
            variables: список переменных (если None, будут определены автоматически)
        """
        self.expression = expression

        # Автоматическое определение переменных
        if variables is None:
            variables = extract_variables(expression)

        if not variables:
            raise ValueError("В выражении не найдено переменных (a, b, c, d, e)")

        if len(variables) > 5:
            print(f"Предупреждение: найдено {len(variables)} переменных, но поддерживается максимум 5")
            variables = variables[:5]

        self.variables = variables
        print(f"\nОпределены переменные: {', '.join(self.variables)}")

        self.parser = LogicParser(expression, variables)
        self.tt = TruthTable(self.parser)
        self.nf = NormalForms(self.tt)
        self.post = PostClasses(self.tt)
        self.zheg = ZhegalkinPolynomial(self.tt)
        self.fict = FictitiousVariables(self.tt)
        self.diff = BooleanDifferentiation(self.tt)
        self.min = Minimization(self.tt)
        self.karnaugh = KarnaughMap(self.tt)

    def run_all(self):
        """Выполняет все задачи лабораторной работы"""
        print("=" * 70)
        print(f"ЛАБОРАТОРНАЯ РАБОТА 2")
        print(f"Исходная функция: {self.expression}")
        print(f"Переменные: {', '.join(self.variables)}")
        print("=" * 70)

        # 1. Таблица истинности
        self.tt.print_table()

        # 2. СДНФ и СКНФ
        print("\n" + "=" * 60)
        print("НОРМАЛЬНЫЕ ФОРМЫ")
        print("=" * 60)
        print(f"СДНФ: {self.nf.build_sdnf()}")
        print(f"СКНФ: {self.nf.build_sknf()}")

        # 3. Числовые формы
        print(f"\nЧисловая форма СДНФ: {self.nf.get_numeric_form_sdnf()}")
        print(f"Числовая форма СКНФ: {self.nf.get_numeric_form_sknf()}")

        # 4. Индексная форма
        print(f"\nИндексная форма: {self.nf.get_index_form()}")

        # 5. Классы Поста
        self.post.print_classes()

        # 6. Полином Жегалкина
        self.zheg.print_polynomial()

        # 7. Фиктивные переменные
        self.fict.print_result()

        # 8. Булева дифференциация
        try:
            self.diff.print_derivatives(max_vars=min(4, len(self.variables)))
        except Exception as e:
            print(f"\nОшибка при вычислении производных: {e}")

        # 9. Минимизация ДНФ расчетным методом
        try:
            self.min.print_minimization_dnf()
        except Exception as e:
            print(f"\nОшибка при минимизации ДНФ: {e}")

        # 10. Минимизация ДНФ расчетно-табличным методом
        try:
            self.min.print_minimization_dnf_table()
        except Exception as e:
            print(f"\nОшибка при расчетно-табличной минимизации: {e}")

        # 11. Минимизация картами Карно
        try:
            self.karnaugh.print_karnaugh_dnf()
        except Exception as e:
            print(f"\nОшибка при минимизации картами Карно: {e}")

        print("\n" + "=" * 70)
        print("АНАЛИЗ ФУНКЦИИ ЗАВЕРШЕН")
        print("=" * 70)


def main():
    """Точка входа с циклом"""
    print_menu()

    while True:
        print("\n" + "►" * 70)
        print("ВВЕДИТЕ ЛОГИЧЕСКУЮ ФУНКЦИЮ")
        print("◄" * 70)

        # Получаем функцию от пользователя
        if len(sys.argv) > 1 and not hasattr(main, 'args_processed'):
            # Если передан аргумент командной строки при первом запуске
            expression = ' '.join(sys.argv[1:])
            print(f"\nФункция из аргумента: {expression}")
            main.args_processed = True
        else:
            # Запрашиваем ввод от пользователя
            print("\nВведите логическую функцию (или 'exit' для выхода, 'help' для справки):")
            user_input = input(">>> ").strip()

            if user_input.lower() == 'exit':
                print("\nДо свидания!")
                break

            if user_input.lower() == 'help':
                print_menu()
                continue

            if not user_input:
                print("Функция не введена. Попробуйте снова.")
                continue

            expression = user_input

        print(f"\nАнализ функции: {expression}")

        try:
            lab = Lab2(expression)
            lab.run_all()
        except Exception as e:
            print(f"\n❌ ОШИБКА: {e}")
            print("\nПопробуйте другой формат функции.")
            print("Убедитесь, что:")
            print("  - Используются только переменные a, b, c, d, e")
            print("  - Операции записаны правильно: &, |, !, ->, ~")
            print("  - Расставлены скобки при необходимости")

        print("\n" + "=" * 70)
        print("Для продолжения нажмите Enter...")
        input()
        print("\n" * 2)


if __name__ == "__main__":
    # Сбрасываем флаг обработки аргументов
    main.args_processed = False
    main()