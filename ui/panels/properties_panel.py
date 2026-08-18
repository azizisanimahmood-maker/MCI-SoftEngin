from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)


class PropertiesPanel(QWidget):
    """MCI SoftEngine object properties panel."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QLabel("PROPERTIES")

        title.setStyleSheet("""
            QLabel {
                color: #8DD9FF;
                font-weight: bold;
                font-size: 11pt;
                padding: 4px;
            }
        """)

        layout.addWidget(title)

        self.table = QTableWidget(0, 2)

        self.table.setHorizontalHeaderLabels([
            "Property",
            "Value",
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        self.table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

        self.set_default_properties()

    def set_default_properties(self):

        properties = [
            ("Name", "MCI Object"),
            ("Section", "-"),
            ("Material", "-"),
            ("Level", "Level 01"),
            ("Length", "-"),
            ("Rotation", "0°"),
            ("Layer", "STRUCTURE"),
            ("Status", "Ready"),
        ]

        self.set_properties(properties)

    def set_properties(self, properties):

        self.table.setRowCount(0)

        for row, (name, value) in enumerate(properties):

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(str(name))
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(str(value))
            )
