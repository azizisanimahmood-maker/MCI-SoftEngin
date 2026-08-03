from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget


class Canvas(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMouseTracking(True)

        self.entities = []

        self.renderer = None

        self.background = Qt.black

    def set_renderer(self, renderer):

        self.renderer = renderer

    def set_entities(self, entities):

        self.entities = entities

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing,
            True
        )

        if self.renderer:

            self.renderer.draw(
                self,
                self.entities
            )

    def clear(self, color):

        self.background = color

    def update_canvas(self):

        self.update()

    def mousePressEvent(self, event):

        pass

    def mouseMoveEvent(self, event):

        pass

    def mouseReleaseEvent(self, event):

        pass

    def wheelEvent(self, event):

        pass

    def resizeEvent(self, event):

        super().resizeEvent(event)