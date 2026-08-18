from ui.panels.project_panel import ProjectPanel
from ui.panels.properties_panel import PropertiesPanel
from ui.panels.layers_panel import LayersPanel
from ui.panels.command_panel import CommandPanel
from ui.panels.view_panel import ViewPanel
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QDockWidget,
    QLineEdit,
    QLabel,
    QFrame,
)

from ui.canvas import Canvas
from ui.ribbon import Ribbon
from renderer.renderer import Renderer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "MCI SoftEngine | Structural CAD"
        )

        self.resize(1500, 900)
        self.setMinimumSize(1200, 750)

        self.entities = []

        self._build_style()
        self.build_menu()
        self.build_ribbon()
        self.build_main_area()
        self.build_command_line()
        self.build_status_bar()

        # =================================================
        # CONNECT CANVAS
        # =================================================

        self.canvas.set_renderer(
            Renderer()
        )

        self.canvas.set_entities(
            self.entities
        )

        self.canvas.mouse_world_position.connect(
            self.update_coordinates
        )

        self.canvas.commandFinished.connect(
            self.command_finished
        )

        # =================================================
        # CONNECT RIBBON
        # =================================================

        self.ribbon.commandRequested.connect(
            self.execute_ribbon_command
        )

    # =====================================================
    # STYLE
    # =====================================================

    def _build_style(self):

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

            QDockWidget::title {
                background: #111E29;
                color: #EAF7FF;
                padding: 8px;
                border: 1px solid #293D4B;
                font-weight: bold;
            }

            QLineEdit {
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

            QLabel {
                color: #BFD4DF;
            }

            QLineEdit {
                padding: 6px;
            }
        """)

    # =====================================================
    # MENU
    # =====================================================

    def build_menu(self):

        menu = self.menuBar()

        menus = {
            "File": [
                "New Project",
                "Open",
                "Save",
                "Export",
                "Exit",
            ],

            "Edit": [
                "Undo",
                "Redo",
                "Cut",
                "Copy",
                "Paste",
            ],

            "View": [
                "Top",
                "Front",
                "3D",
                "Zoom",
                "Pan",
                "Fit",
            ],

            "Draw": [
                "Line",
                "Polyline",
                "Rectangle",
                "Circle",
                "Arc",
                "Ellipse",
                "Polygon",
                "Point",
            ],

            "Modify": [
                "Move",
                "Copy",
                "Rotate",
                "Mirror",
                "Trim",
                "Extend",
                "Offset",
                "Erase",
            ],

            "Annotate": [
                "Text",
                "Dimension",
                "Leader",
                "Table",
            ],

            "Architecture": [
                "Wall",
                "Door",
                "Window",
                "Room",
                "Stair",
            ],

            "Structure": [
                "Column",
                "Beam",
                "Brace",
                "Shear Wall",
                "Slab",
                "Foundation",
            ],

            "Analysis": [
                "Loads",
                "Supports",
                "Combinations",
                "Analysis",
                "Results",
            ],

            "Tools": [
                "Options",
                "Units",
                "Customize",
            ],

            "Help": [
                "Documentation",
                "About MCI SoftEngine",
            ],
        }

        for name, actions in menus.items():

            menu_item = menu.addMenu(name)

            for text in actions:

                action = QAction(
                    text,
                    self
                )

                menu_item.addAction(
                    action
                )

    # =====================================================
    # RIBBON
    # =====================================================

    def build_ribbon(self):

        self.ribbon = Ribbon(self)

        self.setMenuWidget(
            self.ribbon
        )

    # =====================================================
    # MAIN AREA
    # =====================================================

    def build_main_area(self):

        # =================================================
        # REAL CAD CANVAS
        # =================================================

        self.canvas = Canvas()

        self.canvas.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        # =================================================
        # MODULAR UI PANELS
        # =================================================

        self.project_panel = ProjectPanel()

        self.properties_panel = PropertiesPanel()

        self.layers_panel = LayersPanel()

        self.view_panel = ViewPanel()

        # =================================================
        # LEFT PROJECT PANEL
        # =================================================

        project_dock = QDockWidget(
            "PROJECT",
            self
        )

        project_dock.setObjectName(
            "ProjectPanelDock"
        )

        project_dock.setWidget(
            self.project_panel
        )

        project_dock.setMinimumWidth(
            245
        )

        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            project_dock
        )

        self.project_dock = project_dock

        # =================================================
        # RIGHT PROPERTIES PANEL
        # =================================================

        properties_dock = QDockWidget(
            "PROPERTIES",
            self
        )

        properties_dock.setObjectName(
            "PropertiesPanelDock"
        )

        properties_dock.setWidget(
            self.properties_panel
        )

        properties_dock.setMinimumWidth(
            300
        )

        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            properties_dock
        )

        self.properties_dock = properties_dock

        # =================================================
        # RIGHT LAYERS PANEL
        # =================================================

        layers_dock = QDockWidget(
            "LAYERS",
            self
        )

        layers_dock.setObjectName(
            "LayersPanelDock"
        )

        layers_dock.setWidget(
            self.layers_panel
        )

        layers_dock.setMinimumWidth(
            300
        )

        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            layers_dock
        )

        self.layers_dock = layers_dock

        # =================================================
        # RIGHT VIEW PANEL
        # =================================================

        view_dock = QDockWidget(
            "VIEW",
            self
        )

        view_dock.setObjectName(
            "ViewPanelDock"
        )

        view_dock.setWidget(
            self.view_panel
        )

        view_dock.setMinimumWidth(
            300
        )

        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            view_dock
        )

        self.view_dock = view_dock

        # =================================================
        # CENTRAL CAD AREA
        # =================================================

        central = QWidget()

        central_layout = QVBoxLayout(
            central
        )

        central_layout.setContentsMargins(
            3,
            3,
            3,
            3
        )

        central_layout.setSpacing(
            3
        )

        central_layout.addWidget(
            self.canvas
        )

        self.setCentralWidget(
            central
        )

        # =================================================
        # DOCK ARRANGEMENT
        # =================================================

        self.tabifyDockWidget(
            properties_dock,
            layers_dock
        )

        self.tabifyDockWidget(
            layers_dock,
            view_dock
        )

        properties_dock.raise_()
    # =====================================================
    # PROJECT TREE
    # =====================================================

    def populate_project_tree(self):

        root = QTreeWidgetItem(
            ["Project"]
        )

        self.project_tree.addTopLevelItem(
            root
        )

        levels = QTreeWidgetItem(
            ["Levels"]
        )

        root.addChild(
            levels
        )

        for level in [
            "Level 03",
            "Level 02",
            "Level 01",
            "Ground",
            "Base",
        ]:

            levels.addChild(
                QTreeWidgetItem(
                    [level]
                )
            )

        grids = QTreeWidgetItem(
            ["Structural Grids"]
        )

        root.addChild(
            grids
        )

        views = QTreeWidgetItem(
            ["Views"]
        )

        root.addChild(
            views
        )

        for view in [
            "Floor Plans",
            "3D Views",
            "Elevations",
            "Sections",
        ]:

            views.addChild(
                QTreeWidgetItem(
                    [view]
                )
            )

        objects = QTreeWidgetItem(
            ["Objects"]
        )

        root.addChild(
            objects
        )

        for obj in [
            "Architecture",
            "Structure",
            "Columns",
            "Beams",
            "Slabs",
            "Foundations",
            "Walls",
            "Braces",
        ]:

            objects.addChild(
                QTreeWidgetItem(
                    [obj]
                )
            )

        root.setExpanded(True)
        levels.setExpanded(True)
        views.setExpanded(True)
        objects.setExpanded(True)

    # =====================================================
    # COMMAND LINE
    # =====================================================

    def build_command_line(self):

        frame = QFrame()

        frame.setFixedHeight(
            105
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            8,
            5,
            8,
            5
        )

        self.command_history = QLabel(
            "Command: Ready"
        )

        self.command_history.setStyleSheet(
            "color: #8DD9FF;"
        )

        layout.addWidget(
            self.command_history
        )

        self.command_input = QLineEdit()

        self.command_input.setPlaceholderText(
            "Type a command..."
        )

        layout.addWidget(
            self.command_input
        )

        self.centralWidget().layout().addWidget(
            frame
        )

        self.command_input.returnPressed.connect(
            self.execute_command
        )

    # =====================================================
    # COMMAND EXECUTION
    # =====================================================

    def execute_command(self):

        text = (
            self.command_input
            .text()
            .strip()
        )

        if not text:
            return

        command = text.upper()

        self.command_history.setText(
            f"Command: {command}"
        )

        self.command_input.clear()

        self.execute_ribbon_command(
            command
        )

    def execute_ribbon_command(
        self,
        command
    ):

        command = str(
            command
        ).strip().upper()

        # Commands that Canvas currently supports
        canvas_commands = {
            "LINE",
            "PLINE",
            "POLYLINE",
            "RECTANG",
            "RECTANGLE",
            "CIRCLE",
            "ARC",
            "POINT",
            "POLYGON",
            "ELLIPSE",
            "MOVE",
        }

        if command in canvas_commands:

            self.canvas.start_command(
                command
            )

            self.command_history.setText(
                f"Command: {command}  |  "
                f"Specify first point:"
            )

            self.canvas.setFocus()

            return

        # -------------------------------------------------
        # VIEW
        # -------------------------------------------------

        if command == "ZOOM EXTENTS":

            self.canvas.zoom = 1.0
            self.canvas.pan_x = 0.0
            self.canvas.pan_y = 0.0
            self.canvas.update()

            return

        if command == "ZOOM 1.2":

            self.canvas.zoom = min(
                self.canvas.zoom * 1.2,
                100.0
            )

            self.canvas.update()

            return

        if command == "ZOOM 0.833333":

            self.canvas.zoom = max(
                self.canvas.zoom / 1.2,
                0.05
            )

            self.canvas.update()

            return

        if command == "PAN":

            self.command_history.setText(
                "Command: PAN | "
                "Use middle mouse button"
            )

            return

        self.command_history.setText(
            f"Command: {command} | "
            "Not implemented yet"
        )

    # =====================================================
    # COORDINATES
    # =====================================================

    def update_coordinates(
        self,
        x,
        y
    ):

        self.status_coordinates.setText(
            f"X: {x:8.2f}    "
            f"Y: {y:8.2f}    "
            f"Z: 0.00"
        )

    # =====================================================
    # COMMAND FINISHED
    # =====================================================

    def command_finished(
        self,
        command
    ):

        self.command_history.setText(
            f"Command: {command}"
        )

    # =====================================================
    # STATUS BAR
    # =====================================================

    def build_status_bar(self):

        self.status_coordinates = QLabel(
            "X: 0.00    Y: 0.00    Z: 0.00"
        )

        self.status_coordinates.setMinimumWidth(
            250
        )

        self.statusBar().addWidget(
            self.status_coordinates
        )

        for text in [
            "GRID ON",
            "SNAP ON",
            "ORTHO OFF",
            "POLAR OFF",
            "OSNAP ON",
        ]:

            label = QLabel(text)

            label.setFrameStyle(
                QFrame.Shape.Panel |
                QFrame.Shadow.Sunken
            )

            label.setStyleSheet(
                "padding: 3px 10px;"
            )

            self.statusBar().addWidget(
                label
            )

        self.statusBar().addPermanentWidget(
            QLabel("Layer: STRUCTURE")
        )

        self.statusBar().addPermanentWidget(
            QLabel("Scale: 1:100")
        )

        self.statusBar().addPermanentWidget(
            QLabel("Units: mm")
        )


def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "MCI SoftEngine"
    )

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()


