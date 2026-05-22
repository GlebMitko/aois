# post_classes.py
"""Определение принадлежности функции к классам Поста"""


class PostClasses:
    """Классы Поста для булевых функций"""

    def __init__(self, truth_table):
        self.tt = truth_table
        self.var_count = truth_table.var_count
        self.vector = truth_table.get_vector()

    def is_t0(self) -> bool:
        """Проверка принадлежности к классу T0 (константа 0)"""
        return self.vector[0] == 0

    def is_t1(self) -> bool:
        """Проверка принадлежности к классу T1 (константа 1)"""
        return self.vector[-1] == 1

    def is_s(self) -> bool:
        """Проверка принадлежности к классу S (самодвойственная)"""
        n = len(self.vector)
        for i in range(n // 2):
            if self.vector[i] == self.vector[n - 1 - i]:
                return False
        return True

    def is_m(self) -> bool:
        """Проверка принадлежности к классу M (монотонная)"""
        size = len(self.vector)
        n = self.var_count

        for i in range(size):
            for j in range(size):
                if i != j and self._less_or_equal(i, j, n):
                    if self.vector[i] == 1 and self.vector[j] == 0:
                        return False
        return True

    def _less_or_equal(self, idx1: int, idx2: int, n: int) -> bool:
        """Проверяет, что все биты idx1 <= соответствующих битов idx2"""
        for bit in range(n):
            val1 = (idx1 >> (n - 1 - bit)) & 1
            val2 = (idx2 >> (n - 1 - bit)) & 1
            if val1 > val2:
                return False
        return True

    def is_l(self) -> bool:
        """Проверка принадлежности к классу L (линейная)"""
        coefficients = self._build_zhegalkin_coefficients()
        n = self.var_count
        for i in range(1 << n):
            # Проверяем, что коэффициент при произведении (не одной переменной) равен 0
            if i > 0 and (i & (i - 1)) != 0:  # Не степень двойки
                if coefficients[i] == 1:
                    return False
        return True

    def _build_zhegalkin_coefficients(self) -> list:
        """Построение коэффициентов полинома Жегалкина"""
        n = self.var_count
        size = 1 << n
        coeff = self.vector.copy()

        for i in range(n):
            step = 1 << i
            for j in range(size):
                if j & (1 << i):
                    coeff[j] ^= coeff[j ^ (1 << i)]

        return coeff

    def get_classes(self) -> dict:
        """Возвращает словарь с принадлежностью ко всем классам"""
        return {
            'T0': self.is_t0(),
            'T1': self.is_t1(),
            'S': self.is_s(),
            'M': self.is_m(),
            'L': self.is_l()
        }

    def print_classes(self):
        """Вывод принадлежности к классам Поста"""
        classes = self.get_classes()
        print("\nПринадлежность к классам Поста:")
        for name, belongs in classes.items():
            print(f"  {name}: {'Да' if belongs else 'Нет'}")