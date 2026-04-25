"""Точка входа."""

from app.controller import AppController
from app.view.main_window import MainWindow


if __name__ == "__main__":
    controller = AppController()
    app = MainWindow(controller)
    app.mainloop()
