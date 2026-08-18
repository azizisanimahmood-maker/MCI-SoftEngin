from __future__ import annotations

import math

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPen, QPolygonF, QPainterPath


class Renderer:
    """Main 2D renderer for MCI SoftEngine CAD canvas."""

    def __init__(self):
        self.grid_minor = 25
        self.grid_major = 125

    # =====================================================
    # WORLD -> SCREEN
    # =====================================================

    def world_to_screen(self, canvas, point):
        if isinstance(point, QPointF):
            x = point.x()
            y = point.y()
        elif isinstance(point, (tuple, list)):
            x = float(point[0])
            y = float(point[1])
        else:
            x = float(point.x())
            y = float(point.y())

        cx = canvas.width() / 2.0
        cy = canvas.height() / 2.0

        return QPointF(
            cx + (x + canvas.pan_x) * canvas.zoom,
            cy - (y + canvas.pan_y) * canvas.zoom,
        )

    # =====================================================
    # SCREEN -> WORLD
    # =====================================================

    def screen_to_world(self, canvas, point):
        cx = canvas.width() / 2.0
        cy = canvas.height() / 2.0

        return QPointF(
            (point.x() - cx) / canvas.zoom - canvas.pan_x,
            (cy - point.y()) / canvas.zoom - canvas.pan_y,
        )

    # =====================================================
    # MAIN RENDER
    # =====================================================

    def render(self, painter, canvas, entities):
        self.draw_grid(painter, canvas)
        self.draw_axes(painter, canvas)
        self.draw_entities(painter, canvas, entities)

    # =====================================================
    # GRID
    # =====================================================

    def draw_grid(self, painter, canvas):
        zoom = max(float(canvas.zoom), 0.0001)

        minor_screen = self.grid_minor * zoom
        major_screen = self.grid_major * zoom

        # Keep the grid readable during zoom.
        if minor_screen < 8:
            minor_world = self.grid_minor

            while minor_world * zoom < 8:
                minor_world *= 2

            minor_screen = minor_world * zoom
        else:
            minor_world = self.grid_minor

        major_world = minor_world * 5
        major_screen = major_world * zoom

        width = canvas.width()
        height = canvas.height()

        cx = width / 2.0
        cy = height / 2.0

        # World coordinate range visible on screen.
        left_world = (-cx / zoom) - canvas.pan_x
        right_world = ((width - cx) / zoom) - canvas.pan_x

        bottom_world = ((cy - height) / zoom) - canvas.pan_y
        top_world = (cy / zoom) - canvas.pan_y

        # -------------------------------------------------
        # Minor grid
        # -------------------------------------------------

        minor_pen = QPen(Qt.GlobalColor.darkGray)
        minor_pen.setWidth(1)
        painter.setPen(minor_pen)

        start_x = math.floor(left_world / minor_world) * minor_world
        x = start_x

        while x <= right_world:
            sx = self.world_to_screen(
                canvas,
                QPointF(x, 0)
            ).x()

            painter.drawLine(
                int(round(sx)),
                0,
                int(round(sx)),
                height
            )

            x += minor_world

        start_y = math.floor(bottom_world / minor_world) * minor_world
        y = start_y

        while y <= top_world:
            sy = self.world_to_screen(
                canvas,
                QPointF(0, y)
            ).y()

            painter.drawLine(
                0,
                int(round(sy)),
                width,
                int(round(sy))
            )

            y += minor_world

        # -------------------------------------------------
        # Major grid
        # -------------------------------------------------

        major_pen = QPen(Qt.GlobalColor.gray)
        major_pen.setWidth(1)
        painter.setPen(major_pen)

        start_x = math.floor(left_world / major_world) * major_world
        x = start_x

        while x <= right_world:
            sx = self.world_to_screen(
                canvas,
                QPointF(x, 0)
            ).x()

            painter.drawLine(
                int(round(sx)),
                0,
                int(round(sx)),
                height
            )

            x += major_world

        start_y = math.floor(bottom_world / major_world) * major_world
        y = start_y

        while y <= top_world:
            sy = self.world_to_screen(
                canvas,
                QPointF(0, y)
            ).y()

            painter.drawLine(
                0,
                int(round(sy)),
                width,
                int(round(sy))
            )

            y += major_world

    # =====================================================
    # AXES
    # =====================================================

    def draw_axes(self, painter, canvas):
        width = canvas.width()
        height = canvas.height()

        origin = self.world_to_screen(
            canvas,
            QPointF(0, 0)
        )

        ox = int(round(origin.x()))
        oy = int(round(origin.y()))

        axis_pen = QPen(Qt.GlobalColor.cyan)
        axis_pen.setWidth(2)
        painter.setPen(axis_pen)

        # X axis
        if 0 <= oy <= height:
            painter.drawLine(
                0,
                oy,
                width,
                oy
            )

        # Y axis
        if 0 <= ox <= width:
            painter.drawLine(
                ox,
                0,
                ox,
                height
            )

    # =====================================================
    # ENTITIES
    # =====================================================

    def draw_entities(self, painter, canvas, entities):
        if not entities:
            return

        pen = QPen(Qt.GlobalColor.white)
        pen.setWidth(2)
        painter.setPen(pen)

        for entity in entities:
            if not isinstance(entity, dict):
                continue

            typ = str(
                entity.get("type", "")
            ).upper()

            if typ == "LINE":
                self.draw_line(
                    painter,
                    canvas,
                    entity
                )

            elif typ in ("RECTANG", "RECTANGLE"):
                self.draw_rectangle(
                    painter,
                    canvas,
                    entity
                )

            elif typ == "CIRCLE":
                self.draw_circle(
                    painter,
                    canvas,
                    entity
                )

            elif typ == "POINT":
                self.draw_point(
                    painter,
                    canvas,
                    entity
                )

            elif typ in ("PLINE", "POLYLINE"):
                self.draw_polyline(
                    painter,
                    canvas,
                    entity
                )

            elif typ == "POLYGON":
                self.draw_polygon(
                    painter,
                    canvas,
                    entity
                )

            elif typ == "ELLIPSE":
                self.draw_ellipse(
                    painter,
                    canvas,
                    entity
                )

            elif typ == "ARC":
                self.draw_arc(
                    painter,
                    canvas,
                    entity
                )

    # =====================================================
    # LINE
    # =====================================================

    def draw_line(self, painter, canvas, entity):
        p1 = entity.get(
            "p1",
            entity.get("start")
        )

        p2 = entity.get(
            "p2",
            entity.get("end")
        )

        if p1 is None or p2 is None:
            return

        painter.drawLine(
            self.world_to_screen(canvas, p1),
            self.world_to_screen(canvas, p2)
        )

    # =====================================================
    # RECTANGLE
    # =====================================================

    def draw_rectangle(self, painter, canvas, entity):
        p1 = entity.get(
            "p1",
            entity.get("start")
        )

        p2 = entity.get(
            "p2",
            entity.get("end")
        )

        if p1 is None or p2 is None:
            return

        a = self.world_to_screen(canvas, p1)
        b = self.world_to_screen(canvas, p2)

        left = min(a.x(), b.x())
        right = max(a.x(), b.x())
        top = min(a.y(), b.y())
        bottom = max(a.y(), b.y())

        painter.drawRect(
            int(round(left)),
            int(round(top)),
            int(round(right - left)),
            int(round(bottom - top))
        )

    # =====================================================
    # CIRCLE
    # =====================================================

    def draw_circle(self, painter, canvas, entity):
        center = entity.get("center")
        radius = entity.get("radius")

        if center is None or radius is None:
            return

        center_screen = self.world_to_screen(
            canvas,
            center
        )

        r = abs(float(radius)) * canvas.zoom

        painter.drawEllipse(
            center_screen,
            r,
            r
        )

    # =====================================================
    # POINT
    # =====================================================

    def draw_point(self, painter, canvas, entity):
        point = entity.get("point")

        if point is None:
            return

        p = self.world_to_screen(
            canvas,
            point
        )

        size = 5

        painter.drawLine(
            int(p.x() - size),
            int(p.y()),
            int(p.x() + size),
            int(p.y())
        )

        painter.drawLine(
            int(p.x()),
            int(p.y() - size),
            int(p.x()),
            int(p.y() + size)
        )

    # =====================================================
    # POLYLINE
    # =====================================================

    def draw_polyline(self, painter, canvas, entity):
        points = entity.get("points") or []

        if len(points) < 2:
            return

        screen_points = [
            self.world_to_screen(canvas, point)
            for point in points
        ]

        painter.drawPolyline(
            QPolygonF(screen_points)
        )

    # =====================================================
    # POLYGON
    # =====================================================

    def draw_polygon(self, painter, canvas, entity):
        points = entity.get("points") or []

        if len(points) < 3:
            return

        screen_points = [
            self.world_to_screen(canvas, point)
            for point in points
        ]

        painter.drawPolygon(
            QPolygonF(screen_points)
        )

    # =====================================================
    # ELLIPSE
    # =====================================================

    def draw_ellipse(self, painter, canvas, entity):
        center = entity.get("center")
        rx = entity.get("rx")
        ry = entity.get("ry")

        if center is None or rx is None or ry is None:
            return

        center_screen = self.world_to_screen(
            canvas,
            center
        )

        painter.drawEllipse(
            center_screen,
            abs(float(rx)) * canvas.zoom,
            abs(float(ry)) * canvas.zoom
        )

    # =====================================================
    # ARC
    # =====================================================

    def draw_arc(self, painter, canvas, entity):
        center = entity.get("center")
        radius = entity.get("radius")

        start = entity.get(
            "start",
            entity.get("start_angle")
        )

        end = entity.get(
            "end",
            entity.get("end_angle")
        )

        if (
            center is None
            or radius is None
            or start is None
            or end is None
        ):
            return

        if isinstance(center, QPointF):
            cx = center.x()
            cy = center.y()
        else:
            cx = float(center[0])
            cy = float(center[1])

        span = float(end) - float(start)

        if abs(span) < 1e-9:
            span = 360.0

        steps = max(
            12,
            int(abs(span) / 4.0)
        )

        path = QPainterPath()

        for i in range(steps + 1):
            angle = math.radians(
                float(start)
                + span * i / steps
            )

            world_point = QPointF(
                cx + float(radius) * math.cos(angle),
                cy + float(radius) * math.sin(angle)
            )

            screen_point = self.world_to_screen(
                canvas,
                world_point
            )

            if i == 0:
                path.moveTo(screen_point)
            else:
                path.lineTo(screen_point)

        painter.drawPath(path)


__all__ = ["Renderer"]
