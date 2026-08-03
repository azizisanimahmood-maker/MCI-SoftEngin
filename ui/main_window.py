from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout
)

from ui.canvas import Canvas


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("MCI SoftEngine")

        self.resize(1600, 900)

        self.canvas = Canvas()

        self._build_ui()

    def _build_ui(self):

        central = QWidget()

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.canvas)

        central.setLayout(layout)

        self.setCentralWidget(central)

    def set_renderer(self, renderer):

        self.canvas.set_renderer(renderer)

    def set_entities(self, entities):

        self.canvas.set_entities(entities)