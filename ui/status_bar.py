from __future__ import annotations

from PySide6.QtWidgets import QStatusBar, QLabel


class StatusBar(QStatusBar):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.coord_label = QLabel("X:0  Y:0")

        self.snap_label = QLabel("SNAP")

        self.layer_label = QLabel("Layer:0")

        self.message_label = QLabel("Ready")

        self.addPermanentWidget(self.coord_label)

        self.addPermanentWidget(self.snap_label)

        self.addPermanentWidget(self.layer_label)

        self.addWidget(self.message_label)

    def set_coordinates(self, x, y):

        self.coord_label.setText(
            f"X:{x:.3f}  Y:{y:.3f}"
        )

    def set_layer(self, layer):

        self.layer_label.setText(
            f"Layer:{layer}"
        )

    def set_snap(self, enabled):

        self.snap_label.setText(
            "SNAP ON" if enabled else "SNAP OFF"
        )

    def show_message(self, text):

        self.message_label.setText(text)