from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.menus = {}

        self.actions = {}

        self._create_default()

    def _create_default(self):

        for name in (
            "File",
            "Edit",
            "View",
            "Insert",
            "Tools",
            "Help"
        ):

            self.add_menu(name)

    def add_menu(self, name):

        menu = self.addMenu(name)

        self.menus[name] = menu

        return menu

    def add_action(
        self,
        menu_name,
        action_name,
        callback=None
    ):

        if menu_name not in self.menus:
            return

        action = QAction(action_name, self)

        if callback:
            action.triggered.connect(callback)

        self.menus[menu_name].addAction(action)

        self.actions[action_name] = action

        return action

    def get_action(self, name):

        return self.actions.get(name)