from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
)


class ProjectPanel(QWidget):
    """MCI SoftEngine project browser panel."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QLabel("PROJECT BROWSER")
        title.setStyleSheet("""
            QLabel {
                color: #8DD9FF;
                font-weight: bold;
                font-size: 11pt;
                padding: 4px;
            }
        """)

        layout.addWidget(title)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)

        layout.addWidget(self.tree)

        self._build_tree()

    def _build_tree(self):

        project = QTreeWidgetItem(["MCI SoftEngine"])

        levels = QTreeWidgetItem(["Levels"])
        for name in [
            "Level 03",
            "Level 02",
            "Level 01",
            "Ground",
            "Base",
        ]:
            levels.addChild(QTreeWidgetItem([name]))

        grids = QTreeWidgetItem(["Structural Grids"])

        views = QTreeWidgetItem(["Views"])
        for name in [
            "Floor Plans",
            "3D Views",
            "Elevations",
            "Sections",
        ]:
            views.addChild(QTreeWidgetItem([name]))

        objects = QTreeWidgetItem(["Objects"])
        for name in [
            "Architecture",
            "Structure",
            "Columns",
            "Beams",
            "Slabs",
            "Foundations",
            "Walls",
            "Braces",
        ]:
            objects.addChild(QTreeWidgetItem([name]))

        project.addChild(levels)
        project.addChild(grids)
        project.addChild(views)
        project.addChild(objects)

        self.tree.addTopLevelItem(project)

        project.setExpanded(True)
        levels.setExpanded(True)
        views.setExpanded(True)
        objects.setExpanded(True)
