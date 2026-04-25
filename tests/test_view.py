from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.controller import AppController
from app.view import main_window as mw


class DummyWidget:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.children = []
        self.last_delete = None
        self.inserted = ""

    def pack(self, *args, **kwargs):
        self.pack_args = (args, kwargs)
        return self

    def grid(self, *args, **kwargs):
        self.grid_args = (args, kwargs)
        return self

    def add(self, child, **kwargs):
        self.children.append((child, kwargs))

    def delete(self, *args):
        self.last_delete = args

    def insert(self, *args):
        self.inserted = args[-1]


class DummyNotebook(DummyWidget):
    pass


class DummyStringVar:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class ViewTests(unittest.TestCase):
    def make_window(self):
        window = object.__new__(mw.MainWindow)
        window.controller = AppController()
        return window

    def test_init_builds_ui(self) -> None:
        with (
            patch.object(mw.tk.Tk, "__init__", lambda self: None),
            patch.object(mw.tk.Tk, "title", lambda self, text: None),
            patch.object(mw.tk.Tk, "geometry", lambda self, text: None),
            patch.object(mw.tk.Tk, "minsize", lambda self, w, h: None),
            patch.object(mw.MainWindow, "_build_ui", lambda self: setattr(self, "built", True)),
        ):
            window = mw.MainWindow(AppController())
            self.assertTrue(window.built)

    def test_make_and_set_output(self) -> None:
        window = self.make_window()
        with patch.object(mw.tk, "Text", DummyWidget):
            output = window._make_output(DummyWidget())
            window._set_output(output, "hello")
            self.assertEqual(output.inserted, "hello")

    def test_safe_action_success(self) -> None:
        window = self.make_window()
        output = DummyWidget()
        window._safe_action(lambda: "ok", output)
        self.assertEqual(output.inserted, "ok")

    def test_safe_action_error(self) -> None:
        window = self.make_window()
        output = DummyWidget()
        with patch.object(mw.messagebox, "showerror") as showerror:
            window._safe_action(lambda: (_ for _ in ()).throw(ValueError("boom")), output)
            showerror.assert_called_once()

    def test_build_ui(self) -> None:
        window = self.make_window()
        with (
            patch.object(mw.ttk, "Notebook", DummyNotebook),
            patch.object(window, "_build_codes_tab", lambda notebook: DummyWidget()),
            patch.object(window, "_build_integer_ops_tab", lambda notebook: DummyWidget()),
            patch.object(window, "_build_float_tab", lambda notebook: DummyWidget()),
            patch.object(window, "_build_bcd_tab", lambda notebook: DummyWidget()),
        ):
            window._build_ui()

    def test_build_codes_tab(self) -> None:
        window = self.make_window()
        with (
            patch.object(mw.ttk, "Frame", DummyWidget),
            patch.object(mw.ttk, "Label", DummyWidget),
            patch.object(mw.ttk, "Entry", DummyWidget),
            patch.object(mw.ttk, "Button", DummyWidget),
            patch.object(mw.tk, "StringVar", DummyStringVar),
            patch.object(mw.MainWindow, "_make_output", lambda self, parent: DummyWidget()),
        ):
            tab = window._build_codes_tab(DummyNotebook())
            self.assertIsInstance(tab, DummyWidget)

    def test_build_integer_ops_tab(self) -> None:
        window = self.make_window()
        with (
            patch.object(mw.ttk, "Frame", DummyWidget),
            patch.object(mw.ttk, "Label", DummyWidget),
            patch.object(mw.ttk, "Entry", DummyWidget),
            patch.object(mw.ttk, "Button", DummyWidget),
            patch.object(mw.tk, "StringVar", DummyStringVar),
            patch.object(mw.MainWindow, "_make_output", lambda self, parent: DummyWidget()),
        ):
            tab = window._build_integer_ops_tab(DummyNotebook())
            self.assertIsInstance(tab, DummyWidget)

    def test_build_float_tab(self) -> None:
        window = self.make_window()
        with (
            patch.object(mw.ttk, "Frame", DummyWidget),
            patch.object(mw.ttk, "Label", DummyWidget),
            patch.object(mw.ttk, "Entry", DummyWidget),
            patch.object(mw.ttk, "Button", DummyWidget),
            patch.object(mw.tk, "StringVar", DummyStringVar),
            patch.object(mw.MainWindow, "_make_output", lambda self, parent: DummyWidget()),
        ):
            tab = window._build_float_tab(DummyNotebook())
            self.assertIsInstance(tab, DummyWidget)

    def test_build_bcd_tab(self) -> None:
        window = self.make_window()
        with (
            patch.object(mw.ttk, "Frame", DummyWidget),
            patch.object(mw.ttk, "Label", DummyWidget),
            patch.object(mw.ttk, "Entry", DummyWidget),
            patch.object(mw.ttk, "Button", DummyWidget),
            patch.object(mw.ttk, "Combobox", DummyWidget),
            patch.object(mw.tk, "StringVar", DummyStringVar),
            patch.object(mw.MainWindow, "_make_output", lambda self, parent: DummyWidget()),
        ):
            tab = window._build_bcd_tab(DummyNotebook())
            self.assertIsInstance(tab, DummyWidget)


if __name__ == "__main__":
    unittest.main()
