# zhegalkin.py (исправленная версия)

class ZhegalkinPolynomial:
    """Полином Жегалкина булевой функции"""

    def __init__(self, truth_table):
        self.tt = truth_table
        self.variables = truth_table.variables
        self.var_count = truth_table.var_count
        self.vector = truth_table.get_vector()
        self.coefficients = self._build_coefficients()

    def _build_coefficients(self) -> list:
        """Построение коэффициентов полинома Жегалкина методом треугольника"""
        n = self.var_count
        size = 1 << n
        coeff = self.vector.copy()

        # Метод треугольника Паскаля (преобразование Мёбиуса)
        for i in range(n):
            step = 1 << i
            for j in range(size):
                if j & (1 << i):
                    coeff[j] ^= coeff[j ^ (1 << i)]

        return coeff

    def _int_to_binary(self, n: int, width: int) -> list:
        """Преобразует число в бинарный список"""
        return [int(x) for x in format(n, f'0{width}b')]

    def _term_to_string(self, mask: int) -> str:
        """Преобразует маску в строку терма"""
        if mask == 0:
            return "1"

        bits = self._int_to_binary(mask, self.var_count)
        terms = []
        for i, bit in enumerate(bits):
            if bit:
                terms.append(self.variables[i])

        if not terms:
            return "1"
        if len(terms) == 1:
            return terms[0]
        return '&'.join(terms)

    def build(self) -> str:
        """Построение полинома Жегалкина"""
        terms = []
        for i, coeff in enumerate(self.coefficients):
            if coeff:
                term = self._term_to_string(i)
                terms.append(term)

        if not terms:
            return "0"

        return ' ⊕ '.join(terms)

    def get_coefficients(self) -> dict:
        """Возвращает коэффициенты в виде словаря"""
        result = {}
        for i, coeff in enumerate(self.coefficients):
            if coeff:
                term = self._term_to_string(i)
                result[term] = coeff
        return result

    def print_polynomial(self):
        """Вывод полинома Жегалкина"""
        print(f"\nПолином Жегалкина: {self.build()}")