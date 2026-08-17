import sys
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QAction, QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QTabWidget, QDockWidget, QTreeWidget, QTreeWidgetItem,
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QFrame,
    QPushButton, QSplitter, QSizePolicy
)


class DrawingCanvas(QWidget):
    """Simple CAD-style preview canvas. This is UI only; no CAD engine is changed."""

    def __init__(self):
        super().__init__()
        self.setMinimumSize(500, 400)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#07111B"))

        # Grid
        grid_pen = QPen(QColor("#142938"))
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)

        step = 25
        for x in range(0, self.width(), step):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), step):
            painter.drawLine(0, y, self.width(), y)

        # Major grid
        major_pen = QPen(QColor("#203D4D"))
        major_pen.setWidth(1)
        painter.setPen(major_pen)
        for x in range(0, self.width(), step * 5):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), step * 5):
            painter.drawLine(0, y, self.width(), y)

        # Axes
        painter.setPen(QPen(QColor("#2CC7FF"), 2))
        painter.drawLine(40, self.height() - 45, 180, self.height() - 45)
        painter.drawLine(40, self.height() - 45, 40, self.height() - 180)

        painter.setPen(QPen(QColor("#FF5252"), 2))
        painter.drawLine(40, self.height() - 45, 150, self.height() - 45)

        painter.setPen(QPen(QColor("#55E889"), 2))
        painter.drawLine(40, self.height() - 45, 40, self.height() - 155)

        # Sample structural plan
        pen = QPen(QColor("#8DD9FF"), 2)
        painter.setPen(pen)

        left, top = 170, 100
        width, height = min(650, self.width() - 330), min(430, self.height() - 190)

        # Outer frame
        painter.drawRect(left, top, width, height)

        # Structural grid / beams
        xs = [left, left + width // 4, left + width // 2,
              left + 3 * width // 4, left + width]
        ys = [top, top + height // 3, top + 2 * height // 3, top + height]

        beam_pen = QPen(QColor("#6EE7A8"), 3)
        painter.setPen(beam_pen)

        for x in xs:
            painter.drawLine(x, top, x, top + height)
        for y in ys:
            painter.drawLine(left, y, left + width, y)

        # Columns
        painter.setPen(QPen(QColor("#FFD84D"), 2))
        painter.setBrush(QColor("#FFD84D"))
        for x in xs:
            for y in ys:
                painter.drawRect(x - 5, y - 5, 10, 10)

        painter.setBrush(Qt.NoBrush)

        # Labels
        painter.setPen(QColor("#D9F2FF"))
        painter.setFont(QFont("Segoe UI", 9))

        for i, x in enumerate(xs):
            painter.drawText(x - 5, top - 12, chr(65 + i))

        for i, y in enumerate(ys):
            painter.drawText(left - 25, y + 4, str(i + 1))

        painter.setPen(QColor("#8AA6B7"))
        painter.drawText(20, 25, "MCI SoftEngine  •  Drawing Canvas")
        painter.drawText(self.width() - 150, self.height() - 20, "TOP VIEW")

    def mouseMoveEvent(self, event):
        self.parentWidget().window().status_coordinates.setText(
            f"X: {event.position().x():7.2f}    Y: {event.position().y():7.2f}    Z: 0.00"
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MCI SoftEngine | Structural CAD")
        self.resize(1500, 900)
        self.setMinimumSize(1200, 750)

        self.build_menu()
        self.build_ribbon()
        self.build_main_area()
        self.build_command_line()
        self.build_status_bar()

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background: #0A141E;
                color: #DCEAF2;
                font-family: "Segoe UI";
                font-size: 10pt;
            }

            QMenuBar {
                background: #111E29;
                border-bottom: 1px solid #263A49;
                padding: 3px;
            }

            QMenuBar::item {
                padding: 7px 12px;
                background: transparent;
            }

            QMenuBar::item:selected {
                background: #20384A;
            }

            QMenu {
                background: #14222E;
                border: 1px solid #314958;
            }

            QMenu::item {
                padding: 7px 28px;
            }

            QMenu::item:selected {
                background: #24516A;
            }

            QToolBar {
                background: #111E29;
                border: none;
                border-bottom: 1px solid #293D4B;
                spacing: 3px;
                padding: 4px;
            }

            QToolButton {
                color: #DCEAF2;
                background: transparent;
                border: 1px solid transparent;
                padding: 7px 10px;
            }

            QToolButton:hover {
                background: #1E3A4D;
                border: 1px solid #315E78;
            }

            QToolButton:checked {
                background: #245777;
                border: 1px solid #4A9AC2;
            }

            QTabWidget::pane {
                border: 1px solid #263A49;
                background: #0D1822;
            }

            QTabBar::tab {
                background: #111E29;
                padding: 8px 18px;
                border-right: 1px solid #263A49;
            }

            QTabBar::tab:selected {
                background: #1B3446;
                color: #FFFFFF;
            }

            QDockWidget {
                titlebar-close-icon: none;
                titlebar-normal-icon: none;
            }

            QDockWidget::title {
                background: #111E29;
                color: #EAF7FF;
                padding: 8px;
                border: 1px solid #293D4B;
                font-weight: bold;
            }

            QTreeWidget, QTableWidget, QLineEdit {
                background: #0D1822;
                border: 1px solid #263A49;
                color: #DCEAF2;
            }

            QTreeWidget::item {
                padding: 5px;
            }

            QTreeWidget::item:selected {
                background: #21465C;
            }

            QTableWidget {
                gridline-color: #263A49;
            }

            QHeaderView::section {
                background: #162733;
                color: #BFD4DF;
                border: 1px solid #263A49;
                padding: 5px;
            }

            QPushButton {
                background: #183244;
                border: 1px solid #31566B;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background: #24516A;
            }
        """)

    def build_menu(self):
        menu = self.menuBar()

        menus = {
            "File": ["New Project", "Open", "Save", "Export", "Exit"],
            "Edit": ["Undo", "Redo", "Cut", "Copy", "Paste"],
            "View": ["Top", "Front", "3D", "Zoom", "Pan", "Fit"],
            "Draw": ["Line", "Polyline", "Rectangle", "Circle", "Arc"],
            "Modify": ["Move", "Copy", "Rotate", "Mirror", "Trim", "Offset"],
            "Annotate": ["Text", "Dimension", "Leader", "Table"],
            "Architecture": ["Wall", "Door", "Window", "Room", "Stair"],
            "Structure": ["Column", "Beam", "Brace", "Shear Wall", "Slab", "Foundation"],
            "Analysis": ["Loads", "Supports", "Combinations", "Analysis", "Results"],
            "Modeling": ["Levels", "Grids", "Objects"],
            "Layers": ["Layer Manager", "Layer Properties"],
            "Tools": ["Options", "Units", "Customize"],
            "Settings": ["Appearance", "Workspace"],
            "Window": ["Project", "Properties", "Layers", "Command Line"],
            "Help": ["Documentation", "About MCI SoftEngine"],
        }

        for name, actions in menus.items():
            m = menu.addMenu(name)
            for text in actions:
                a = QAction(text, self)
                m.addAction(a)

    def build_ribbon(self):
        self.ribbon_tabs = QTabWidget()
        self.ribbon_tabs.setFixedHeight(118)

        tabs = {
            "HOME": ["Select", "Line", "Polyline", "Rectangle", "Circle",
                     "Move", "Copy", "Rotate", "Mirror", "Trim", "Extend",
                     "Offset", "Erase"],
            "DRAW": ["Line", "Polyline", "Circle", "Arc", "Rectangle",
                     "Polygon", "Spline", "Hatch", "Point"],
            "MODIFY": ["Move", "Copy", "Rotate", "Mirror", "Scale",
                       "Stretch", "Trim", "Extend", "Fillet", "Chamfer",
                       "Offset", "Array"],
            "ANNOTATE": ["Text", "MText", "Dimension", "Leader",
                         "Multileader", "Table", "Mark", "Grid"],
            "ARCHITECTURE": ["Wall", "Door", "Window", "Room", "Stair",
                             "Column", "Slab", "Roof"],
            "STRUCTURE": ["Column", "Beam", "Brace", "Shear Wall",
                          "Slab", "Foundation", "Footing", "Grid", "Axis"],
            "ANALYSIS": ["Load", "Combination", "Supports", "Meshing",
                         "Analysis", "Results", "Diagrams", "Design Check"],
            "VIEW": ["Top", "Bottom", "Front", "Back", "Left", "Right",
                     "3D", "Isometric", "Zoom", "Pan", "Fit", "Grid", "Snap"]
        }

        for tab_name, tools in tabs.items():
            bar = QToolBar()
            bar.setMovable(False)
            bar.setIconSize(bar.iconSize())

            for tool in tools:
                action = QAction(tool, self)
                action.setCheckable(tool in ("Select", "Grid", "Snap"))
                bar.addAction(action)

            self.ribbon_tabs.addTab(bar, tab_name)

        self.addToolBar(Qt.TopToolBarArea, self.ribbon_tabs.findChildren(QToolBar)[0])
        # Remove the automatically added first toolbar; ribbon tabs remain as a central widget.
        self.removeToolBar(self.ribbon_tabs.findChildren(QToolBar)[0])
        self.setMenuWidget(self.ribbon_tabs)

    def build_main_area(self):
        self.canvas = DrawingCanvas()

        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabel("PROJECT BROWSER")
        self.populate_project_tree()

        project_dock = QDockWidget("PROJECT", self)
        project_dock.setWidget(self.project_tree)
        project_dock.setMinimumWidth(245)
        project_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, project_dock)

        self.properties = QTableWidget(8, 2)
        self.properties.setHorizontalHeaderLabels(["Property", "Value"])
        self.properties.horizontalHeader().setStretchLastSection(True)

        rows = [
            ("Name", "B-101"),
            ("Section", "40 × 60 cm"),
            ("Material", "Concrete"),
            ("Level", "Level 01"),
            ("Length", "6.50 m"),
            ("Rotation", "0°"),
            ("Layer", "STRUCTURE"),
            ("Status", "Defined"),
        ]

        for r, (a, b) in enumerate(rows):
            self.properties.setItem(r, 0, QTableWidgetItem(a))
            self.properties.setItem(r, 1, QTableWidgetItem(b))

        layers = QTableWidget(11, 5)
        layers.setHorizontalHeaderLabels(
            ["Layer", "Visible", "Lock", "Type", "Weight"]
        )
        layer_names = [
            "STRUCTURE", "ARCHITECTURE", "WALL", "COLUMN", "BEAM",
            "SLAB", "FOUNDATION", "DIMENSION", "TEXT", "GRID", "AXIS"
        ]

        for r, name in enumerate(layer_names):
            layers.setItem(r, 0, QTableWidgetItem(name))
            layers.setItem(r, 1, QTableWidgetItem("●"))
            layers.setItem(r, 2, QTableWidgetItem("□"))
            layers.setItem(r, 3, QTableWidgetItem("Continuous"))
            layers.setItem(r, 4, QTableWidgetItem("0.30 mm"))

        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(5, 5, 5, 5)
        right_layout.addWidget(QLabel("PROPERTIES"))
        right_layout.addWidget(self.properties)
        right_layout.addWidget(QLabel("LAYERS"))
        right_layout.addWidget(layers)

        right_dock = QDockWidget("PROPERTIES / LAYERS", self)
        right_dock.setWidget(right_container)
        right_dock.setMinimumWidth(310)
        right_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, right_dock)

        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(3, 3, 3, 3)
        central_layout.setSpacing(3)

        tabs = QTabWidget()
        tabs.addTab(self.canvas, "Floor Plan 01")
        tabs.addTab(QWidget(), "3D View")
        tabs.addTab(QWidget(), "Analysis")
        central_layout.addWidget(tabs)

        self.setCentralWidget(central)

    def populate_project_tree(self):
        root = QTreeWidgetItem(["Project"])
        self.project_tree.addTopLevelItem(root)

        levels = QTreeWidgetItem(["Levels"])
        root.addChild(levels)
        for level in ["Level 03", "Level 02", "Level 01", "Ground", "Base"]:
            levels.addChild(QTreeWidgetItem([level]))

        grids = QTreeWidgetItem(["Structural Grids"])
        root.addChild(grids)

        views = QTreeWidgetItem(["Views"])
        root.addChild(views)
        for view in ["Floor Plans", "3D Views", "Elevations", "Sections"]:
            views.addChild(QTreeWidgetItem([view]))

        objects = QTreeWidgetItem(["Objects"])
        root.addChild(objects)
        for obj in ["Architecture", "Structure", "Columns", "Beams",
                    "Slabs", "Foundations", "Walls", "Braces"]:
            objects.addChild(QTreeWidgetItem([obj]))

        root.setExpanded(True)
        levels.setExpanded(True)
        views.setExpanded(True)
        objects.setExpanded(True)

    def build_command_line(self):
        command_frame = QFrame()
        command_frame.setFixedHeight(115)
        command_layout = QVBoxLayout(command_frame)
        command_layout.setContentsMargins(8, 5, 8, 5)

        header = QHBoxLayout()
        title = QLabel("COMMAND LINE")
        title.setStyleSheet("font-weight: bold; color: #8DD9FF;")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(QLabel("History"))
        header.addWidget(QLabel("Suggestions"))
        command_layout.addLayout(header)

        history = QLabel(
            "Command: LINE\n"
            "Specify first point:\n"
            "Specify next point:\n"
            "Specify next point or [Undo]:"
        )
        history.setStyleSheet("color: #B7CBD6;")
        command_layout.addWidget(history)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Type a command...")
        command_layout.addWidget(self.command_input)

        self.status_command = command_frame
        self.status_command.setParent(self.centralWidget())
        self.centralWidget().layout().addWidget(command_frame)

        self.command_input.returnPressed.connect(self.execute_command)

    def execute_command(self):
        text = self.command_input.text().strip()
        if text:
            self.status_command.findChildren(QLabel)[1].setText(
                f"Command: {text.upper()}"
            )
        self.command_input.clear()

    def build_status_bar(self):
        self.status_coordinates = QLabel("X: 0.00    Y: 0.00    Z: 0.00")
        self.status_coordinates.setMinimumWidth(220)

        self.statusBar().addWidget(self.status_coordinates)
        for text in [
            "GRID  ON", "SNAP  ON", "ORTHO  OFF",
            "POLAR  OFF", "OSNAP  ON"
        ]:
            label = QLabel(text)
            label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            label.setStyleSheet("padding: 3px 10px;")
            self.statusBar().addWidget(label)

        self.statusBar().addPermanentWidget(QLabel("Layer: STRUCTURE"))
        self.statusBar().addPermanentWidget(QLabel("Scale: 1:100"))
        self.statusBar().addPermanentWidget(QLabel("Units: mm"))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MCI SoftEngine")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
# --- MCI integration methods ---
def _mci_set_renderer(self, renderer):
    self.renderer = renderer

def _mci_set_entities(self, entities):
    self.entities = entities
    if hasattr(self, "canvas"):
        self.canvas.entities = entities

MainWindow.set_renderer = _mci_set_renderer
MainWindow.set_entities = _mci_set_entities
