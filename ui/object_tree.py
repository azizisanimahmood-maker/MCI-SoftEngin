from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem
)


class ObjectTree(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMinimumWidth(240)

        self.tree = QTreeWidget()

        self.tree.setHeaderLabels([
            "Objects"
        ])

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Object Tree")
        )

        layout.addWidget(
            self.tree
        )

        self.setLayout(layout)

    def populate(self, entities):

        self.tree.clear()

        for entity in entities:

            item = QTreeWidgetItem()

            item.setText(
                0,
                f"{type(entity).__name__} ({entity.id[:8]})"
            )

            self.tree.addTopLevelItem(item)

    def clear(self):

        self.tree.clear()

    def selected_item(self):

        return self.tree.currentItem()
