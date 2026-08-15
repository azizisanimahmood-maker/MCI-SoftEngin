from __future__ import annotations

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QTabWidget,
    QWidget,
    QHBoxLayout,
    QToolButton,
)


class Ribbon(QTabWidget):

    commandRequested = Signal(str)

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMinimumHeight(120)
        self.setMovable(False)

        self._tabs = {}
        self._buttons = {}

        self._create_default_tabs()

    # =====================================================
    # CREATE DEFAULT TABS
    # =====================================================

    def _create_default_tabs(self):

        self.add_ribbon_tab("Draw")
        self.add_ribbon_tab("Modify")
        self.add_ribbon_tab("Dimension")
        self.add_ribbon_tab("View")

        self._build_draw()
        self._build_modify()
        self._build_dimension()
        self._build_view()

    # =====================================================
    # CREATE TAB
    # =====================================================

    def add_ribbon_tab(self, name):

        page = QWidget()

        layout = QHBoxLayout()

        layout.setContentsMargins(
            6,
            6,
            6,
            6
        )

        layout.setSpacing(6)

        page.setLayout(layout)

        self.addTab(
            page,
            name
        )

        self._tabs[name] = layout

        return page

    # =====================================================
    # ADD BUTTON
    # =====================================================

    def add_button(
        self,
        tab_name,
        command,
        text=None
    ):

        layout = self._tabs.get(
            tab_name
        )

        if layout is None:
            return None

        button = QToolButton()

        button.setText(
            text or command
        )

        # =================================================
        # اصلاح شده برای PySide6
        # =================================================

        button.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )

        button.setMinimumSize(
            75,
            70
        )

        button.setAutoRaise(False)

        button.clicked.connect(
            lambda checked=False,
            cmd=command:
            self.commandRequested.emit(cmd)
        )

        layout.addWidget(
            button
        )

        self._buttons[command] = button

        return button

    # =====================================================
    # DRAW
    # =====================================================

    def _build_draw(self):

        commands = [
            ("LINE", "LINE"),
            ("PLINE", "PLINE"),
            ("RECTANG", "RECTANG"),
            ("CIRCLE", "CIRCLE"),
            ("ARC", "ARC"),
            ("POINT", "POINT"),
            ("POLYGON", "POLYGON"),
            ("ELLIPSE", "ELLIPSE"),
        ]

        for command, text in commands:

            self.add_button(
                "Draw",
                command,
                text
            )

    # =====================================================
    # MODIFY
    # =====================================================

    def _build_modify(self):

        commands = [
            ("MOVE", "MOVE"),
            ("COPY", "COPY"),
            ("ROTATE", "ROTATE"),
            ("SCALE", "SCALE"),
            ("MIRROR", "MIRROR"),
            ("OFFSET", "OFFSET"),
            ("TRIM", "TRIM"),
            ("EXTEND", "EXTEND"),
            ("ERASE", "ERASE"),
        ]

        for command, text in commands:

            self.add_button(
                "Modify",
                command,
                text
            )

    # =====================================================
    # DIMENSION
    # =====================================================

    def _build_dimension(self):

        commands = [
            ("DIMLINEAR", "Linear"),
            ("DIMALIGNED", "Aligned"),
            ("DIMANGULAR", "Angular"),
            ("DIMRADIUS", "Radius"),
            ("DIMDIAMETER", "Diameter"),
        ]

        for command, text in commands:

            self.add_button(
                "Dimension",
                command,
                text
            )

    # =====================================================
    # VIEW
    # =====================================================

    def _build_view(self):

        commands = [
            ("ZOOM ALL", "Zoom All"),
            ("ZOOM EXTENTS", "Extents"),
            ("ZOOM 1.2", "Zoom In"),
            ("ZOOM 0.833333", "Zoom Out"),
            ("PAN 100 0", "Pan Right"),
            ("PAN -100 0", "Pan Left"),
            ("REDRAW", "Redraw"),
            ("REGEN", "Regen"),
        ]

        for command, text in commands:

            self.add_button(
                "View",
                command,
                text
            )

    # =====================================================
    # ACCESS
    # =====================================================

    def tab_layout(self, name):

        return self._tabs.get(
            name
        )

    def get_button(self, command):

        return self._buttons.get(
            command
        )