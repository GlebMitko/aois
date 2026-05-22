# fictitious_vars.py
"""Поиск фиктивных переменных"""


class FictitiousVariables:
    """Класс для поиска фиктивных переменных"""

    def __init__(self, truth_table):
        self.tt = truth_table
        self.variables = truth_table.variables
        self.var_count = truth_table.var_count
        self.vector = truth_table.get_vector()

    def find_fictitious(self) -> list:
        """
        Находит все фиктивные переменные

        Returns:
            список фиктивных переменных
        """
        fictitious = []
        for var_idx in range(self.var_count):
            if self._is_fictitious(var_idx):
                fictitious.append(self.variables[var_idx])
        return fictitious

    def _is_fictitious(self, var_idx: int) -> bool:
        """
        Проверяет, является ли переменная фиктивной

        Переменная фиктивна, если значение функции не зависит от неё
        """
        n = self.var_count
        size = 1 << n

        # Для всех пар наборов, отличающихся только этой переменной
        for i in range(size):
            # Набор, где переменная = 0
            mask0 = i & ~(1 << (n - 1 - var_idx))
            # Набор, где переменная = 1
            mask1 = i | (1 << (n - 1 - var_idx))

            # Если наборы различны (не выходим за пределы)
            if mask0 != mask1:
                if self.vector[mask0] != self.vector[mask1]:
                    return False

        return True

    def get_essential_variables(self) -> list:
        """Возвращает список существенных переменных"""
        fictitious = self.find_fictitious()
        return [v for v in self.variables if v not in fictitious]

    def print_result(self):
        """Вывод результатов поиска фиктивных переменных"""
        fictitious = self.find_fictitious()
        essential = self.get_essential_variables()

        print("\nФиктивные переменные:")
        if fictitious:
            print(f"  {', '.join(fictitious)}")
        else:
            print("  Нет фиктивных переменных")

        print("Существенные переменные:")
        print(f"  {', '.join(essential)}")