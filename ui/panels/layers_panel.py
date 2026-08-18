from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)


class LayersPanel(QWidget):
    """MCI SoftEngine layer manager panel."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QLabel("LAYERS")

        title.setStyleSheet("""
            QLabel {
                color: #8DD9FF;
                font-weight: bold;
                font-size: 11pt;
                padding: 4px;
            }
        """)

        layout.addWidget(title)

        self.table = QTableWidget(0, 5)

        self.table.setHorizontalHeaderLabels([
            "Layer",
            "Visible",
            "Lock",
            "Type",
            "Weight",
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        for column in range(1, 5):
            self.table.horizontalHeader().setSectionResizeMode(
                column,
                QHeaderView.ResizeToContents
            )

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        layout.addWidget(self.table)

        self._build_default_layers()

    def _build_default_layers(self):

        layers = [
            "STRUCTURE",
            "ARCHITECTURE",
            "WALL",
            "COLUMN",
            "BEAM",
            "SLAB",
            "FOUNDATION",
            "DIMENSION",
            "TEXT",
            "GRID",
            "AXIS",
        ]

        for name in layers:
            self.add_layer(name)

    def add_layer(
        self,
        name,
        visible=True,
        locked=False,
        line_type="Continuous",
        weight="0.30 mm",
    ):

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(
            row,
            0,
            QTableWidgetItem(str(name))
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(
                "●" if visible else "○"
            )
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(
                "■" if locked else "□"
            )
        )

        self.table.setItem(
            row,
            3,
            QTableWidgetItem(str(line_type))
        )

        self.table.setItem(
            row,
            4,
            QTableWidgetItem(str(weight))
        )
