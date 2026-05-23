# minimization.py
"""Минимизация ДНФ и КНФ (расчетный и расчетно-табличный методы)"""

class Minimization:

    def __init__(self, truth_table):
        self.tt = truth_table
        self.vars = truth_table.variables
        self.n = truth_table.var_count

        self.minterms = set(truth_table.get_minterms())
        self.maxterms = set(truth_table.get_maxterms())

    # ==========================================================
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ==========================================================

    def _int_to_binary(self, n, width):
        return tuple(int(x) for x in format(n, f'0{width}b'))

    def _merge(self, t1, t2):

        diff = 0
        pos = -1

        for i in range(len(t1)):

            if t1[i] != t2[i]:
                diff += 1
                pos = i

            if diff > 1:
                return None

        if diff == 1:
            res = list(t1)
            res[pos] = None
            return tuple(res)

        return None

    def _covers(self, implicant, minterm):

        bits = self._int_to_binary(minterm, self.n)

        for i in range(self.n):

            if implicant[i] is not None:

                if implicant[i] != bits[i]:
                    return False

        return True

    # ==========================================================
    # СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ
    # ==========================================================

    def _term_to_string_dnf(self, term):

        literals = []

        for i, v in enumerate(term):

            if v is None:
                continue

            if v == 1:
                literals.append(self.vars[i])
            else:
                literals.append(f"!{self.vars[i]}")

        if not literals:
            return "1"

        return '&'.join(literals)

    def _term_to_string_cnf(self, term):

        literals = []

        for i, v in enumerate(term):

            if v is None:
                continue

            if v == 0:
                literals.append(self.vars[i])
            else:
                literals.append(f"!{self.vars[i]}")

        if not literals:
            return "0"

        return '|'.join(literals)

    # ==========================================================
    # ПОИСК ПРОСТЫХ ИМПЛИКАНТ
    # ==========================================================

    def _find_prime_implicants(self, terms):

        current = list(terms)

        prime_implicants = []

        while True:

            used = [False] * len(current)

            new_terms = []

            # Группировка и склеивание
            for i in range(len(current)):

                for j in range(i + 1, len(current)):

                    merged = self._merge(current[i], current[j])

                    if merged is not None:

                        used[i] = True
                        used[j] = True

                        if merged not in new_terms:
                            new_terms.append(merged)

            # Добавляем несклеенные
            for i, term in enumerate(current):

                if not used[i]:

                    if term not in prime_implicants:
                        prime_implicants.append(term)

            if not new_terms:
                break

            current = new_terms

        return prime_implicants

    # ==========================================================
    # ТАБЛИЦА ПОКРЫТИЯ
    # ==========================================================

    def _build_cover_table(self, prime_implicants, minterms):

        table = {}

        for pi in prime_implicants:

            covered = []

            for mt in minterms:

                if self._covers(pi, mt):
                    covered.append(mt)

            table[pi] = covered

        return table

    def _find_essential_implicants(self, cover_table, minterms):

        essential = []

        for mt in minterms:

            covering = []

            for pi, covered in cover_table.items():

                if mt in covered:
                    covering.append(pi)

            if len(covering) == 1:

                if covering[0] not in essential:
                    essential.append(covering[0])

        return essential

    # ==========================================================
    # УПРОЩЕНИЕ
    # ==========================================================

    def _simplify_dnf(self, terms):

        strings = []

        for t in terms:

            s = self._term_to_string_dnf(t)

            if s not in strings:
                strings.append(s)

        return strings

    def _simplify_cnf(self, terms):

        strings = []

        for t in terms:

            s = self._term_to_string_cnf(t)

            if s not in strings:
                strings.append(s)

        return strings

    # ==========================================================
    # РАСЧЕТНЫЙ МЕТОД ДНФ
    # ==========================================================

    def minimize_dnf_calculus(self):

        if not self.minterms:
            return "0", []

        current = [
            self._int_to_binary(mt, self.n)
            for mt in sorted(self.minterms)
        ]

        stages = []

        stages.append({
            'stage': 0,
            'terms': [
                self._term_to_string_dnf(t)
                for t in current
            ]
        })

        stage_num = 1

        while True:

            used = [False] * len(current)

            new_terms = []

            for i in range(len(current)):

                for j in range(i + 1, len(current)):

                    merged = self._merge(current[i], current[j])

                    if merged is not None:

                        used[i] = True
                        used[j] = True

                        if merged not in new_terms:
                            new_terms.append(merged)

            for i, t in enumerate(current):

                if not used[i]:

                    if t not in new_terms:
                        new_terms.append(t)

            if new_terms == current:
                break

            current = new_terms

            stages.append({
                'stage': stage_num,
                'terms': [
                    self._term_to_string_dnf(t)
                    for t in current
                ]
            })

            stage_num += 1

        simplified = self._simplify_dnf(current)

        result = ' | '.join(simplified)

        return result, stages

    # ==========================================================
    # РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД ДНФ
    # ==========================================================

    def minimize_dnf_table_method(self):

        if not self.minterms:
            return "0", [], []

        initial_terms = [
            self._int_to_binary(mt, self.n)
            for mt in sorted(self.minterms)
        ]

        stages = []

        stages.append({
            'stage': 0,
            'terms': [
                self._term_to_string_dnf(t)
                for t in initial_terms
            ]
        })

        # Поиск простых импликант
        prime_implicants = self._find_prime_implicants(initial_terms)

        stages.append({
            'stage': 1,
            'terms': [
                self._term_to_string_dnf(t)
                for t in prime_implicants
            ]
        })

        # Таблица покрытия
        cover_table = self._build_cover_table(
            prime_implicants,
            sorted(self.minterms)
        )

        # Обязательные импликанты
        essential = self._find_essential_implicants(
            cover_table,
            sorted(self.minterms)
        )

        covered = set()

        for pi in essential:

            for mt in cover_table[pi]:
                covered.add(mt)

        result_implicants = essential[:]

        # Добавляем недостающие
        for mt in self.minterms:

            if mt not in covered:

                for pi in prime_implicants:

                    if pi not in result_implicants:

                        if self._covers(pi, mt):

                            result_implicants.append(pi)

                            for x in cover_table[pi]:
                                covered.add(x)

                            break

        simplified = self._simplify_dnf(result_implicants)

        result = ' | '.join(simplified)

        # Данные таблицы покрытия
        table_data = []

        for pi in prime_implicants:

            table_data.append({
                'implicant': self._term_to_string_dnf(pi),
                'covers': cover_table[pi],
                'essential': pi in essential
            })

        return result, stages, table_data

    # ==========================================================
    # РАСЧЕТНЫЙ МЕТОД КНФ
    # ==========================================================

    def minimize_cnf_calculus(self):

        if not self.maxterms:
            return "1", []

        current = [
            self._int_to_binary(mt, self.n)
            for mt in sorted(self.maxterms)
        ]

        stages = []

        stages.append({
            'stage': 0,
            'terms': [
                self._term_to_string_cnf(t)
                for t in current
            ]
        })

        stage_num = 1

        while True:

            used = [False] * len(current)

            new_terms = []

            for i in range(len(current)):

                for j in range(i + 1, len(current)):

                    merged = self._merge(current[i], current[j])

                    if merged is not None:

                        used[i] = True
                        used[j] = True

                        if merged not in new_terms:
                            new_terms.append(merged)

            for i, t in enumerate(current):

                if not used[i]:

                    if t not in new_terms:
                        new_terms.append(t)

            if new_terms == current:
                break

            current = new_terms

            stages.append({
                'stage': stage_num,
                'terms': [
                    self._term_to_string_cnf(t)
                    for t in current
                ]
            })

            stage_num += 1

        simplified = self._simplify_cnf(current)

        result = ' & '.join([f"({x})" for x in simplified])

        return result, stages

    # ==========================================================
    # РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД КНФ
    # ==========================================================

    def minimize_cnf_table_method(self):

        if not self.maxterms:
            return "1", [], []

        initial_terms = [
            self._int_to_binary(mt, self.n)
            for mt in sorted(self.maxterms)
        ]

        stages = []

        stages.append({
            'stage': 0,
            'terms': [
                self._term_to_string_cnf(t)
                for t in initial_terms
            ]
        })

        prime_implicants = self._find_prime_implicants(initial_terms)

        stages.append({
            'stage': 1,
            'terms': [
                self._term_to_string_cnf(t)
                for t in prime_implicants
            ]
        })

        cover_table = self._build_cover_table(
            prime_implicants,
            sorted(self.maxterms)
        )

        essential = self._find_essential_implicants(
            cover_table,
            sorted(self.maxterms)
        )

        covered = set()

        for pi in essential:

            for mt in cover_table[pi]:
                covered.add(mt)

        result_implicants = essential[:]

        for mt in self.maxterms:

            if mt not in covered:

                for pi in prime_implicants:

                    if pi not in result_implicants:

                        if self._covers(pi, mt):

                            result_implicants.append(pi)

                            for x in cover_table[pi]:
                                covered.add(x)

                            break

        simplified = self._simplify_cnf(result_implicants)

        result = ' & '.join(
            [f"({x})" for x in simplified]
        )

        table_data = []

        for pi in prime_implicants:

            table_data.append({
                'implicant': self._term_to_string_cnf(pi),
                'covers': cover_table[pi],
                'essential': pi in essential
            })

        return result, stages, table_data

    # ==========================================================
    # ВЫВОД
    # ==========================================================

    def print_minimization_dnf_calculus(self):

        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ ДНФ (РАСЧЕТНЫЙ МЕТОД)")
        print("=" * 60)

        result, stages = self.minimize_dnf_calculus()

        for s in stages:

            print(f"\nЭтап {s['stage']}:")

            print("  " + " | ".join(s['terms']))

        print(f"\nРезультат: {result}")

        return result

    def print_minimization_dnf_table(self):

        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ ДНФ (РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД)")
        print("=" * 60)

        result, stages, table_data = self.minimize_dnf_table_method()

        for s in stages:

            print(f"\nЭтап {s['stage']}:")

            print("  " + " | ".join(s['terms']))

        print("\nТаблица покрытия:")

        for row in table_data:

            mark = "*" if row['essential'] else " "

            print(
                f" {mark} {row['implicant']:20} -> {row['covers']}"
            )

        print("\n* — обязательная импликанта")

        print(f"\nРезультат: {result}")

        return result

    def print_minimization_cnf_calculus(self):

        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ КНФ (РАСЧЕТНЫЙ МЕТОД)")
        print("=" * 60)

        result, stages = self.minimize_cnf_calculus()

        for s in stages:

            print(f"\nЭтап {s['stage']}:")

            print("  " + " & ".join(s['terms']))

        print(f"\nРезультат: {result}")

        return result

    def print_minimization_cnf_table(self):

        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ КНФ (РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД)")
        print("=" * 60)

        result, stages, table_data = self.minimize_cnf_table_method()

        for s in stages:

            print(f"\nЭтап {s['stage']}:")

            print("  " + " & ".join(s['terms']))

        print("\nТаблица покрытия:")

        for row in table_data:

            mark = "*" if row['essential'] else " "

            print(
                f" {mark} {row['implicant']:20} -> {row['covers']}"
            )

        print("\n* — обязательная импликанта")

        print(f"\nРезультат: {result}")

        return result