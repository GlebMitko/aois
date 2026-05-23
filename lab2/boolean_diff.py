# boolean_diff.py
"""Булева дифференциация (частные и смешанные производные)"""

from itertools import combinations
from truth_table import TruthTable


class BooleanDifferentiation:
    """Булева дифференциация"""

    def __init__(self, truth_table):
        self.tt = truth_table
        self.variables = truth_table.variables
        self.var_count = truth_table.var_count
        self.vector = truth_table.get_vector()

    def _vector_to_formula(self, vector: list, remaining_vars: list) -> str:
        """Преобразует вектор производной в логическую формулу"""
        if not vector:
            return "0"

        minterms = [i for i, val in enumerate(vector) if val == 1]
        if not minterms:
            return "0"
        if len(minterms) == len(vector):
            return "1"

        terms = []
        for mt in minterms:
            bits = []
            for i in range(len(remaining_vars)):
                bit = (mt >> (len(remaining_vars) - 1 - i)) & 1
                if bit == 1:
                    bits.append(remaining_vars[i])
                else:
                    bits.append(f"!{remaining_vars[i]}")
            terms.append('&'.join(bits))

        if len(terms) == 1:
            return terms[0]
        return ' | '.join(terms)

    def derivative(self, *variables) -> str:
        """Возвращает формулу производной по указанным переменным"""
        if not variables:
            return self._vector_to_formula(self.vector, self.variables)

        try:
            indices = [self.variables.index(v) for v in variables]
        except ValueError:
            return "0"
        indices.sort()

        remaining = [v for v in self.variables if v not in variables]

        current = self.vector.copy()
        current_n = self.var_count
        current_vars = self.variables.copy()

        for idx in indices:
            if current_n <= 1:
                return "0"

            # Находим актуальный индекс в текущем наборе переменных
            var_name = self.variables[idx]
            if var_name in current_vars:
                current_idx = current_vars.index(var_name)
            else:
                return "0"

            step = 1 << (current_n - 1 - current_idx)
            new_vector = []
            for i in range(0, len(current), step * 2):
                for j in range(step):
                    if i + j + step < len(current):
                        new_vector.append(current[i + j] ^ current[i + j + step])
            current = new_vector
            current_n -= 1
            current_vars.pop(current_idx)

        if current_n == 0:
            return str(current[0]) if current else "0"

        return self._vector_to_formula(current, remaining)

    def partial_derivative(self, var_name: str) -> str:
        """Частная производная по переменной"""
        return self.derivative(var_name)

    def mixed_derivative(self, *variables) -> str:
        """Смешанная производная"""
        return self.derivative(*variables)

    def print_derivatives(self):
        """Вывод всех производных"""
        print("\n" + "=" * 60)
        print("БУЛЕВА ДИФФЕРЕНЦИАЦИЯ")
        print("=" * 60)

        if self.var_count == 0:
            print("Нет переменных для дифференциации")
            return

        print("\nЧастные производные первого порядка:")
        for var in self.variables:
            deriv = self.partial_derivative(var)
            print(f"  ∂f/∂{var} = {deriv}")

        if self.var_count >= 2:
            print("\nСмешанные производные второго порядка:")
            for v1, v2 in combinations(self.variables, 2):
                try:
                    deriv = self.mixed_derivative(v1, v2)
                    print(f"  ∂²f/∂{v1}∂{v2} = {deriv}")
                except:
                    print(f"  ∂²f/∂{v1}∂{v2} = 0")

        if self.var_count >= 3:
            print("\nСмешанные производные третьего порядка:")
            for v1, v2, v3 in combinations(self.variables, 3):
                try:
                    deriv = self.mixed_derivative(v1, v2, v3)
                    print(f"  ∂³f/∂{v1}∂{v2}∂{v3} = {deriv}")
                except:
                    print(f"  ∂³f/∂{v1}∂{v2}∂{v3} = 0")