# hash_table.py
"""Хеш-таблица с линейным разрешением коллизий (линейный поиск)"""

from typing import Any, Optional, List, Dict, Tuple
from hash_function import calculate_v, hash_function


class HashTableEntry:
    """
    Структура ячейки хеш-таблицы (согласно рисунку 1 из ЛР6):

    ID - идентификатор ключевого слова (ключ)
    C  - флажок коллизий (1 если есть коллизия)
    U  - флажок занято (1 если ячейка занята)
    T  - терминальный флажок (1 если конец цепочки)
    L  - флажок связи (1 если Pi - указатель)
    D  - флажок вычеркивания (1 если удалена)
    Po - указатель области переполнения (адрес следующей записи)
    Pi - данные или указатель
    """

    def __init__(self, key: str = None, data: Any = None):
        self.id = key  # ID - ключевое слово
        self.c = 0  # C - флажок коллизий
        self.u = 1 if key is not None else 0  # U - флажок занято
        self.t = 1  # T - терминальный флажок
        self.l = 0  # L - флажок связи (0=данные, 1=указатель)
        self.d = 0  # D - флажок вычеркивания
        self.po = -1  # Po - указатель переполнения
        self.pi = data  # Pi - данные

    def to_dict(self) -> dict:
        """Преобразует запись в словарь для вывода"""
        return {
            'ID': self.id,
            'C': self.c,
            'U': self.u,
            'T': self.t,
            'L': self.l,
            'D': self.d,
            'Po': self.po if self.po != -1 else '-',
            'Pi': self.pi
        }

    def __str__(self) -> str:
        status = "ЗАНЯТО" if self.u else "СВОБОДНО"
        if self.d:
            status = "УДАЛЕНО"
        return f"ID: {self.id} | {status} | C={self.c} | T={self.t} | Po={self.po} | Pi={self.pi}"


class HashTable:
    """
    Хеш-таблица с линейным разрешением коллизий (линейный пробинг)

    При коллизии: последовательный поиск следующей свободной ячейки
    (index + 1) % size
    """

    def __init__(self, size: int = 20, base: int = 0):
        """
        size - размер таблицы (H)
        base - начальный адрес таблицы (B)
        """
        self.size = size
        self.base = base
        self.table: List[Optional[HashTableEntry]] = [None] * size
        self.entries_count = 0
        self.collisions_count = 0

    def _hash(self, key: str) -> int:
        """Вычисляет хеш-адрес для ключа"""
        return hash_function(key, self.size, self.base)

    def _linear_probe(self, start_index: int) -> int:
        """
        Линейный пробинг: поиск следующей свободной ячейки
        Возвращает индекс свободной ячейки или -1 если таблица заполнена
        """
        for i in range(self.size):
            idx = (start_index + i) % self.size
            entry = self.table[idx]
            if entry is None or entry.u == 0 or entry.d:
                return idx
        return -1

    def _find_chain_end(self, start_index: int) -> int:
        """Находит последнюю ячейку в цепочке"""
        current = start_index
        while current != -1 and self.table[current] and self.table[current].po != -1:
            current = self.table[current].po
        return current

    def insert(self, key: str, data: Any) -> bool:
        """
        Вставка новой записи в хеш-таблицу
        """
        # Проверка на дубликат
        if self.find(key, silent=True) is not None:
            print(f"Ошибка: ключ '{key}' уже существует")
            return False

        hash_addr = self._hash(key)
        original_hash = hash_addr

        # Если ячейка свободна
        entry = self.table[hash_addr]
        if entry is None or entry.u == 0 or entry.d:
            self.table[hash_addr] = HashTableEntry(key, data)
            self.table[hash_addr].t = 1
            self.table[hash_addr].po = -1
            self.entries_count += 1
            return True

        # Коллизия - ищем свободную ячейку
        self.collisions_count += 1
        free_index = self._linear_probe(hash_addr)

        if free_index == -1:
            print("Ошибка: таблица заполнена")
            return False

        # Устанавливаем флажок коллизии на исходной ячейке
        if self.table[hash_addr].c == 0:
            self.table[hash_addr].c = 1

        # Находим последнюю ячейку в цепочке
        last_index = self._find_chain_end(hash_addr)

        # Создаем новую запись
        self.table[free_index] = HashTableEntry(key, data)
        self.table[free_index].t = 1
        self.table[free_index].po = -1

        # Связываем с предыдущей
        if last_index != -1 and self.table[last_index]:
            self.table[last_index].t = 0
            self.table[last_index].po = free_index

        self.entries_count += 1
        return True

    def find(self, key: str, silent: bool = False) -> Optional[Tuple[int, HashTableEntry]]:
        """
        Поиск записи по ключу
        Возвращает (индекс, запись) или None
        """
        hash_addr = self._hash(key)

        # Проверяем цепочку начиная с хеш-адреса
        index = hash_addr
        visited = set()

        while index != -1 and index not in visited:
            visited.add(index)
            entry = self.table[index]

            if entry is not None and entry.u and not entry.d and entry.id == key:
                if not silent:
                    print(f"Найдено: индекс={index}, ID={entry.id}, Pi={entry.pi}")
                return index, entry

            # Переходим к следующему в цепочке
            if entry is not None:
                index = entry.po
            else:
                index = -1

        if not silent:
            print(f"Ключ '{key}' не найден")
        return None

    def update(self, key: str, new_data: Any) -> bool:
        """
        Обновление данных по ключу
        """
        result = self.find(key, silent=True)
        if result is None:
            print(f"Ошибка: ключ '{key}' не найден")
            return False

        index, entry = result
        entry.pi = new_data
        print(f"Данные для '{key}' обновлены")
        return True

    def delete(self, key: str) -> bool:
        """
        Удаление записи по ключу (устанавливается флажок D=1)
        """
        result = self.find(key, silent=True)
        if result is None:
            print(f"Ошибка: ключ '{key}' не найден")
            return False

        index, entry = result
        hash_addr = self._hash(key)

        # Устанавливаем флажок вычеркивания
        entry.d = 1
        entry.u = 0

        # Если это не первая ячейка в цепочке
        if index != hash_addr:
            # Ищем предыдущую ячейку
            prev_index = hash_addr
            while prev_index != -1 and self.table[prev_index] and self.table[prev_index].po != index:
                prev_index = self.table[prev_index].po if self.table[prev_index] else -1

            if prev_index != -1 and self.table[prev_index]:
                self.table[prev_index].po = entry.po
                if entry.po == -1:
                    self.table[prev_index].t = 1

        self.entries_count -= 1
        print(f"Запись с ключом '{key}' удалена")
        return True

    def display(self):
        """Вывод содержимого хеш-таблицы"""
        print("\n" + "=" * 110)
        print("ХЕШ-ТАБЛИЦА")
        print("=" * 110)
        print(f"{'№':^4} | {'ID':^18} | {'C':^3} | {'U':^3} | {'T':^3} | {'L':^3} | {'D':^3} | {'Po':^4} | {'Pi':^45}")
        print("-" * 110)

        for i, entry in enumerate(self.table):
            if entry is None or entry.u == 0:
                status = "СВОБОДНО"
                if entry and entry.d:
                    status = "УДАЛЕНО"
                print(
                    f"{i:^4} | {status:^18} | {'-':^3} | {entry.u if entry else 0:^3} | {'-':^3} | {'-':^3} | {(entry.d if entry else '-'):^3} | {'-':^4} | {'-':^45}")
            else:
                po = entry.po if entry.po != -1 else '-'
                pi = str(entry.pi)[:43] if entry.pi else '-'
                print(
                    f"{i:^4} | {entry.id:^18} | {entry.c:^3} | {entry.u:^3} | {entry.t:^3} | {entry.l:^3} | {entry.d:^3} | {po:^4} | {pi:^45}")

        print("-" * 110)
        fill_ratio = self.entries_count / self.size * 100
        print(f"Всего записей: {self.entries_count}/{self.size}")
        print(f"Коллизий: {self.collisions_count}")
        print(f"Коэффициент заполнения: {fill_ratio:.1f}%")

    def show_v_h_table(self):
        """Показывает вычисленные значения V и h для всех записей"""
        print("\n" + "=" * 60)
        print("ВЫЧИСЛЕННЫЕ ЗНАЧЕНИЯ V И H")
        print("=" * 60)
        print(f"{'Ключевое слово':^22} | {'V':^10} | {'h':^10}")
        print("-" * 50)

        for i, entry in enumerate(self.table):
            if entry and entry.u and not entry.d and entry.id:
                v = calculate_v(entry.id)
                h = hash_function(entry.id, self.size, self.base)
                print(f"{entry.id:^22} | {v:^10} | {h:^10}")

        print("-" * 50)
        print(f"Размер таблицы: {self.size}")
        print(f"Заполнено: {self.entries_count}")
        print(f"Свободно: {self.size - self.entries_count}")
        print(f"Коллизий: {self.collisions_count}")

    def get_all_entries(self) -> List[Dict]:
        """Возвращает все записи для отображения"""
        result = []
        for i, entry in enumerate(self.table):
            if entry and entry.u and not entry.d and entry.id:
                v = calculate_v(entry.id)
                h = hash_function(entry.id, self.size, self.base)
                result.append({
                    'index': i,
                    'key': entry.id,
                    'v': v,
                    'h': h,
                    'c': entry.c,
                    't': entry.t,
                    'po': entry.po,
                    'data': entry.pi
                })
        return result