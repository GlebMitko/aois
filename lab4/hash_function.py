# hash_function.py
"""Хеш-функция из ЛР6 на основе первых двух букв (кириллица)"""


def char_to_num(c: str) -> int:
    """
    Преобразует букву в число (А=0, Б=1, ..., Я=32)
    """
    russian_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    c_upper = c.upper()
    if c_upper in russian_alphabet:
        return russian_alphabet.index(c_upper)
    return 0


def calculate_v(word: str) -> int:
    """
    Вычисляет числовое значение V по первым двум буквам
    V = код(1-й буквы) * 33^1 + код(2-й буквы) * 33^0
    """
    word = word.upper().strip()
    if len(word) == 0:
        return 0
    if len(word) == 1:
        return char_to_num(word[0]) * 33

    c1 = char_to_num(word[0])
    c2 = char_to_num(word[1])
    return c1 * 33 + c2


def hash_function(word: str, table_size: int, base: int = 0) -> int:
    """
    Хеш-функция: h(V) = V mod H + B
    где V - числовое значение, H - размер таблицы, B - начальный адрес
    """
    v = calculate_v(word)
    return (v % table_size) + base