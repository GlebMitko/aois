# minimization.py
"""Минимизация ДНФ и КНФ (расчетный метод) для 1-5 переменных"""


class Minimization:
    def __init__(self, truth_table):
        self.tt = truth_table
        self.vars = truth_table.variables
        self.n = truth_table.var_count
        self.minterms = set(truth_table.get_minterms())
        self.maxterms = set(truth_table.get_maxterms())

    def _int_to_binary(self, n, width):
        return [int(x) for x in format(n, f'0{width}b')]

    def _term_to_string_dnf(self, term):
        literals = []
        for i, v in enumerate(term):
            if v is None:
                continue
            literals.append(self.vars[i] if v == 1 else f"!{self.vars[i]}")
        if not literals:
            return "1"
        if len(literals) == 1:
            return literals[0]
        return '&'.join(literals)

    def _term_to_string_cnf(self, term):
        literals = []
        for i, v in enumerate(term):
            if v is None:
                continue
            literals.append(self.vars[i] if v == 0 else f"!{self.vars[i]}")
        if not literals:
            return "0"
        if len(literals) == 1:
            return literals[0]
        return '|'.join(literals)

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

    def _simplify_dnf(self, terms):
        """Универсальное упрощение ДНФ для любого числа переменных"""
        if not terms:
            return []

        # Преобразуем в строки
        strings = [self._term_to_string_dnf(t) for t in terms]

        # Убираем дубликаты
        strings = list(dict.fromkeys(strings))

        # Цикл упрощения
        changed = True
        while changed:
            changed = False
            new_strings = []
            used = [False] * len(strings)

            for i in range(len(strings)):
                if used[i]:
                    continue
                for j in range(i + 1, len(strings)):
                    if used[j]:
                        continue
                    t1 = strings[i]
                    t2 = strings[j]

                    # Разбиваем на литералы
                    lits1 = set(t1.split('&')) if '&' in t1 else {t1}
                    lits2 = set(t2.split('&')) if '&' in t2 else {t2}

                    # Ищем пару a и !a
                    sym = lits1.symmetric_difference(lits2)
                    if len(sym) == 2:
                        s1, s2 = list(sym)
                        if s1 == f"!{s2}" or s2 == f"!{s1}":
                            common = lits1.intersection(lits2)
                            if common:
                                new_term = '&'.join(sorted(common))
                                new_strings.append(new_term)
                                used[i] = used[j] = True
                                changed = True
                                break
                if not used[i] and strings[i] not in new_strings:
                    new_strings.append(strings[i])

            strings = new_strings

        # Поглощение
        result = []
        for i, t1 in enumerate(strings):
            lits1 = set(t1.split('&')) if '&' in t1 else {t1}
            covered = False
            for j, t2 in enumerate(strings):
                if i != j:
                    lits2 = set(t2.split('&')) if '&' in t2 else {t2}
                    if lits1.issuperset(lits2):
                        covered = True
                        break
            if not covered:
                result.append(t1)

        return result

    def _simplify_cnf(self, terms):
        """Универсальное упрощение КНФ"""
        if not terms:
            return []

        strings = [self._term_to_string_cnf(t) for t in terms]
        strings = list(dict.fromkeys(strings))

        changed = True
        while changed:
            changed = False
            new_strings = []
            used = [False] * len(strings)

            for i in range(len(strings)):
                if used[i]:
                    continue
                for j in range(i + 1, len(strings)):
                    if used[j]:
                        continue
                    t1 = strings[i]
                    t2 = strings[j]

                    lits1 = set(t1.split('|')) if '|' in t1 else {t1}
                    lits2 = set(t2.split('|')) if '|' in t2 else {t2}

                    sym = lits1.symmetric_difference(lits2)
                    if len(sym) == 2:
                        s1, s2 = list(sym)
                        if s1 == f"!{s2}" or s2 == f"!{s1}":
                            common = lits1.intersection(lits2)
                            if common:
                                new_term = '|'.join(sorted(common))
                                new_strings.append(new_term)
                                used[i] = used[j] = True
                                changed = True
                                break
                if not used[i] and strings[i] not in new_strings:
                    new_strings.append(strings[i])

            strings = new_strings

        # Поглощение для КНФ
        result = []
        for i, t1 in enumerate(strings):
            lits1 = set(t1.split('|')) if '|' in t1 else {t1}
            covered = False
            for j, t2 in enumerate(strings):
                if i != j:
                    lits2 = set(t2.split('|')) if '|' in t2 else {t2}
                    if lits1.issuperset(lits2):
                        covered = True
                        break
            if not covered:
                result.append(t1)

        return result

    # ==================== ДНФ ====================

    def minimize_dnf_calculus(self):
        if not self.minterms:
            return "0", []

        stages = []
        current = [tuple(self._int_to_binary(mt, self.n)) for mt in sorted(self.minterms)]
        stages.append({'stage': 0, 'terms': [self._term_to_string_dnf(t) for t in current]})

        changed = True
        stage_num = 1
        while changed and len(current) > 1:
            new_terms = []
            used = [False] * len(current)
            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    merged = self._merge(current[i], current[j])
                    if merged:
                        used[i] = used[j] = True
                        if merged not in new_terms:
                            new_terms.append(merged)
            for i, t in enumerate(current):
                if not used[i] and t not in new_terms:
                    new_terms.append(t)
            changed = len(new_terms) != len(current)
            current = new_terms
            stages.append({'stage': stage_num, 'terms': [self._term_to_string_dnf(t) for t in current]})
            stage_num += 1

        # Упрощаем
        simplified = self._simplify_dnf(current)
        dnf = ' | '.join(simplified) if simplified else "0"

        return dnf, stages

    def minimize_dnf_table_method(self):
        dnf, stages = self.minimize_dnf_calculus()
        return dnf, stages, []

    # ==================== КНФ ====================

    def minimize_cnf_calculus(self):
        if not self.maxterms:
            return "1", []

        stages = []
        current = [tuple(self._int_to_binary(mt, self.n)) for mt in sorted(self.maxterms)]
        stages.append({'stage': 0, 'terms': [self._term_to_string_cnf(t) for t in current]})

        changed = True
        stage_num = 1
        while changed and len(current) > 1:
            new_terms = []
            used = [False] * len(current)
            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    merged = self._merge(current[i], current[j])
                    if merged:
                        used[i] = used[j] = True
                        if merged not in new_terms:
                            new_terms.append(merged)
            for i, t in enumerate(current):
                if not used[i] and t not in new_terms:
                    new_terms.append(t)
            changed = len(new_terms) != len(current)
            current = new_terms
            stages.append({'stage': stage_num, 'terms': [f"({self._term_to_string_cnf(t)})" for t in current]})
            stage_num += 1

        simplified = self._simplify_cnf(current)
        cnf = ' & '.join([f"({t})" for t in simplified]) if simplified else "1"

        return cnf, stages

    def minimize_cnf_table_method(self):
        cnf, stages = self.minimize_cnf_calculus()
        return cnf, stages, []

    # ==================== ВЫВОД ====================

    def print_minimization_dnf_calculus(self):
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ ДНФ (РАСЧЕТНЫЙ МЕТОД)")
        print("=" * 60)
        dnf, stages = self.minimize_dnf_calculus()
        for s in stages:
            print(f"\nЭтап {s['stage']}:")
            print(f"  {' | '.join(s['terms'])}")
        print(f"\nРезультат: {dnf}")
        return dnf

    def print_minimization_dnf_table(self):
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ ДНФ (РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД)")
        print("=" * 60)
        dnf, stages, _ = self.minimize_dnf_table_method()
        for s in stages:
            print(f"\nЭтап {s['stage']}:")
            print(f"  {' | '.join(s['terms'])}")
        print(f"\nРезультат: {dnf}")
        return dnf

    def print_minimization_cnf_calculus(self):
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ КНФ (РАСЧЕТНЫЙ МЕТОД)")
        print("=" * 60)
        cnf, stages = self.minimize_cnf_calculus()
        for s in stages:
            print(f"\nЭтап {s['stage']}:")
            if s['stage'] == 0:
                print(f"  {' & '.join(s['terms'])}")
            else:
                formatted = ' & '.join(s['terms']) if len(s['terms']) > 1 else s['terms'][0]
                print(f"  {formatted}")
        print(f"\nРезультат: {cnf}")
        return cnf

    def print_minimization_cnf_table(self):
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ КНФ (РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД)")
        print("=" * 60)
        cnf, stages, _ = self.minimize_cnf_table_method()
        for s in stages:
            print(f"\nЭтап {s['stage']}:")
            if s['stage'] == 0:
                print(f"  {' & '.join(s['terms'])}")
            else:
                formatted = ' & '.join(s['terms']) if len(s['terms']) > 1 else s['terms'][0]
                print(f"  {formatted}")
        print(f"\nРезультат: {cnf}")
        return cnf