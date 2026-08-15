from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
)


class CoordinateCanvas(QWidget):

    def __init__(self, coordinate_label):
        super().__init__()

        self.coordinate_label = coordinate_label

        self.setMouseTracking(True)

        self.x = 0.0
        self.y = 0.0

        self.setMinimumSize(800, 500)

    def mouseMoveEvent(self, event):

        pos = event.position()

        self.x = pos.x()
        self.y = self.height() - pos.y()

        # نمایش مختصات
        self.coordinate_label.setText(
            f"X: {self.x:.2f}    Y: {self.y:.2f}"
        )

        self.update()

        super().mouseMoveEvent(event)

    def paintEvent(self, event):

        painter = QPainter(self)

        # زمینه
        painter.fillRect(
            self.rect(),
            Qt.white
        )

        # محور X
        painter.setPen(
            QPen(Qt.lightGray, 1)
        )

        painter.drawLine(
            0,
            self.height() // 2,
            self.width(),
            self.height() // 2
        )

        # محور Y
        painter.drawLine(
            self.width() // 2,
            0,
            self.width() // 2,
            self.height()
        )

        # نشانگر موس
        mx = int(self.x)
        my = int(self.height() - self.y)

        painter.setPen(
            QPen(Qt.red, 2)
        )

        painter.drawLine(
            mx - 8,
            my,
            mx + 8,
            my
        )

        painter.drawLine(
            mx,
            my - 8,
            mx,
            my + 8
        )

        # مختصات کنار موس
        painter.setPen(Qt.black)
        painter.setFont(
            QFont("Arial", 10)
        )

        painter.drawText(
            mx + 12,
            my - 12,
            f"({self.x:.2f}, {self.y:.2f})"
        )


class CoordinateWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "MCI SoftEngine - Coordinate System"
        )

        self.resize(1000, 650)

        layout = QVBoxLayout(self)

        self.coordinate_label = QLabel(
            "X: 0.00    Y: 0.00"
        )

        self.coordinate_label.setAlignment(
            Qt.AlignCenter
        )

        self.coordinate_label.setStyleSheet(
            """
            QLabel {
                background-color: #202020;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
            }
            """
        )

        layout.addWidget(
            self.coordinate_label
        )

        self.canvas = CoordinateCanvas(
            self.coordinate_label
        )

        layout.addWidget(
            self.canvas
        )


def main():

    app = QApplication(sys.argv)

    window = CoordinateWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()