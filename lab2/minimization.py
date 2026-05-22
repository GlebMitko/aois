# minimization.py
"""Минимизация логических функций: расчетный и расчетно-табличный методы"""

from itertools import combinations
import itertools

class Minimization:
    """Класс для минимизации логических функций"""

    def __init__(self, truth_table):
        self.tt = truth_table
        self.variables = truth_table.variables
        self.var_count = truth_table.var_count
        self.minterms = truth_table.get_minterms()
        self.maxterms = truth_table.get_maxterms()

    def _int_to_binary(self, n: int, width: int) -> list:
        """Преобразует число в бинарный список"""
        return [int(x) for x in format(n, f'0{width}b')]

    def _term_to_string(self, term: tuple) -> str:
        """
        Преобразует терм (кортеж с 0/1/None) в строку
        None означает отсутствие переменной (склеена)
        """
        literals = []
        for i, val in enumerate(term):
            if val is None:
                continue
            if val == 1:
                literals.append(self.variables[i])
            else:
                literals.append(f"!{self.variables[i]}")

        if not literals:
            return "1"
        if len(literals) == 1:
            return literals[0]
        return '&'.join(literals)

    def _terms_mergeable(self, t1: tuple, t2: tuple) -> tuple:
        """
        Проверяет, можно ли склеить два терма
        Возвращает склеенный терм или None
        """
        diff_count = 0
        diff_pos = -1
        result = list(t1)

        for i in range(len(t1)):
            if t1[i] != t2[i]:
                diff_count += 1
                diff_pos = i
                if diff_count > 1:
                    return None

        if diff_count == 1:
            result[diff_pos] = None
            return tuple(result)
        return None

    def _gluing_stage(self, terms: list) -> tuple:
        """
        Один этап склеивания
        Возвращает (новые_термы, использованные_термы)
        """
        used = [False] * len(terms)
        new_terms = []

        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                merged = self._terms_mergeable(terms[i], terms[j])
                if merged is not None:
                    used[i] = True
                    used[j] = True
                    if merged not in new_terms:
                        new_terms.append(merged)

        # Добавляем неиспользованные термы
        for i, term in enumerate(terms):
            if not used[i] and term not in new_terms:
                new_terms.append(term)

        return new_terms, used

    def minimize_dnf_calculus(self) -> tuple:
        """
        Минимизация ДНФ расчетным методом

        Returns:
            tuple: (минимальная_ДНФ, этапы_склеивания)
        """
        if not self.minterms:
            return "0", []

        stages = []

        # Начальные термы (конституэнты единицы)
        current_terms = []
        for mt in self.minterms:
            binary = self._int_to_binary(mt, self.var_count)
            current_terms.append(tuple(binary))

        stages.append({
            'stage': 0,
            'terms': current_terms.copy(),
            'description': f"Исходные конституэнты: {[self._term_to_string(t) for t in current_terms]}"
        })

        # Многократное склеивание
        changed = True
        stage_num = 1
        while changed and len(current_terms) > 1:
            new_terms, used = self._gluing_stage(current_terms)

            stages.append({
                'stage': stage_num,
                'terms': new_terms.copy(),
                'description': f"После {stage_num}-го склеивания: {[self._term_to_string(t) for t in new_terms]}"
            })

            changed = len(new_terms) != len(current_terms)
            current_terms = new_terms
            stage_num += 1

        # Удаление лишних импликант
        minimal_terms = self._remove_redundant_implicants(current_terms)

        stages.append({
            'stage': 'final',
            'terms': minimal_terms.copy(),
            'description': f"После удаления лишних импликант: {[self._term_to_string(t) for t in minimal_terms]}"
        })

        # Формируем строку ДНФ
        dnf_parts = [self._term_to_string(t) for t in minimal_terms]
        dnf = ' | '.join(dnf_parts) if dnf_parts else "0"

        return dnf, stages

    def _remove_redundant_implicants(self, implicants: list) -> list:
        """
        Удаление лишних импликант
        """
        if len(implicants) <= 1:
            return implicants

        essential = []
        remaining = implicants.copy()

        # Проверяем каждую импликанту
        for i, imp in enumerate(implicants):
            # Проверяем, покрывает ли эта импликанта минтермы, которые не покрывают другие
            imp_minterms = self._get_implicant_minterms(imp)

            other_minterms = set()
            for j, other in enumerate(implicants):
                if i != j:
                    other_minterms.update(self._get_implicant_minterms(other))

            # Если есть минтермы, покрываемые только этой импликантой
            unique = imp_minterms - other_minterms
            if unique:
                essential.append(imp)
                remaining = [r for r in remaining if r != imp]

        # Если все импликанты оказались существенными
        if essential:
            return essential

        # Иначе возвращаем все (или выбираем минимальное покрытие)
        return self._find_minimal_cover(implicants)

    def _get_implicant_minterms(self, implicant: tuple) -> set:
        """
        Возвращает множество минтермов, покрываемых импликантой
        """
        minterms_set = set()

        # Генерируем все комбинации для позиций с None
        none_positions = [i for i, val in enumerate(implicant) if val is None]
        fixed_positions = [(i, val) for i, val in enumerate(implicant) if val is not None]

        # Перебираем все комбинации для свободных переменных
        for bits in itertools.product([0, 1], repeat=len(none_positions)):
            term = [None] * self.var_count
            for pos, val in fixed_positions:
                term[pos] = val
            for idx, pos in enumerate(none_positions):
                term[pos] = bits[idx]

            # Преобразуем в число
            num = 0
            for i, val in enumerate(term):
                if val == 1:
                    num |= (1 << (self.var_count - 1 - i))
            minterms_set.add(num)

        return minterms_set

    def _find_minimal_cover(self, implicants: list) -> list:
        """
        Находит минимальное покрытие методом перебора (для небольших функций)
        """
        if len(implicants) > 10:  # Если много, возвращаем все
            return implicants

        all_minterms = set(self.minterms)

        # Для каждого импликанта получаем покрываемые минтермы
        coverage = []
        for imp in implicants:
            coverage.append(self._get_implicant_minterms(imp))

        # Поиск минимального покрытия
        n = len(implicants)
        best_cover = None
        best_size = n + 1

        for mask in range(1, 1 << n):
            covered = set()
            selected = []
            for i in range(n):
                if mask >> i & 1:
                    covered.update(coverage[i])
                    selected.append(implicants[i])

            if all_minterms.issubset(covered):
                if len(selected) < best_size:
                    best_size = len(selected)
                    best_cover = selected

        return best_cover if best_cover else implicants

    def minimize_dnf_table_method(self) -> tuple:
        """
        Минимизация ДНФ расчетно-табличным методом

        Returns:
            tuple: (минимальная_ДНФ, этапы, таблица)
        """
        # Сначала проводим склеивание как в расчетном методе
        dnf, stages = self.minimize_dnf_calculus()

        # Строим таблицу покрытия для последнего этапа
        final_terms = stages[-1]['terms']

        # Получаем импликанты и минтермы
        implicants = final_terms
        minterms_list = self.minterms

        # Строим таблицу
        table = []
        for imp in implicants:
            row = {
                'implicant': self._term_to_string(imp),
                'covers': sorted(list(self._get_implicant_minterms(imp)))
            }
            table.append(row)

        return dnf, stages, table

    def print_minimization_dnf(self):
        """Вывод минимизации ДНФ расчетным методом"""
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ ДНФ (РАСЧЕТНЫЙ МЕТОД)")
        print("=" * 60)

        dnf, stages = self.minimize_dnf_calculus()

        for stage in stages:
            print(f"\n{stage['description']}")

        print(f"\nРезультат минимизации ДНФ: {dnf}")
        return dnf

    def print_minimization_dnf_table(self):
        """Вывод минимизации ДНФ расчетно-табличным методом"""
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ ДНФ (РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД)")
        print("=" * 60)

        dnf, stages, table = self.minimize_dnf_table_method()

        for stage in stages:
            if stage['stage'] != 'final':
                print(f"\n{stage['description']}")

        print("\nТаблица покрытия:")
        print("-" * 50)
        print(f"{'Импликанта':<20} | {'Покрываемые минтермы'}")
        print("-" * 50)
        for row in table:
            print(f"{row['implicant']:<20} | {row['covers']}")
        print("-" * 50)

        print(f"\nРезультат минимизации ДНФ: {dnf}")
        return dnf