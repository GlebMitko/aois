"""Главное окно приложения."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from ..controller import AppController
from ..model.common import ValidationError


class MainWindow(tk.Tk):
    """Основное окно с вкладками по заданиям лабораторной работы."""

    def __init__(self, controller: AppController):
        super().__init__()
        self.controller = controller
        self.title("Лабораторная работа №1 — Представление чисел")
        self.geometry("1080x780")
        self.minsize(980, 700)
        self._build_ui()

    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        notebook.add(self._build_codes_tab(notebook), text="Коды")
        notebook.add(self._build_integer_ops_tab(notebook), text="Целочисленные операции")
        notebook.add(self._build_float_tab(notebook), text="IEEE-754")
        notebook.add(self._build_bcd_tab(notebook), text="BCD")

    def _make_output(self, parent: tk.Widget) -> tk.Text:
        output = tk.Text(parent, wrap=tk.WORD, height=18, font=("Consolas", 11))
        output.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        return output

    def _set_output(self, widget: tk.Text, text: str) -> None:
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)

    def _safe_action(self, action, output: tk.Text) -> None:
        try:
            self._set_output(output, action())
        except (ValueError, ValidationError, OverflowError, ZeroDivisionError) as exc:
            messagebox.showerror("Ошибка", str(exc))

    def _build_codes_tab(self, notebook: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook, padding=10)
        ttk.Label(frame, text="Десятичное целое число:").pack(anchor=tk.W)
        number_var = tk.StringVar(value="-13")
        ttk.Entry(frame, textvariable=number_var, width=30).pack(anchor=tk.W, pady=(0, 8))
        output = self._make_output(frame)
        ttk.Button(frame, text="Показать коды", command=lambda: self._safe_action(lambda: self.controller.integer_codes(number_var.get()), output)).pack(anchor=tk.W)
        return frame

    def _build_integer_ops_tab(self, notebook: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook, padding=10)
        inputs = ttk.Frame(frame)
        inputs.pack(fill=tk.X)
        left_var = tk.StringVar(value="12")
        right_var = tk.StringVar(value="-5")
        ttk.Label(inputs, text="A:").grid(row=0, column=0, sticky=tk.W, padx=(0, 4), pady=4)
        ttk.Entry(inputs, textvariable=left_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=4)
        ttk.Label(inputs, text="B:").grid(row=0, column=2, sticky=tk.W, padx=(14, 4), pady=4)
        ttk.Entry(inputs, textvariable=right_var, width=20).grid(row=0, column=3, sticky=tk.W, pady=4)
        output = self._make_output(frame)

        buttons = ttk.Frame(frame)
        buttons.pack(fill=tk.X, pady=8)
        ttk.Button(buttons, text="Сложить (доп. код)", command=lambda: self._safe_action(lambda: self.controller.integer_add(left_var.get(), right_var.get()), output)).pack(side=tk.LEFT, padx=4)
        ttk.Button(buttons, text="Вычесть (через -B и сложение)", command=lambda: self._safe_action(lambda: self.controller.integer_subtract(left_var.get(), right_var.get()), output)).pack(side=tk.LEFT, padx=4)
        ttk.Button(buttons, text="Умножить (прямой код)", command=lambda: self._safe_action(lambda: self.controller.integer_multiply(left_var.get(), right_var.get()), output)).pack(side=tk.LEFT, padx=4)
        ttk.Button(buttons, text="Разделить (прямой код)", command=lambda: self._safe_action(lambda: self.controller.integer_divide(left_var.get(), right_var.get()), output)).pack(side=tk.LEFT, padx=4)
        return frame

    def _build_float_tab(self, notebook: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook, padding=10)
        inputs = ttk.Frame(frame)
        inputs.pack(fill=tk.X)
        left_var = tk.StringVar(value="3.5")
        right_var = tk.StringVar(value="-1.25")
        ttk.Label(inputs, text="A:").grid(row=0, column=0, sticky=tk.W, padx=(0, 4), pady=4)
        ttk.Entry(inputs, textvariable=left_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=4)
        ttk.Label(inputs, text="B:").grid(row=0, column=2, sticky=tk.W, padx=(14, 4), pady=4)
        ttk.Entry(inputs, textvariable=right_var, width=20).grid(row=0, column=3, sticky=tk.W, pady=4)
        output = self._make_output(frame)

        buttons = ttk.Frame(frame)
        buttons.pack(fill=tk.X, pady=8)
        ttk.Button(buttons, text="Преобразовать A", command=lambda: self._safe_action(lambda: self.controller.float_convert(left_var.get()), output)).pack(side=tk.LEFT, padx=4)
        for operator in ["+", "-", "*", "/"]:
            ttk.Button(buttons, text=f"A {operator} B", command=lambda op=operator: self._safe_action(lambda: self.controller.float_operation(left_var.get(), right_var.get(), op), output)).pack(side=tk.LEFT, padx=4)
        return frame

    def _build_bcd_tab(self, notebook: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(notebook, padding=10)
        inputs = ttk.Frame(frame)
        inputs.pack(fill=tk.X)
        left_var = tk.StringVar(value="74")
        right_var = tk.StringVar(value="87")
        variant_var = tk.StringVar(value="8421")
        ttk.Label(inputs, text="A:").grid(row=0, column=0, sticky=tk.W, padx=(0, 4), pady=4)
        ttk.Entry(inputs, textvariable=left_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=4)
        ttk.Label(inputs, text="B:").grid(row=0, column=2, sticky=tk.W, padx=(14, 4), pady=4)
        ttk.Entry(inputs, textvariable=right_var, width=20).grid(row=0, column=3, sticky=tk.W, pady=4)
        ttk.Label(inputs, text="BCD-вариант:").grid(row=1, column=0, sticky=tk.W, padx=(0, 4), pady=4)
        ttk.Combobox(inputs, textvariable=variant_var, values=["8421", "2421", "5421", "EXCESS-3", "GRAY"], state="readonly", width=17).grid(row=1, column=1, sticky=tk.W, pady=4)
        output = self._make_output(frame)
        ttk.Button(frame, text="Сложить в BCD", command=lambda: self._safe_action(lambda: self.controller.bcd_add(left_var.get(), right_var.get(), variant_var.get()), output)).pack(anchor=tk.W, pady=8)
        return frame
