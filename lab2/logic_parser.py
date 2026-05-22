# logic_parser.py - полная исправленная версия
"""Парсер логических выражений без использования eval"""


class LogicParser:
    """Парсер логических выражений с операциями &, |, !, ->, ~"""

    def __init__(self, expression: str, variables: list = None):
        """
        Инициализация парсера

        Args:
            expression: логическое выражение в инфиксной форме
            variables: список переменных (если None, будут определены автоматически)
        """
        self.expression = expression.replace(' ', '')

        # Автоматическое определение переменных если не указаны
        if variables is None:
            variables = self._extract_variables()

        self.variables = sorted(list(set(variables)))
        self.var_to_idx = {v: i for i, v in enumerate(self.variables)}
        self.postfix = self._to_postfix()

    def _extract_variables(self) -> list:
        """Извлекает переменные из выражения"""
        vars_set = set()
        i = 0
        while i < len(self.expression):
            ch = self.expression[i]
            if ch.isalpha() and ch.islower():
                vars_set.add(ch)
            i += 1
        return list(vars_set)

    def _tokenize(self) -> list:
        """Разбивает выражение на токены"""
        tokens = []
        i = 0
        while i < len(self.expression):
            ch = self.expression[i]
            if ch == '!':
                tokens.append('!')
                i += 1
            elif ch == '&':
                tokens.append('&')
                i += 1
            elif ch == '|':
                tokens.append('|')
                i += 1
            elif ch == '~':
                tokens.append('~')
                i += 1
            elif ch == '(':
                tokens.append('(')
                i += 1
            elif ch == ')':
                tokens.append(')')
                i += 1
            elif ch == '-':
                if i + 1 < len(self.expression) and self.expression[i + 1] == '>':
                    tokens.append('->')
                    i += 2
                else:
                    raise ValueError("Неверный синтаксис импликации")
            elif ch.isalpha() and ch.islower():
                tokens.append(ch)
                i += 1
            else:
                i += 1  # Пропускаем неизвестные символы
        return tokens

    def _get_precedence(self, op: str) -> int:
        """Возвращает приоритет операции"""
        precedence = {
            '!': 4,
            '&': 3,
            '|': 2,
            '->': 1,
            '~': 0
        }
        return precedence.get(op, -1)

    def _is_operator(self, token: str) -> bool:
        """Проверяет, является ли токен оператором"""
        return token in ('!', '&', '|', '->', '~')

    def _to_postfix(self) -> list:
        """Преобразует инфиксную запись в постфиксную (ОПН)"""
        tokens = self._tokenize()
        output = []
        stack = []

        for token in tokens:
            # Операнд (переменная)
            if token in self.variables or (len(token) == 1 and token.isalpha() and token not in '!&|~'):
                output.append(token)
            # Левая скобка
            elif token == '(':
                stack.append(token)
            # Правая скобка
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
            # Оператор
            elif self._is_operator(token):
                while (stack and stack[-1] != '(' and
                       self._get_precedence(stack[-1]) >= self._get_precedence(token)):
                    output.append(stack.pop())
                stack.append(token)

        # Выталкиваем оставшиеся операторы
        while stack:
            output.append(stack.pop())

        return output

    def evaluate(self, values: list) -> int:
        """
        Вычисляет значение функции на заданном наборе значений

        Args:
            values: список значений переменных в порядке self.variables

        Returns:
            0 или 1
        """
        stack = []
        var_map = {self.variables[i]: values[i] for i in range(len(self.variables))}

        for token in self.postfix:
            # Переменная
            if token in var_map:
                stack.append(var_map[token])
            # Оператор НЕ (унарный)
            elif token == '!':
                if stack:
                    a = stack.pop()
                    stack.append(1 - a)
                else:
                    stack.append(0)
            # Бинарные операторы
            elif token in ('&', '|', '->', '~'):
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()

                    if token == '&':
                        stack.append(a & b)
                    elif token == '|':
                        stack.append(a | b)
                    elif token == '->':
                        # a -> b = !a | b
                        stack.append((1 - a) | b)
                    elif token == '~':
                        # a ~ b = a == b
                        stack.append(1 if a == b else 0)
                else:
                    stack.append(0)

        return stack[-1] if stack else 0


# Для тестирования
if __name__ == "__main__":
    # Тест двойного отрицания
    parser = LogicParser("!!a", ['a'])
    print(f"!!0 = {parser.evaluate([0])}")  # Должно быть 0
    print(f"!!1 = {parser.evaluate([1])}")  # Должно быть 1

    # Тест тройного отрицания
    parser2 = LogicParser("!!!a", ['a'])
    print(f"!!!0 = {parser2.evaluate([0])}")  # Должно быть 1
    print(f"!!!1 = {parser2.evaluate([1])}")  # Должно быть 0