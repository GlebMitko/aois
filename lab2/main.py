# main.py
"""Лабораторная работа 2 - Построение СКНФ и СДНФ на основании таблиц истинности"""

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
    """Извлекает все переменные из выражения (a, b, c, d, e)"""
    variables = sorted(set(re.findall(r'[a-e]', expression)))
    return variables


def print_menu():
    """Выводит меню программы"""
    print("\n" + "=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА 2")
    print("ПОСТРОЕНИЕ СКНФ И СДНФ НА ОСНОВАНИИ ТАБЛИЦ ИСТИННОСТИ")
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
    """Основной класс лабораторной работы 2"""

    def __init__(self, expression: str, variables: list = None):
        """
        Инициализация

        Args:
            expression: логическое выражение
            variables: список переменных (если None, будут определены автоматически)
        """
        self.expression = expression

        # Автоматическое определение переменных если не указаны
        if variables is None:
            variables = extract_variables(expression)

        if not variables:
            raise ValueError("В выражении не найдено переменных (a, b, c, d, e)")

        if len(variables) > 5:
            print(f"Предупреждение: найдено {len(variables)} переменных, но поддерживается максимум 5")
            variables = variables[:5]

        self.variables = variables
        print(f"\nОпределены переменные: {', '.join(self.variables)}")

        # Создаем все необходимые объекты
        self.parser = LogicParser(expression, variables)
        self.tt = TruthTable(self.parser)
        self.nf = NormalForms(self.tt)
        self.post = PostClasses(self.tt)
        self.zheg = ZhegalkinPolynomial(self.tt)
        self.fict = FictitiousVariables(self.tt)
        self.diff = BooleanDifferentiation(self.tt)
        self.minim = Minimization(self.tt)
        self.karnaugh = KarnaughMap(self.tt)

    def print_table(self):
        """Вывод таблицы истинности"""
        self.tt.print_table()

    def print_normal_forms(self):
        """Вывод нормальных форм"""
        print("\n" + "=" * 60)
        print("НОРМАЛЬНЫЕ ФОРМЫ")
        print("=" * 60)
        print(f"СДНФ: {self.nf.build_sdnf()}")
        print(f"СКНФ: {self.nf.build_sknf()}")

    def print_numeric_forms(self):
        """Вывод числовых форм"""
        print(f"\nЧисловая форма СДНФ: {self.nf.get_numeric_form_sdnf()}")
        print(f"Числовая форма СКНФ: {self.nf.get_numeric_form_sknf()}")

    def print_index_form(self):
        """Вывод индексной формы"""
        print(f"\nИндексная форма: {self.nf.get_index_form()}")

    def print_post_classes(self):
        """Вывод классов Поста"""
        self.post.print_classes()

    def print_zhegalkin(self):
        """Вывод полинома Жегалкина"""
        self.zheg.print_polynomial()

    def print_fictitious(self):
        """Вывод фиктивных переменных"""
        self.fict.print_result()

    def print_derivatives(self):
        """Вывод булевой дифференциации"""
        self.diff.print_derivatives()

    def print_minimization_dnf_calculus(self):
        """Минимизация ДНФ расчетным методом"""
        self.minim.print_minimization_dnf_calculus()

    def print_minimization_dnf_table(self):
        """Минимизация ДНФ расчетно-табличным методом"""
        self.minim.print_minimization_dnf_table()

    def print_minimization_cnf_calculus(self):
        """Минимизация КНФ расчетным методом"""
        self.minim.print_minimization_cnf_calculus()

    def print_minimization_cnf_table(self):
        """Минимизация КНФ расчетно-табличным методом"""
        self.minim.print_minimization_cnf_table()

    def print_karnaugh_dnf(self):
        """Минимизация ДНФ картами Карно"""
        self.karnaugh.print_karnaugh_dnf()

    def print_karnaugh_cnf(self):
        """Минимизация КНФ картами Карно"""
        self.karnaugh.print_karnaugh_cnf()

    def run_all(self):
        """Выполняет все задачи лабораторной работы"""
        print("\n" + "=" * 70)
        print(f"АНАЛИЗ ФУНКЦИИ: {self.expression}")
        print("=" * 70)

        # 1. Таблица истинности
        self.print_table()

        # 2. СДНФ и СКНФ
        self.print_normal_forms()

        # 3. Числовые формы
        self.print_numeric_forms()

        # 4. Индексная форма
        self.print_index_form()

        # 5. Классы Поста
        self.print_post_classes()

        # 6. Полином Жегалкина
        self.print_zhegalkin()

        # 7. Фиктивные переменные
        self.print_fictitious()

        # 8. Булева дифференциация
        self.print_derivatives()

        # 9. Минимизация ДНФ (расчетный метод)
        self.print_minimization_dnf_calculus()

        # 10. Минимизация ДНФ (расчетно-табличный метод)
        self.print_minimization_dnf_table()

        # 11. Минимизация ДНФ (карты Карно)
        self.print_karnaugh_dnf()

        # 12. Минимизация КНФ (расчетный метод)
        self.print_minimization_cnf_calculus()

        # 13. Минимизация КНФ (расчетно-табличный метод)
        self.print_minimization_cnf_table()

        # 14. Минимизация КНФ (карты Карно)
        self.print_karnaugh_cnf()

        print("\n" + "=" * 70)
        print("АНАЛИЗ ФУНКЦИИ ЗАВЕРШЕН")
        print("=" * 70)


def main():
    """Главная функция с циклом"""
    print_menu()

    while True:
        print("\n" + "►" * 70)
        print("ВВЕДИТЕ ЛОГИЧЕСКУЮ ФУНКЦИЮ")
        print("◄" * 70)

        # Получаем функцию от пользователя
        if len(sys.argv) > 1 and not hasattr(main, 'args_processed'):
            expression = ' '.join(sys.argv[1:])
            print(f"\nФункция из аргумента: {expression}")
            main.args_processed = True
        else:
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
            import traceback
            traceback.print_exc()
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
    main.args_processed = False
    main()