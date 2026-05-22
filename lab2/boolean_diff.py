# boolean_diff.py (исправленная версия с обработкой ошибок)
"""Булева дифференциация (частные и смешанные производные)"""

from itertools import combinations
import math


class BooleanDifferentiation:
    """Булева дифференциация"""

    def __init__(self, truth_table):
        self.tt = truth_table
        self.variables = truth_table.variables
        self.var_count = truth_table.var_count
        self.vector = truth_table.get_vector()
        self.n = self.var_count
        self.size = 1 << self.n

    def _get_mask(self, var_idx: int, current_n: int = None) -> int:
        """Возвращает маску для переменной"""
        if current_n is None:
            current_n = self.n
        if current_n - 1 - var_idx < 0:
            return 0
        return 1 << (current_n - 1 - var_idx)

    def derivative(self, *variables) -> list:
        """
        Вычисляет производную по указанным переменным

        Args:
            *variables: имена переменных (например, 'a', 'b')

        Returns:
            вектор производной
        """
        if not variables:
            return self.vector.copy()

        # Находим индексы переменных
        try:
            indices = [self.variables.index(v) for v in variables]
        except ValueError as e:
            print(f"Ошибка: переменная {e} не найдена")
            return []

        indices.sort()

        # Начинаем с функции
        current = self.vector.copy()
        current_n = self.n
        current_vars = self.variables.copy()

        # Последовательно берем производные
        for idx in indices:
            # Находим актуальный индекс в текущем наборе переменных
            var_name = self.variables[idx]
            if var_name in current_vars:
                current_idx = current_vars.index(var_name)
                current, current_n = self._derivative_of_vector(current, current_idx, current_n)
                # Удаляем переменную из списка
                current_vars.pop(current_idx)
            else:
                # Переменная уже была удалена (производная по ней равна 0)
                return [0] * (1 << max(0, current_n - 1))

            if current_n == 0:
                break

        return current

    def _derivative_of_vector(self, vector: list, var_idx: int, current_n: int) -> tuple:
        """
        Вычисляет производную вектора по переменной

        Args:
            vector: текущий вектор
            var_idx: индекс переменной в текущем пространстве
            current_n: текущее количество переменных

        Returns:
            tuple: (новый вектор, новое количество переменных)
        """
        if current_n <= 0:
            return [0], 0

        if current_n == 1:
            # Для одной переменной производная - это разность
            if len(vector) >= 2:
                return [vector[0] ^ vector[1]], 0
            return [0], 0

        if var_idx >= current_n:
            return [0] * (1 << (current_n - 1)), current_n - 1

        new_n = current_n - 1
        new_size = 1 << new_n
        result = [0] * new_size

        # Находим шаг для группировки пар
        step = 1 << (current_n - 1 - var_idx)

        # Группируем пары
        for i in range(0, len(vector), step * 2):
            for j in range(step):
                idx1 = i + j
                idx2 = i + j + step
                if idx1 < len(vector) and idx2 < len(vector):
                    out_idx = idx1 // 2
                    if out_idx < new_size:
                        result[out_idx] = vector[idx1] ^ vector[idx2]

        return result, new_n

    def partial_derivative_vector(self, var_name: str) -> list:
        """
        Возвращает вектор частной производной по переменной
        """
        if var_name not in self.variables:
            return []

        var_idx = self.variables.index(var_name)
        step = 1 << (self.n - 1 - var_idx)
        result = []

        for i in range(0, self.size, step * 2):
            for j in range(step):
                idx1 = i + j
                idx2 = i + j + step
                if idx2 < self.size:
                    result.append(self.vector[idx1] ^ self.vector[idx2])

        return result

    def mixed_derivative(self, *variables) -> list:
        """
        Смешанная производная по нескольким переменным
        """
        if not variables:
            return self.vector.copy()

        # Проверяем, что все переменные существуют
        for var in variables:
            if var not in self.variables:
                return []

        return self.derivative(*variables)

    def print_derivatives(self, max_vars: int = 4):
        """Выводит производные до указанного порядка"""
        print("\n" + "=" * 60)
        print("БУЛЕВА ДИФФЕРЕНЦИАЦИЯ")
        print("=" * 60)

        # Частные производные первого порядка
        print("\nЧастные производные первого порядка:")
        for var in self.variables:
            deriv = self.partial_derivative_vector(var)
            if deriv:
                ones = [i for i, val in enumerate(deriv) if val]
                if ones:
                    print(f"  ∂f/∂{var}: наборы остальных переменных: {ones}")
                else:
                    print(f"  ∂f/∂{var}: 0 (функция не зависит от {var})")
            else:
                print(f"  ∂f/∂{var}: 0")

        # Смешанные производные высших порядков
        if len(self.variables) >= 2 and max_vars >= 2:
            print("\nСмешанные производные:")
            for r in range(2, min(max_vars, len(self.variables)) + 1):
                for vars_combo in combinations(self.variables, r):
                    try:
                        # Проверяем, что все переменные различны
                        if len(set(vars_combo)) != len(vars_combo):
                            continue

                        deriv = self.mixed_derivative(*vars_combo)
                        if deriv:
                            ones = [i for i, val in enumerate(deriv) if val]
                            if ones:
                                remaining = [v for v in self.variables if v not in vars_combo]
                                if remaining:
                                    print(
                                        f"  ∂^{r}f/∂{'∂'.join(vars_combo)}: наборы ({', '.join(remaining)}) -> {ones}")
                                else:
                                    print(f"  ∂^{r}f/∂{'∂'.join(vars_combo)}: {ones}")
                            else:
                                print(f"  ∂^{r}f/∂{'∂'.join(vars_combo)}: 0")
                        else:
                            print(f"  ∂^{r}f/∂{'∂'.join(vars_combo)}: 0")
                    except Exception as e:
                        print(f"  ∂^{r}f/∂{'∂'.join(vars_combo)}: 0 ({e})")

    def check_dependence(self, var_name: str) -> bool:
        """Проверяет, зависит ли функция от переменной"""
        deriv = self.partial_derivative_vector(var_name)
        return any(deriv)

    def derivative_numeric_form(self, *variables) -> str:
            """
            Возвращает числовую форму производной
            """
            deriv = self.derivative(*variables)
            if not deriv:
                return "0"

            # Находим номера наборов, где производная = 1
            ones = [i for i, val in enumerate(deriv) if val]

            if not ones:
                return "0"

            remaining_vars = [v for v in self.variables if v not in variables]
            if remaining_vars:
                return f"∂{''.join(variables)}f: {remaining_vars} ({', '.join(map(str, ones))})"
            else:
                return f"∂{''.join(variables)}f: ({', '.join(map(str, ones))})"