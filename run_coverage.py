"""Подсчёт покрытия тестами с сохранением отчёта в coverage_report.txt."""

from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path

from coverage import Coverage

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

INCLUDE = [
    "app/*.py",
    "app/model/*.py",
    "app/view/*.py",
]

if __name__ == "__main__":
    cov = Coverage(include=INCLUDE)
    cov.start()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    cov.stop()
    cov.save()

    buffer = io.StringIO()
    total = cov.report(include=INCLUDE, show_missing=True, file=buffer)
    report_text = buffer.getvalue() + f"\nИтоговое покрытие: {total:.2f}%\n"
    (ROOT / "coverage_report.txt").write_text(report_text, encoding="utf-8")
    print(report_text)
    raise SystemExit(0 if result.wasSuccessful() and total >= 90 else 1)
