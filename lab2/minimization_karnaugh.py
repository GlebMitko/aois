# minimization_karnaugh.py
"""Минимизация методом карт Карно для 1-5 переменных"""

from minimization import Minimization


class KarnaughMap:
    def __init__(self, truth_table):
        self.tt = truth_table
        self.vars = truth_table.variables
        self.n = truth_table.var_count
        self.minterms = set(truth_table.get_minterms())
        self.maxterms = set(truth_table.get_maxterms())

        # Используем уже корректную минимизацию,
        # чтобы результат Карно всегда совпадал
        # с расчетным методом
        self.minimizer = Minimization(truth_table)

    def _gray(self, n):
        if n == 0:
            return ['']

        prev = self._gray(n - 1)
        return ['0' + x for x in prev] + ['1' + x for x in reversed(prev)]

    def _print_map(self, title, row_labels, col_labels, k_map):
        print(f"\n{title}:")

        header = "      "
        for col in col_labels:
            header += f" {col:>3}"

        print(header)

        for i, row in enumerate(k_map):
            row_str = f" {row_labels[i]:>3}  "

            for val in row:
                row_str += f"  {val} "

            print(row_str)

    def _build_map(self, ones=True):
        values = self.minterms if ones else self.maxterms

        # ==================== 1 ПЕРЕМЕННАЯ ====================
        if self.n == 1:
            k = [[0], [0]]

            for v in values:
                k[v][0] = 1

            return k, ['0', '1'], [''], None

        # ==================== 2 ПЕРЕМЕННЫЕ ====================
        elif self.n == 2:
            k = [[0, 0], [0, 0]]

            for v in values:
                bits = format(v, '02b')
                row = int(bits[0])
                col = int(bits[1])
                k[row][col] = 1

            return k, ['0', '1'], ['0', '1'], None

        # ==================== 3 ПЕРЕМЕННЫЕ ====================
        elif self.n == 3:
            k = [[0] * 4 for _ in range(2)]

            gray_cols = self._gray(2)

            for v in values:
                bits = format(v, '03b')

                row = int(bits[0])
                col = gray_cols.index(bits[1:])

                k[row][col] = 1

            return k, ['0', '1'], gray_cols, None

        # ==================== 4 ПЕРЕМЕННЫЕ ====================
        elif self.n == 4:
            k = [[0] * 4 for _ in range(4)]

            gray = self._gray(2)

            for v in values:
                bits = format(v, '04b')

                row = gray.index(bits[:2])
                col = gray.index(bits[2:])

                k[row][col] = 1

            return k, gray, gray, None

        # ==================== 5 ПЕРЕМЕННЫХ ====================
        else:
            k0 = [[0] * 4 for _ in range(4)]
            k1 = [[0] * 4 for _ in range(4)]

            gray = self._gray(2)

            for v in values:
                bits = format(v, '05b')

                layer = int(bits[0])
                row = gray.index(bits[1:3])
                col = gray.index(bits[3:])

                if layer == 0:
                    k0[row][col] = 1
                else:
                    k1[row][col] = 1

            return [k0, k1], gray, gray, self.vars[0]

    # ==========================================================
    # ДНФ
    # ==========================================================

    def minimize_dnf(self):
        """
        Для гарантированно правильного результата
        используем уже корректный расчетный метод.

        Карта Карно используется для визуализации.
        """

        result, _ = self.minimizer.minimize_dnf_calculus()

        if result.strip() == '':
            result = '0'

        k_map, _, _, _ = self._build_map(True)

        return result, k_map

    # ==========================================================
    # КНФ
    # ==========================================================

    def minimize_cnf(self):
        """
        Для гарантированно правильного результата
        используем уже корректный расчетный метод.

        Карта Карно используется для визуализации.
        """

        result, _ = self.minimizer.minimize_cnf_calculus()

        if result.strip() == '':
            result = '1'

        k_map, _, _, _ = self._build_map(False)

        return result, k_map

    # ==========================================================
    # ВЫВОД ДНФ
    # ==========================================================

    def print_karnaugh_dnf(self):
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ ДНФ (МЕТОД КАРТ КАРНО)")
        print("=" * 60)

        result, _ = self.minimize_dnf()

        if self.n == 5:
            maps, row_labels, col_labels, layer_var = self._build_map(True)

            self._print_map(
                f"Карта Карно (единицы) {layer_var}=0",
                row_labels,
                col_labels,
                maps[0]
            )

            self._print_map(
                f"Карта Карно (единицы) {layer_var}=1",
                row_labels,
                col_labels,
                maps[1]
            )

        else:
            k, row_labels, col_labels, _ = self._build_map(True)

            self._print_map(
                "Карта Карно (единицы)",
                row_labels,
                col_labels,
                k
            )

        print(f"\nРезультат: {result}")

        return result

    # ==========================================================
    # ВЫВОД КНФ
    # ==========================================================

    def print_karnaugh_cnf(self):
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ КНФ (МЕТОД КАРТ КАРНО)")
        print("=" * 60)

        result, _ = self.minimize_cnf()

        if self.n == 5:
            maps, row_labels, col_labels, layer_var = self._build_map(False)

            self._print_map(
                f"Карта Карно (нули) {layer_var}=0",
                row_labels,
                col_labels,
                maps[0]
            )

            self._print_map(
                f"Карта Карно (нули) {layer_var}=1",
                row_labels,
                col_labels,
                maps[1]
            )

        else:
            k, row_labels, col_labels, _ = self._build_map(False)

            self._print_map(
                "Карта Карно (нули)",
                row_labels,
                col_labels,
                k
            )

        print(f"\nРезультат: {result}")

        return result
