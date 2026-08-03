from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit
)


class CommandLine(QWidget):

    commandEntered = Signal(str)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.label = QLabel("Command:")

        self.edit = QLineEdit()

        self.edit.returnPressed.connect(
            self._send_command
        )

        layout = QHBoxLayout()

        layout.addWidget(self.label)

        layout.addWidget(self.edit)

        self.setLayout(layout)

    def _send_command(self):

        text = self.edit.text().strip()

        if text:

            self.commandEntered.emit(text)

        self.edit.clear()

    def set_prompt(self, text):

        self.label.setText(text)

    def set_text(self, text):

        self.edit.setText(text)

    def text(self):

        return self.edit.text()

    def clear(self):

        self.edit.clear()

    def focus(self):

        self.edit.setFocus()