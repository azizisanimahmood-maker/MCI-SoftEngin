from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit
)


class PropertyPanel(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMinimumWidth(260)

        self.form = QFormLayout()

        self.type_edit = QLineEdit()
        self.layer_edit = QLineEdit()
        self.color_edit = QLineEdit()
        self.lineweight_edit = QLineEdit()

        self.form.addRow("Type", self.type_edit)
        self.form.addRow("Layer", self.layer_edit)
        self.form.addRow("Color", self.color_edit)
        self.form.addRow("LineWeight", self.lineweight_edit)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Properties"))

        layout.addLayout(self.form)

        layout.addStretch()

        self.setLayout(layout)

    def set_entity(self, entity):

        if entity is None:

            self.clear()

            return

        self.type_edit.setText(type(entity).__name__)

        self.layer_edit.setText(str(entity.layer))

        self.color_edit.setText(str(entity.color))

        self.lineweight_edit.setText(str(entity.lineweight))

    def clear(self):

        self.type_edit.clear()

        self.layer_edit.clear()

        self.color_edit.clear()

        self.lineweight_edit.clear()