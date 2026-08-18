from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
)


class CommandPanel(QWidget):
    """MCI SoftEngine command console."""

    commandEntered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(5)

        header = QHBoxLayout()

        title = QLabel("COMMAND LINE")

        title.setStyleSheet("""
            QLabel {
                color: #8DD9FF;
                font-weight: bold;
                font-size: 10pt;
            }
        """)

        header.addWidget(title)
        header.addStretch()

        clear_button = QPushButton("Clear")
        clear_button.setFixedWidth(60)

        header.addWidget(clear_button)

        layout.addLayout(header)

        self.history = QListWidget()
        self.history.setMaximumHeight(95)

        layout.addWidget(self.history)

        input_layout = QHBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText(
            "Type a command..."
        )

        execute_button = QPushButton("Execute")
        execute_button.setFixedWidth(75)

        input_layout.addWidget(self.input)
        input_layout.addWidget(execute_button)

        layout.addLayout(input_layout)

        self.input.returnPressed.connect(
            self._emit_command
        )

        execute_button.clicked.connect(
            self._emit_command
        )

        clear_button.clicked.connect(
            self.clear_history
        )

    def _emit_command(self):

        command = self.input.text().strip()

        if not command:
            return

        self.add_history(
            f"> {command}"
        )

        self.input.clear()

        self.commandEntered.emit(
            command
        )

    def add_history(self, text):

        self.history.addItem(
            str(text)
        )

        self.history.scrollToBottom()

    def set_prompt(self, text):

        self.add_history(
            str(text)
        )

    def clear_history(self):

        self.history.clear()
