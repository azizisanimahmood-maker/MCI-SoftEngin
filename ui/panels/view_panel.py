from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QGroupBox,
)


class ViewPanel(QWidget):
    """MCI SoftEngine view and navigation controls."""

    viewRequested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        title = QLabel("VIEW / NAVIGATION")

        title.setStyleSheet("""
            QLabel {
                color: #8DD9FF;
                font-weight: bold;
                font-size: 11pt;
                padding: 4px;
            }
        """)

        layout.addWidget(title)

        views_group = QGroupBox("STANDARD VIEWS")

        views_layout = QGridLayout(views_group)

        views = [
            ("Top", "TOP"),
            ("Front", "FRONT"),
            ("Back", "BACK"),
            ("Left", "LEFT"),
            ("Right", "RIGHT"),
            ("3D", "3D"),
        ]

        for index, (text, command) in enumerate(views):

            button = QPushButton(text)

            button.clicked.connect(
                lambda checked=False, cmd=command:
                self.viewRequested.emit(cmd)
            )

            row = index // 2
            column = index % 2

            views_layout.addWidget(
                button,
                row,
                column
            )

        layout.addWidget(views_group)

        navigation_group = QGroupBox("NAVIGATION")

        navigation_layout = QGridLayout(
            navigation_group
        )

        navigation = [
            ("Zoom +", "ZOOM_IN"),
            ("Zoom -", "ZOOM_OUT"),
            ("Fit", "FIT"),
            ("Pan", "PAN"),
        ]

        for index, (text, command) in enumerate(navigation):

            button = QPushButton(text)

            button.clicked.connect(
                lambda checked=False, cmd=command:
                self.viewRequested.emit(cmd)
            )

            row = index // 2
            column = index % 2

            navigation_layout.addWidget(
                button,
                row,
                column
            )

        layout.addWidget(
            navigation_group
        )

        layout.addStretch()
