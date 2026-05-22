# main.py
"""Главный файл для работы с хеш-таблицей"""

import sys
from hash_table import HashTable
from data import INITIAL_DATA, TEST_KEYS


def print_menu():
    print("\n" + "=" * 70)
    print("ХЕШ-ТАБЛИЦА. ТЕМАТИКА: ГЕОГРАФИЯ (ВАРИАНТ 3)")
    print("Метод разрешения коллизий: линейный поиск")
    print("=" * 70)
    print("1. Показать хеш-таблицу")
    print("2. Найти запись по ключу")
    print("3. Добавить новую запись")
    print("4. Обновить данные по ключу")
    print("5. Удалить запись")
    print("6. Показать вычисленные значения V и h для всех ключей")
    print("7. Коэффициент заполнения и статистика")
    print("0. Выход")
    print("-" * 70)


def main():
    # Создаем хеш-таблицу (H=20, B=0)
    ht = HashTable(size=20, base=0)

    print("\n" + "=" * 70)
    print("ЗАГРУЗКА НАЧАЛЬНЫХ ДАННЫХ (ГЕОГРАФИЯ)")
    print("=" * 70)

    # Загружаем начальные данные
    for key, data in INITIAL_DATA:
        success = ht.insert(key, data)
        if success:
            v = ht._hash(key)  # это h, для показа
            print(f"  Добавлено: {key:20} -> h={v}")
        else:
            print(f"  ОШИБКА: {key} не добавлен")

    print(f"\nЗагружено записей: {ht.entries_count}")
    print(f"Коллизий: {ht.collisions_count}")

    # Демонстрация поиска для тестовых ключей
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ ПОИСКА")
    print("=" * 70)
    for key in TEST_KEYS:
        ht.find(key)

    # Основной цикл
    while True:
        print_menu()
        choice = input("\nВыберите действие: ").strip()

        if choice == '0':
            print("\nДо свидания!")
            break

        elif choice == '1':
            ht.display()

        elif choice == '2':
            key = input("Введите ключевое слово для поиска: ").strip()
            ht.find(key)

        elif choice == '3':
            key = input("Введите новое ключевое слово: ").strip()
            data = input("Введите данные: ").strip()
            if ht.insert(key, data):
                print(f"Запись '{key}' добавлена")
            else:
                print(f"Не удалось добавить '{key}'")

        elif choice == '4':
            key = input("Введите ключевое слово для обновления: ").strip()
            new_data = input("Введите новые данные: ").strip()
            ht.update(key, new_data)

        elif choice == '5':
            key = input("Введите ключевое слово для удаления: ").strip()
            ht.delete(key)

        elif choice == '6':
            ht.show_v_h_table()

        elif choice == '7':
            fill_ratio = ht.entries_count / ht.size * 100
            print("\n" + "=" * 50)
            print("СТАТИСТИКА ХЕШ-ТАБЛИЦЫ")
            print("=" * 50)
            print(f"Размер таблицы (H): {ht.size}")
            print(f"Начальный адрес (B): {ht.base}")
            print(f"Занято ячеек: {ht.entries_count}")
            print(f"Свободно ячеек: {ht.size - ht.entries_count}")
            print(f"Коллизий: {ht.collisions_count}")
            print(f"Коэффициент заполнения: {fill_ratio:.1f}%")

        else:
            print("Неверный выбор. Введите число от 0 до 7.")


if __name__ == "__main__":
    main()