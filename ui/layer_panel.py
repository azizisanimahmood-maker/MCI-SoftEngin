from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QHBoxLayout
)


class LayerPanel(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMinimumWidth(220)

        self.layer_list = QListWidget()

        self.btn_add = QPushButton("Add")

        self.btn_remove = QPushButton("Remove")

        buttons = QHBoxLayout()

        buttons.addWidget(self.btn_add)

        buttons.addWidget(self.btn_remove)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Layers"))

        layout.addWidget(self.layer_list)

        layout.addLayout(buttons)

        self.setLayout(layout)

    def add_layer(self, name):

        self.layer_list.addItem(name)

    def remove_current(self):

        row = self.layer_list.currentRow()

        if row >= 0:

            self.layer_list.takeItem(row)

    def current_layer(self):

        item = self.layer_list.currentItem()

        if item:

            return item.text()

        return None

    def clear(self):

        self.layer_list.clear()
