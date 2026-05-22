# run_tests.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_tests_with_coverage():
    """Запускает тесты с измерением покрытия"""

    try:
        import coverage

        # Исключаем main.py и другие вспомогательные файлы
        cov = coverage.Coverage(
            source=['.'],
            omit=[
                'tests/*',
                'run_tests.py',
                'test_functions.py',
                'interactive.py',
                'main.py',  # Исключаем main.py
                '*/__pycache__/*',
                '*/.pytest_cache/*',
                'show_coverage.py'
            ]
        )

        cov.start()

        # Загружаем все тесты
        loader = unittest.TestLoader()
        start_dir = os.path.join(os.path.dirname(__file__), 'tests')
        suite = loader.discover(start_dir, pattern='test_*.py')

        runner = unittest.TextTestRunner(verbosity=1)
        result = runner.run(suite)

        cov.stop()
        cov.save()

        print("\n" + "=" * 70)
        print("СТАТИСТИКА ТЕСТОВ")
        print("=" * 70)
        print(f"Выполнено тестов: {result.testsRun}")
        print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"Ошибок: {len(result.errors)}")
        print(f"Провалено: {len(result.failures)}")

        print("\n" + "=" * 70)
        print("ОТЧЕТ О ПОКРЫТИИ КОДА")
        print("=" * 70)
        cov.report(show_missing=True)

        total = cov.report(show_missing=False)

        print("\n" + "=" * 70)
        if total >= 90:
            print(f"✅ ПОКРЫТИЕ {total:.1f}% - ЦЕЛЬ ДОСТИГНУТА (>=90%)")
        else:
            print(f"❌ ПОКРЫТИЕ {total:.1f}% - НУЖНО БОЛЬШЕ ТЕСТОВ (цель 90%)")
        print("=" * 70)

        cov.html_report(directory='htmlcov')
        print("\n📊 HTML отчет создан в папке 'htmlcov'")

        return result.wasSuccessful()

    except ImportError:
        print("❌ Библиотека 'coverage' не установлена.")
        print("   Установите ее: pip install coverage")

        loader = unittest.TestLoader()
        start_dir = os.path.join(os.path.dirname(__file__), 'tests')
        suite = loader.discover(start_dir, pattern='test_*.py')
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests_with_coverage()
    sys.exit(0 if success else 1)