# minimization_karnaugh.py
"""Минимизация методом карт Карно для 1-5 переменных (честный табличный метод)"""

from minimization import Minimization


class KarnaughMap:
    def __init__(self, truth_table):
        self.tt = truth_table
        self.vars = truth_table.variables
        self.n = truth_table.var_count
        self.minterms = set(truth_table.get_minterms())
        self.maxterms = set(truth_table.get_maxterms())

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

    def _get_map_structure(self, ones=True):
        """
        Строит карту Карно и возвращает её структуру:
        матрицу (или две для 5 переменных) и карту {координаты: номер_набора}
        """
        # Нам ВСЕГДА нужен один и тот же порядок индексов для координат,
        # независимо от того, минимизируем мы ДНФ или КНФ. Карта Карно — одна.
        # Просто внутри ячеек будут лежать либо 1, либо 0.

        if self.n == 1:
            k = [[0], [0]]
            coord_to_term = {}
            for v in range(2):
                k[v][0] = 1 if v in self.minterms else 0
                coord_to_term[(0, v, 0)] = v
            return k, ['0', '1'], [''], coord_to_term

        elif self.n == 2:
            k = [[0, 0], [0, 0]]
            coord_to_term = {}
            for r in range(2):
                for c in range(2):
                    term = (r << 1) | c
                    k[r][c] = 1 if term in self.minterms else 0
                    coord_to_term[(0, r, c)] = term
            return k, ['0', '1'], ['0', '1'], coord_to_term

        elif self.n == 3:
            k = [[0] * 4 for _ in range(2)]
            gray_cols = self._gray(2)
            coord_to_term = {}
            for r in range(2):
                for c, g_c in enumerate(gray_cols):
                    bits = f"{r}{g_c}"
                    term = int(bits, 2)
                    k[r][c] = 1 if term in self.minterms else 0
                    coord_to_term[(0, r, c)] = term
            return k, ['0', '1'], gray_cols, coord_to_term

        elif self.n == 4:
            k = [[0] * 4 for _ in range(4)]
            gray = self._gray(2)
            coord_to_term = {}
            for r, g_r in enumerate(gray):
                for c, g_c in enumerate(gray):
                    bits = f"{g_r}{g_c}"
                    term = int(bits, 2)
                    k[r][c] = 1 if term in self.minterms else 0
                    coord_to_term[(0, r, c)] = term
            return k, gray, gray, coord_to_term

        else:
            k0 = [[0] * 4 for _ in range(4)]
            k1 = [[0] * 4 for _ in range(4)]
            gray = self._gray(2)
            coord_to_term = {}
            for layer in range(2):
                k_curr = k0 if layer == 0 else k1
                for r, g_r in enumerate(gray):
                    for c, g_c in enumerate(gray):
                        bits = f"{layer}{g_r}{g_c}"
                        term = int(bits, 2)
                        k_curr[r][c] = 1 if term in self.minterms else 0
                        coord_to_term[(layer, r, c)] = term
            return [k0, k1], gray, gray, coord_to_term

    def _build_map(self, ones=True):
        """Инвертирует значения матрицы для вывода нулей в КНФ, если требуется"""
        k, r, c, coord_to_term = self._get_map_structure(ones)
        if not ones:
            if self.n == 5:
                k_res = [[[1 - val for val in row] for row in layer] for layer in k]
            else:
                k_res = [[1 - val for val in row] for row in k]
            return k_res, r, c, self.vars[0] if self.n == 5 else None
        return k, r, c, self.vars[0] if self.n == 5 else None

    def _get_neighbors(self, coord):
        l, r, c = coord
        max_l = 2 if self.n == 5 else 1
        max_r = 1 if self.n == 1 else (2 if self.n in (2, 3) else 4)
        max_c = 1 if self.n == 1 else (2 if self.n == 2 else 4)

        neighbors = []
        if max_l > 1:
            neighbors.append(((l + 1) % max_l, r, c))
        neighbors.append((l, (r - 1) % max_r, c))
        neighbors.append((l, (r + 1) % max_r, c))
        if max_c > 1:
            neighbors.append((l, r, (c - 1) % max_c))
            neighbors.append((l, r, (c + 1) % max_c))

        return set(neighbors)

    def _find_karnaugh_loops(self, target_coords):
        if not target_coords:
            return []

        current_loops = [{coord} for coord in target_coords]
        all_valid_loops = []
        max_power = self.n

        for power in range(max_power + 1):
            size = 2 ** power
            loops_of_size = [loop for loop in current_loops if len(loop) == size]

            if not loops_of_size:
                break

            all_valid_loops.extend(loops_of_size)
            next_loops = []

            for i in range(len(loops_of_size)):
                for j in range(i + 1, len(loops_of_size)):
                    l1, l2 = loops_of_size[i], loops_of_size[j]
                    combined = l1 | l2
                    if len(combined) == size * 2:
                        is_valid_loop = True
                        for coord in combined:
                            nb = self._get_neighbors(coord)
                            # Проверяем, что у каждого элемента группы есть нужный сосед в этой же группе
                            if len(nb & combined) < power + 1:
                                is_valid_loop = False
                                break

                        if is_valid_loop and combined not in next_loops:
                            next_loops.append(combined)
            current_loops = next_loops

        prime_loops = []
        for loop in sorted(all_valid_loops, key=len, reverse=True):
            if not any(loop < super_loop for super_loop in prime_loops):
                prime_loops.append(loop)

        return prime_loops

    def _convert_loop_to_string(self, loop, coord_to_term, is_dnf=True):
        terms = [coord_to_term[coord] for coord in loop]
        bin_terms = [format(t, f'0{self.n}b') for t in terms]

        result_literals = []
        for bit_idx in range(self.n):
            bits_at_pos = {b[bit_idx] for b in bin_terms}
            if len(bits_at_pos) == 1:
                bit = bits_at_pos.pop()
                var_name = self.vars[bit_idx]

                if is_dnf:
                    result_literals.append(var_name if bit == '1' else f"!{var_name}")
                else:
                    result_literals.append(var_name if bit == '0' else f"!{var_name}")

        if not result_literals:
            return "1" if is_dnf else "0"

        return ("&".join(result_literals)) if is_dnf else ("|".join(result_literals))

    def _minimize_by_karnaugh(self, is_dnf=True):
        # Строим общую структуру
        _, _, _, coord_to_term = self._get_map_structure()

        # Четко фильтруем целевые координаты: для ДНФ ищем минтермы, для КНФ — макстермы
        target_terms = self.minterms if is_dnf else self.maxterms
        target_coords = [coord for coord, term in coord_to_term.items() if term in target_terms]

        if not target_coords:
            return "0" if is_dnf else "1", None
        if len(target_coords) == (2 ** self.n):
            return "1" if is_dnf else "0", None

        # Ищем склейки
        prime_loops = self._find_karnaugh_loops(target_coords)

        # Выбираем обязательные петли
        essential_loops = []
        uncovered_coords = set(target_coords)

        for coord in target_coords:
            covering_loops = [loop for loop in prime_loops if coord in loop]
            if len(covering_loops) == 1:
                el = covering_loops[0]
                if el not in essential_loops:
                    essential_loops.append(el)

        for el in essential_loops:
            uncovered_coords -= el

        final_loops = essential_loops[:]

        # Жадное покрытие остатков
        while uncovered_coords:
            best_loop = None
            best_cover_count = -1

            for loop in prime_loops:
                cover_count = len(loop & uncovered_coords)
                if cover_count > best_cover_count:
                    best_cover_count = cover_count
                    best_loop = loop

            if best_loop is None or best_cover_count == 0:
                break

            final_loops.append(best_loop)
            uncovered_coords -= best_loop

        # Собираем строковый ответ
        strings = []
        for loop in final_loops:
            s = self._convert_loop_to_string(loop, coord_to_term, is_dnf)
            if s not in strings:
                strings.append(s)

        if is_dnf:
            result = ' | '.join(strings)
        else:
            result = ' & '.join([f"({x})" for x in strings])

        return result

    def minimize_dnf(self):
        return self._minimize_by_karnaugh(is_dnf=True), None

    def minimize_cnf(self):
        return self._minimize_by_karnaugh(is_dnf=False), None

    def print_karnaugh_dnf(self):
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ ДНФ (МЕТОД КАРТ КАРНО)")
        print("=" * 60)

        result, _ = self.minimize_dnf()

        if self.n == 5:
            maps, row_labels, col_labels, layer_var = self._build_map(True)
            self._print_map(f"Карта Карно (единицы) {layer_var}=0", row_labels, col_labels, maps[0])
            self._print_map(f"Карта Карно (единицы) {layer_var}=1", row_labels, col_labels, maps[1])
        else:
            k, row_labels, col_labels, _ = self._build_map(True)
            self._print_map("Карта Карно (единицы)", row_labels, col_labels, k)

        print(f"\nРезультат: {result}")
        return result

    def print_karnaugh_cnf(self):
        print("\n" + "=" * 60)
        print("МИНИМИЗАЦИЯ КНФ (МЕТОД КАРТ КАРНО)")
        print("=" * 60)

        result, _ = self.minimize_cnf()

        if self.n == 5:
            maps, row_labels, col_labels, layer_var = self._build_map(False)
            self._print_map(f"Карта Карно (нули) {layer_var}=0", row_labels, col_labels, maps[0])
            self._print_map(f"Карта Карно (нули) {layer_var}=1", row_labels, col_labels, maps[1])
        else:
            k, row_labels, col_labels, _ = self._build_map(False)
            self._print_map("Карта Карно (нули)", row_labels, col_labels, k)

        print(f"\nРезультат: {result}")
        return result