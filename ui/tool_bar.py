from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar


class ToolBar(QToolBar):

    def __init__(self, title="Tools", parent=None):

        super().__init__(title, parent)

        self.setMovable(False)

        self.setFloatable(False)

        self.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon
        )

        self.actions = {}

    def add_tool(
        self,
        name,
        callback=None
    ):

        action = QAction(name, self)

        if callback:
            action.triggered.connect(callback)

        self.addAction(action)

        self.actions[name] = action

        return action

    def get_action(self, name):

        return self.actions.get(name)

    def clear_tools(self):

        self.clear()

        self.actions.clear()