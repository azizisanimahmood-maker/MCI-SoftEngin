from __future__ import annotations

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QTabWidget,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QToolButton,
    QLabel,
    QFrame,
    QSizePolicy,
)


class Ribbon(QTabWidget):

    commandRequested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumHeight(125)
        self.setMaximumHeight(145)
        self.setMovable(False)
        self.setDocumentMode(True)

        self._tabs = {}
        self._buttons = {}

        self.setStyleSheet("""
            QTabWidget {
                background: #0B151E;
                border: none;
            }

            QTabWidget::pane {
                border: none;
                background: #0B151E;
                border-bottom: 1px solid #263B49;
            }

            QTabBar {
                background: #101D27;
            }

            QTabBar::tab {
                background: #101D27;
                color: #AFC4D0;
                padding: 8px 20px;
                min-width: 80px;
                border: none;
            }

            QTabBar::tab:selected {
                background: #1C3B4E;
                color: #FFFFFF;
                border-bottom: 2px solid #38BDF8;
            }

            QTabBar::tab:hover {
                background: #183244;
                color: white;
            }

            QToolButton {
                background: #111F2A;
                color: #D9EAF2;
                border: 1px solid #263E4D;
                border-radius: 4px;
                padding: 4px;
                min-width: 72px;
                min-height: 68px;
            }

            QToolButton:hover {
                background: #1B3C50;
                border: 1px solid #3C7897;
            }

            QToolButton:pressed {
                background: #245777;
            }

            QToolButton:checked {
                background: #245777;
                border: 1px solid #55B9E8;
            }

            QLabel {
                color: #78909C;
            }
        """)

        self._create_tabs()

    # =====================================================
    # TABS
    # =====================================================

    def _create_tabs(self):

        tabs = [
            "HOME",
            "DRAW",
            "MODIFY",
            "ANNOTATE",
            "ARCHITECTURE",
            "STRUCTURE",
            "ANALYSIS",
            "VIEW",
        ]

        for name in tabs:
            self.add_ribbon_tab(name)

        self._build_home()
        self._build_draw()
        self._build_modify()
        self._build_annotate()
        self._build_architecture()
        self._build_structure()
        self._build_analysis()
        self._build_view()

    # =====================================================
    # TAB
    # =====================================================

    def add_ribbon_tab(self, name):

        page = QWidget()

        layout = QHBoxLayout(page)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(8)

        self.addTab(page, name)

        self._tabs[name] = layout

        return page

    # =====================================================
    # GROUP
    # =====================================================

    def add_group(self, tab_name, title):

        layout = self._tabs[tab_name]

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.NoFrame)

        group_layout = QVBoxLayout(frame)
        group_layout.setContentsMargins(4, 2, 4, 0)
        group_layout.setSpacing(2)

        content = QHBoxLayout()
        content.setSpacing(3)

        group_layout.addLayout(content)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Segoe UI", 8))

        group_layout.addWidget(label)

        layout.addWidget(frame)

        return content

    # =====================================================
    # BUTTON
    # =====================================================

    def add_button(
        self,
        layout,
        command,
        text,
        icon_text=None,
        checkable=False,
    ):

        button = QToolButton()

        button.setText(
            f"{icon_text}\n{text}"
            if icon_text
            else text
        )

        button.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextOnly
        )

        button.setCheckable(checkable)

        button.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )

        button.clicked.connect(
            lambda checked=False, cmd=command:
            self.commandRequested.emit(cmd)
        )

        layout.addWidget(button)

        self._buttons[command] = button

        return button

    # =====================================================
    # HOME
    # =====================================================

    def _build_home(self):

        draw = self.add_group("HOME", "DRAW")

        self.add_button(draw, "LINE", "Line", "╱")
        self.add_button(draw, "RECTANG", "Rectangle", "□")
        self.add_button(draw, "CIRCLE", "Circle", "○")

        modify = self.add_group("HOME", "MODIFY")

        self.add_button(modify, "MOVE", "Move", "✥")
        self.add_button(modify, "COPY", "Copy", "▣")
        self.add_button(modify, "ROTATE", "Rotate", "↻")
        self.add_button(modify, "ERASE", "Erase", "×")

        view = self.add_group("HOME", "VIEW")

        self.add_button(view, "ZOOM EXTENTS", "Extents", "⌗")
        self.add_button(view, "PAN", "Pan", "✋")

    # =====================================================
    # DRAW
    # =====================================================

    def _build_draw(self):

        geometry = self.add_group("DRAW", "GEOMETRY")

        commands = [
            ("LINE", "Line", "╱"),
            ("PLINE", "Polyline", "⌁"),
            ("RECTANG", "Rectangle", "□"),
            ("CIRCLE", "Circle", "○"),
            ("ARC", "Arc", "◔"),
            ("ELLIPSE", "Ellipse", "⬭"),
            ("POINT", "Point", "•"),
            ("POLYGON", "Polygon", "⬡"),
        ]

        for command, text, icon in commands:
            self.add_button(
                geometry,
                command,
                text,
                icon
            )

    # =====================================================
    # MODIFY
    # =====================================================

    def _build_modify(self):

        group = self.add_group("MODIFY", "MODIFY")

        commands = [
            ("MOVE", "Move", "✥"),
            ("COPY", "Copy", "▣"),
            ("ROTATE", "Rotate", "↻"),
            ("SCALE", "Scale", "⇲"),
            ("MIRROR", "Mirror", "⇄"),
            ("OFFSET", "Offset", "║"),
            ("TRIM", "Trim", "✂"),
            ("EXTEND", "Extend", "↔"),
            ("ERASE", "Erase", "×"),
        ]

        for command, text, icon in commands:
            self.add_button(
                group,
                command,
                text,
                icon
            )

    # =====================================================
    # ANNOTATE
    # =====================================================

    def _build_annotate(self):

        group = self.add_group("ANNOTATE", "ANNOTATION")

        commands = [
            ("TEXT", "Text", "T"),
            ("MTEXT", "MText", "T"),
            ("DIMLINEAR", "Linear", "↔"),
            ("DIMALIGNED", "Aligned", "∕"),
            ("DIMANGULAR", "Angular", "∠"),
            ("DIMRADIUS", "Radius", "R"),
            ("DIMDIAMETER", "Diameter", "Ø"),
        ]

        for command, text, icon in commands:
            self.add_button(
                group,
                command,
                text,
                icon
            )

    # =====================================================
    # ARCHITECTURE
    # =====================================================

    def _build_architecture(self):

        group = self.add_group(
            "ARCHITECTURE",
            "ARCHITECTURAL"
        )

        commands = [
            ("WALL", "Wall", "▤"),
            ("DOOR", "Door", "▯"),
            ("WINDOW", "Window", "▥"),
            ("ROOM", "Room", "□"),
            ("STAIR", "Stair", "▤"),
            ("ROOF", "Roof", "⌂"),
        ]

        for command, text, icon in commands:
            self.add_button(
                group,
                command,
                text,
                icon
            )

    # =====================================================
    # STRUCTURE
    # =====================================================

    def _build_structure(self):

        group = self.add_group(
            "STRUCTURE",
            "STRUCTURAL MODEL"
        )

        commands = [
            ("COLUMN", "Column", "▮"),
            ("BEAM", "Beam", "━"),
            ("BRACE", "Brace", "╲"),
            ("SHEAR WALL", "Shear Wall", "▥"),
            ("SLAB", "Slab", "▱"),
            ("FOUNDATION", "Foundation", "⌔"),
        ]

        for command, text, icon in commands:
            self.add_button(
                group,
                command,
                text,
                icon
            )

    # =====================================================
    # ANALYSIS
    # =====================================================

    def _build_analysis(self):

        group = self.add_group(
            "ANALYSIS",
            "ANALYSIS"
        )

        commands = [
            ("LOAD", "Load", "↓"),
            ("SUPPORT", "Supports", "▲"),
            ("COMBINATION", "Combinations", "≡"),
            ("MESH", "Meshing", "▦"),
            ("ANALYSIS", "Analyze", "▶"),
            ("RESULTS", "Results", "Σ"),
            ("DESIGN CHECK", "Design Check", "✓"),
        ]

        for command, text, icon in commands:
            self.add_button(
                group,
                command,
                text,
                icon
            )

    # =====================================================
    # VIEW
    # =====================================================

    def _build_view(self):

        navigation = self.add_group(
            "VIEW",
            "NAVIGATION"
        )

        commands = [
            ("ZOOM EXTENTS", "Extents", "⌗"),
            ("ZOOM 1.2", "Zoom In", "+"),
            ("ZOOM 0.833333", "Zoom Out", "−"),
            ("PAN", "Pan", "✋"),
            ("REDRAW", "Redraw", "↻"),
            ("REGEN", "Regen", "⟳"),
        ]

        for command, text, icon in commands:
            self.add_button(
                navigation,
                command,
                text,
                icon
            )

        display = self.add_group(
            "VIEW",
            "DISPLAY"
        )

        self.add_button(
            display,
            "GRID",
            "Grid",
            "#",
            True
        )

        self.add_button(
            display,
            "SNAP",
            "Snap",
            "⌖",
            True
        )

    # =====================================================
    # ACCESS
    # =====================================================

    def tab_layout(self, name):
        return self._tabs.get(name)

    def get_button(self, command):
        return self._buttons.get(command)