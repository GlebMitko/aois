# tests/run_tests.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_tests():
    """Запуск тестов с измерением покрытия"""

    try:
        import coverage

        # Запускаем coverage
        cov = coverage.Coverage(
            source=['.'],
            omit=[
                'tests/*',
                'run_tests.py',
                'main.py',
                'logisim_export.py',
                '*/__pycache__/*'
            ]
        )
        cov.start()

        # Загружаем и запускаем тесты
        loader = unittest.TestLoader()
        start_dir = os.path.dirname(os.path.abspath(__file__))
        suite = loader.discover(start_dir, pattern="test_*.py")

        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        # Останавливаем coverage
        cov.stop()
        cov.save()

        # Статистика тестов
        print(f"\n{'=' * 60}")
        print("СТАТИСТИКА ТЕСТОВ")
        print(f"{'=' * 60}")
        print(f"Выполнено тестов: {result.testsRun}")
        print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"Ошибок: {len(result.errors)}")
        print(f"Провалено: {len(result.failures)}")

        # Отчет о покрытии
        print(f"\n{'=' * 60}")
        print("ОТЧЕТ О ПОКРЫТИИ КОДА")
        print(f"{'=' * 60}")
        cov.report(show_missing=True)

        total = cov.report(show_missing=False)

        print(f"\n{'=' * 60}")
        if total >= 90:
            print(f"✅ ПОКРЫТИЕ {total:.1f}% - ЦЕЛЬ ДОСТИГНУТА (>=90%)")
        else:
            print(f"❌ ПОКРЫТИЕ {total:.1f}% - НУЖНО БОЛЬШЕ ТЕСТОВ (цель 90%)")
        print(f"{'=' * 60}")

        # Генерируем HTML отчет
        cov.html_report(directory='htmlcov')
        print("\n📊 HTML отчет создан в папке 'htmlcov'")
        print("   Откройте htmlcov/index.html в браузере")

        return result.wasSuccessful()

    except ImportError:
        print("❌ Библиотека 'coverage' не установлена.")
        print("   Установите: pip install coverage")
        print("\nЗапуск тестов без измерения покрытия...\n")

        loader = unittest.TestLoader()
        start_dir = os.path.dirname(os.path.abspath(__file__))
        suite = loader.discover(start_dir, pattern="test_*.py")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)