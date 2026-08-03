from __future__ import annotations

from PySide6.QtWidgets import (
    QTabWidget,
    QWidget,
    QHBoxLayout,
)


class Ribbon(QTabWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMinimumHeight(120)

        self.setMovable(False)

        self._tabs = {}

        self._create_default_tabs()

    def _create_default_tabs(self):

        for name in (
            "Draw",
            "Modify",
            "Dimension",
            "View",
        ):

            self.add_ribbon_tab(name)

    def add_ribbon_tab(self, name):

        page = QWidget()

        layout = QHBoxLayout()

        layout.setContentsMargins(6, 6, 6, 6)

        layout.setSpacing(6)

        page.setLayout(layout)

        self.addTab(page, name)

        self._tabs[name] = layout

    def tab_layout(self, name):

        return self._tabs.get(name)