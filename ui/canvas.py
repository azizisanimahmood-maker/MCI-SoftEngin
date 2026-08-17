from __future__ import annotations

import math

from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPainter, QFont, QPen, QPolygonF, QPainterPath
from PySide6.QtWidgets import QWidget


class Canvas(QWidget):
    """Interactive CAD canvas.

    The canvas owns the mouse interaction state.  It creates entities in the
    same dictionary shapes used by DrawingCommands and the renderer.
    """

    mouse_world_position = Signal(float, float)
    commandFinished = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        self.entities = []
        self.renderer = None
        self.background = Qt.GlobalColor.black

        # Selection
        self.selected_entity = -1

        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0

        self.mouse_x = 0.0
        self.mouse_y = 0.0

        self.active_command = ""
        self.command_points = []
        self.preview_point = None
        self.polygon_sides = 5

        self._panning = False
        self._pan_start = QPointF()
        self._pan_origin_x = 0.0
        self._pan_origin_y = 0.0

    # =====================================================
    # RENDERER / ENTITIES
    # =====================================================

    def set_renderer(self, renderer):
        self.renderer = renderer
        self.update()

    def set_entities(self, entities):
        self.entities = entities if entities is not None else []
        self.update()

    # =====================================================
    # COMMAND STATE
    # =====================================================

    def start_command(self, command):
        self.active_command = str(command).strip().upper()
        self.command_points = []
        self.preview_point = None
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.update()

    def cancel_command(self):
        if self.active_command:
            self.commandFinished.emit("CANCEL")
        self.active_command = ""
        self.command_points = []
        self.preview_point = None
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.update()

    def _finish_command(self, command):
        self.commandFinished.emit(command)
        self.active_command = ""
        self.command_points = []
        self.preview_point = None
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.update()

    def _add_entity(self, entity, command):
        self.entities.append(entity)
        self._finish_command(command)

    # =====================================================
    # PAINT
    # =====================================================

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True
        )

        painter.fillRect(
            self.rect(),
            self.background
        )

        # -------------------------------------------------
        # Main renderer
        # -------------------------------------------------
        if self.renderer:
            self.renderer.render(
                painter,
                self,
                self.entities
            )

        # -------------------------------------------------
        # Additional entities
        # -------------------------------------------------
        self._draw_extra_entities(painter)

        # -------------------------------------------------
        # Selection
        # -------------------------------------------------
        self._draw_selection(painter)

        # -------------------------------------------------
        # Command preview
        # -------------------------------------------------
        self.draw_preview(painter)

        # -------------------------------------------------
        # Dynamic Input
        # -------------------------------------------------
        painter.save()

        dynamic_font = QFont()
        dynamic_font.setPointSize(10)
        dynamic_font.setBold(True)
        painter.setFont(dynamic_font)

        painter.setPen(
            QPen(Qt.GlobalColor.yellow)
        )

        if self.active_command:
            cmd = self.active_command

            painter.drawText(
                15,
                28,
                f"Command: {cmd}"
            )

            painter.drawText(
                15,
                50,
                f"X: {self.mouse_x:.2f}"
                f"    Y: {self.mouse_y:.2f}"
            )

            # ---------------------------------------------
            # LINE dynamic information
            # ---------------------------------------------
            if (
                cmd == "LINE"
                and len(self.command_points) == 1
                and self.preview_point is not None
            ):
                p1 = self.command_points[0]
                p2 = self.preview_point

                dx = p2.x() - p1.x()
                dy = p2.y() - p1.y()

                distance = math.hypot(dx, dy)

                angle = math.degrees(
                    math.atan2(dy, dx)
                )

                if angle < 0:
                    angle += 360.0

                painter.drawText(
                    15,
                    72,
                    f"Length: {distance:.2f}"
                    f"    Angle: {angle:.2f}?"
                )

                painter.drawText(
                    15,
                    94,
                    f"?X: {dx:.2f}"
                    f"    ?Y: {dy:.2f}"
                )

            # ---------------------------------------------
            # General dynamic information
            # ---------------------------------------------
            elif (
                self.preview_point is not None
                and len(self.command_points) > 0
            ):
                p1 = self.command_points[-1]
                p2 = self.preview_point

                dx = p2.x() - p1.x()
                dy = p2.y() - p1.y()

                distance = math.hypot(dx, dy)

                angle = math.degrees(
                    math.atan2(dy, dx)
                )

                if angle < 0:
                    angle += 360.0

                painter.drawText(
                    15,
                    72,
                    f"Length: {distance:.2f}"
                    f"    Angle: {angle:.2f}?"
                )

        else:
            painter.setPen(
                QPen(Qt.GlobalColor.white)
            )

            painter.drawText(
                15,
                25,
                f"X = {self.mouse_x:.2f}"
                f"    Y = {self.mouse_y:.2f}"
            )

        painter.restore()

        painter.end()

    # =====================================================
    # ENTITY DRAWING FALLBACK
    # =====================================================

    def _draw_extra_entities(self, painter):
        pen = QPen(Qt.GlobalColor.white)
        pen.setWidth(2)
        painter.setPen(pen)

        for entity in self.entities:
            if not isinstance(entity, dict):
                continue
            typ = str(entity.get("type", "")).upper()

            if typ == "PLINE":
                points = entity.get("points") or []
                if len(points) >= 2:
                    screen_points = []
                    for p in points:
                        wp = p if isinstance(p, QPointF) else QPointF(*p)
                        screen_points.append(self.world_to_screen(wp))
                    painter.drawPolyline(QPolygonF(screen_points))

            elif typ == "POLYGON":
                points = entity.get("points") or []
                if len(points) >= 3:
                    screen_points = []
                    for p in points:
                        wp = p if isinstance(p, QPointF) else QPointF(*p)
                        screen_points.append(self.world_to_screen(wp))
                    painter.drawPolygon(QPolygonF(screen_points))

            elif typ == "ELLIPSE":
                center = entity.get("center")
                rx = entity.get("rx")
                ry = entity.get("ry")
                if center is not None and rx is not None and ry is not None:
                    c = self.world_to_screen(center if isinstance(center, QPointF) else QPointF(*center))
                    painter.drawEllipse(c, abs(rx) * self.zoom, abs(ry) * self.zoom)

            elif typ == "ARC":
                center = entity.get("center")
                radius = entity.get("radius")
                start = entity.get("start", entity.get("start_angle"))
                end = entity.get("end", entity.get("end_angle"))
                if center is None or radius is None or start is None or end is None:
                    continue
                c = center if isinstance(center, QPointF) else QPointF(*center)
                path = self._arc_path((c.x(), c.y()), radius, start, end)
                painter.drawPath(path)

    def _arc_path(self, center, radius, start_deg, end_deg):
        # World coordinates use +Y upward, so construct the arc in world
        # space and convert every sample through world_to_screen().
        span = float(end_deg) - float(start_deg)
        if abs(span) < 1e-9:
            span = 360.0
        steps = max(12, int(abs(span) / 4.0))
        path = QPainterPath()
        for i in range(steps + 1):
            a = math.radians(float(start_deg) + span * i / steps)
            if isinstance(center, QPointF):
                cx, cy = center.x(), center.y()
            else:
                cx, cy = float(center[0]), float(center[1])
            p = QPointF(
                float(cx) + float(radius) * math.cos(a),
                float(cy) + float(radius) * math.sin(a),
            )
            sp = self.world_to_screen(p)
            if i == 0:
                path.moveTo(sp)
            else:
                path.lineTo(sp)
        return path

    # =====================================================
    # SELECTION HIGHLIGHT
    # =====================================================

    def _draw_selection(self, painter):
        index = self.selected_entity

        if index < 0 or index >= len(self.entities):
            return

        entity = self.entities[index]

        if not isinstance(entity, dict):
            return

        pen = QPen(Qt.GlobalColor.yellow)
        pen.setWidth(4)
        painter.setPen(pen)

        typ = str(entity.get("type", "")).upper()

        if typ == "LINE":
            p1 = entity.get("p1", entity.get("start"))
            p2 = entity.get("p2", entity.get("end"))

            if p1 is not None and p2 is not None:
                p1 = p1 if isinstance(p1, QPointF) else QPointF(*p1)
                p2 = p2 if isinstance(p2, QPointF) else QPointF(*p2)

                painter.drawLine(
                    self.world_to_screen(p1),
                    self.world_to_screen(p2)
                )

        elif typ in ("RECTANG", "RECTANGLE"):
            p1 = entity.get("p1", entity.get("start"))
            p2 = entity.get("p2", entity.get("end"))

            if p1 is not None and p2 is not None:
                self._draw_rect(painter, p1, p2)

        elif typ == "CIRCLE":
            center = entity.get("center")
            radius = entity.get("radius")

            if center is not None and radius is not None:
                center = (
                    center
                    if isinstance(center, QPointF)
                    else QPointF(*center)
                )

                painter.drawEllipse(
                    self.world_to_screen(center),
                    abs(float(radius)) * self.zoom,
                    abs(float(radius)) * self.zoom
                )

        elif typ == "POINT":
            point = entity.get("point")

            if point is not None:
                point = (
                    point
                    if isinstance(point, QPointF)
                    else QPointF(*point)
                )
                self._draw_point(painter, point)

        elif typ in ("PLINE", "POLYGON"):
            points = entity.get("points") or []

            if len(points) >= 2:
                screen_points = [
                    self.world_to_screen(
                        p if isinstance(p, QPointF) else QPointF(*p)
                    )
                    for p in points
                ]

                if typ == "POLYGON":
                    painter.drawPolygon(QPolygonF(screen_points))
                else:
                    painter.drawPolyline(QPolygonF(screen_points))

        elif typ == "ELLIPSE":
            center = entity.get("center")
            rx = entity.get("rx")
            ry = entity.get("ry")

            if center is not None and rx is not None and ry is not None:
                center = (
                    center
                    if isinstance(center, QPointF)
                    else QPointF(*center)
                )

                painter.drawEllipse(
                    self.world_to_screen(center),
                    abs(float(rx)) * self.zoom,
                    abs(float(ry)) * self.zoom
                )

        elif typ == "ARC":
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
                center is not None
                and radius is not None
                and start is not None
                and end is not None
            ):
                center = (
                    center
                    if isinstance(center, QPointF)
                    else QPointF(*center)
                )

                painter.drawPath(
                    self._arc_path(
                        (center.x(), center.y()),
                        radius,
                        start,
                        end
                    )
                )

    # =====================================================
    # PREVIEW
    # =====================================================

    def draw_preview(self, painter):
        if not self.active_command or self.preview_point is None:
            return

        pen = QPen(Qt.GlobalColor.yellow)
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)

        cmd = self.active_command
        pts = self.command_points
        cur = self.preview_point

        if cmd == "LINE" and len(pts) == 1:
            painter.drawLine(self.world_to_screen(pts[0]), self.world_to_screen(cur))
            return

        if cmd in ("RECTANG", "RECTANGLE") and len(pts) == 1:
            self._draw_rect(painter, pts[0], cur)
            return

        if cmd == "CIRCLE" and len(pts) == 1:
            r = self._distance(pts[0], cur)
            painter.drawEllipse(self.world_to_screen(pts[0]), r * self.zoom, r * self.zoom)
            return

        if cmd == "POINT":
            self._draw_point(painter, cur)
            return

        if cmd in ("PLINE", "POLYLINE") and pts:
            screen = [self.world_to_screen(p) for p in pts]
            screen.append(self.world_to_screen(cur))
            painter.drawPolyline(QPolygonF(screen))
            return

        if cmd == "ARC":
            if len(pts) == 1:
                r = self._distance(pts[0], cur)
                painter.drawEllipse(self.world_to_screen(pts[0]), r * self.zoom, r * self.zoom)
            elif len(pts) == 2:
                center = pts[0]
                r = self._distance(center, pts[1])
                start = math.degrees(math.atan2(pts[1].y() - center.y(), pts[1].x() - center.x()))
                end = math.degrees(math.atan2(cur.y() - center.y(), cur.x() - center.x()))
                painter.drawPath(self._arc_path((center.x(), center.y()), r, start, end))
            return

        if cmd == "ELLIPSE":
            if len(pts) == 1:
                painter.drawEllipse(self.world_to_screen(pts[0]),
                                    abs(cur.x() - pts[0].x()) * self.zoom,
                                    abs(cur.y() - pts[0].y()) * self.zoom)
            elif len(pts) == 2:
                center = pts[0]
                rx = self._distance(center, pts[1])
                ry = abs(cur.y() - center.y())
                painter.drawEllipse(self.world_to_screen(center), rx * self.zoom, ry * self.zoom)
            return

        if cmd == "POLYGON" and len(pts) == 1:
            self._draw_polygon_preview(painter, pts[0], cur, self.polygon_sides)

    def _draw_rect(self, painter, p1, p2):
        a = self.world_to_screen(p1)
        b = self.world_to_screen(p2)
        left, right = sorted((a.x(), b.x()))
        top, bottom = sorted((a.y(), b.y()))
        painter.drawRect(int(left), int(top), int(right - left), int(bottom - top))

    def _draw_point(self, painter, point):
        p = self.world_to_screen(point)
        s = 5
        painter.drawLine(int(p.x() - s), int(p.y()), int(p.x() + s), int(p.y()))
        painter.drawLine(int(p.x()), int(p.y() - s), int(p.x()), int(p.y() + s))

    def _draw_polygon_preview(self, painter, center, edge, sides):
        radius = self._distance(center, edge)
        points = []
        for i in range(max(3, sides)):
            a = 2.0 * math.pi * i / max(3, sides)
            points.append(self.world_to_screen(QPointF(
                center.x() + radius * math.cos(a),
                center.y() + radius * math.sin(a),
            )))
        painter.drawPolygon(QPolygonF(points))

    # =====================================================
    # COORDINATE TRANSFORMS
    # =====================================================

    def screen_to_world(self, point):
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        return QPointF(
            (point.x() - cx) / self.zoom - self.pan_x,
            (cy - point.y()) / self.zoom - self.pan_y,
        )

    def world_to_screen(self, point):
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        return QPointF(
            cx + (point.x() + self.pan_x) * self.zoom,
            cy - (point.y() + self.pan_y) * self.zoom,
        )

    @staticmethod
    def _distance(a, b):
        return math.hypot(b.x() - a.x(), b.y() - a.y())

    # =====================================================
    # MOUSE
    # =====================================================

    def mouseMoveEvent(self, event):
        world = self.screen_to_world(event.position())
        self.mouse_x = world.x()
        self.mouse_y = world.y()
        self.mouse_world_position.emit(self.mouse_x, self.mouse_y)

        if self._panning:
            delta = event.position() - self._pan_start
            self.pan_x = self._pan_origin_x + delta.x() / self.zoom
            self.pan_y = self._pan_origin_y - delta.y() / self.zoom

        if self.active_command:
            self.preview_point = QPointF(world)

        self.update()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = True
            self._pan_start = event.position()
            self._pan_origin_x = self.pan_x
            self._pan_origin_y = self.pan_y
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
            return

        if event.button() == Qt.MouseButton.RightButton:
            if self.active_command:
                self.cancel_command()
                event.accept()
                return

        if event.button() == Qt.MouseButton.LeftButton:
            world_point = self.screen_to_world(event.position())

            if self.active_command:
                self.handle_command_click(world_point)
            else:
                self.select_entity(world_point)

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.active_command in ("PLINE", "POLYLINE"):
            if len(self.command_points) >= 2:
                self._add_entity({
                    "type": "PLINE",
                    "points": [(p.x(), p.y()) for p in self.command_points],
                }, "PLINE")
            else:
                self.cancel_command()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    # =====================================================
    # SELECTION
    # =====================================================

    def select_entity(self, point):
        """Select the nearest entity under the mouse."""

        best_index = -1
        best_distance = float("inf")

        tolerance = max(8.0 / self.zoom, 5.0)

        for index, entity in enumerate(self.entities):
            if not isinstance(entity, dict):
                continue

            distance = self._entity_distance(entity, point)

            if distance <= tolerance and distance < best_distance:
                best_distance = distance
                best_index = index

        self.selected_entity = best_index
        self.update()

    def _entity_distance(self, entity, point):
        typ = str(entity.get("type", "")).upper()

        if typ == "LINE":
            p1 = entity.get("p1", entity.get("start"))
            p2 = entity.get("p2", entity.get("end"))

            if p1 is None or p2 is None:
                return float("inf")

            p1 = p1 if isinstance(p1, QPointF) else QPointF(*p1)
            p2 = p2 if isinstance(p2, QPointF) else QPointF(*p2)

            return self._distance_to_segment(point, p1, p2)

        if typ in ("RECTANG", "RECTANGLE"):
            p1 = entity.get("p1", entity.get("start"))
            p2 = entity.get("p2", entity.get("end"))

            if p1 is None or p2 is None:
                return float("inf")

            p1 = p1 if isinstance(p1, QPointF) else QPointF(*p1)
            p2 = p2 if isinstance(p2, QPointF) else QPointF(*p2)

            corners = [
                QPointF(p1.x(), p1.y()),
                QPointF(p2.x(), p1.y()),
                QPointF(p2.x(), p2.y()),
                QPointF(p1.x(), p2.y()),
            ]

            distances = []

            for i in range(4):
                distances.append(
                    self._distance_to_segment(
                        point,
                        corners[i],
                        corners[(i + 1) % 4]
                    )
                )

            return min(distances)

        if typ in ("CIRCLE", "ARC"):
            center = entity.get("center")
            radius = entity.get("radius")

            if center is None or radius is None:
                return float("inf")

            center = (
                center
                if isinstance(center, QPointF)
                else QPointF(*center)
            )

            return abs(self._distance(center, point) - abs(float(radius)))

        if typ == "POINT":
            p = entity.get("point")

            if p is None:
                return float("inf")

            p = p if isinstance(p, QPointF) else QPointF(*p)

            return self._distance(p, point)

        if typ in ("PLINE", "POLYGON"):
            points = entity.get("points") or []

            if len(points) < 2:
                return float("inf")

            pts = [
                p if isinstance(p, QPointF) else QPointF(*p)
                for p in points
            ]

            distances = []

            for i in range(len(pts) - 1):
                distances.append(
                    self._distance_to_segment(
                        point,
                        pts[i],
                        pts[i + 1]
                    )
                )

            if typ == "POLYGON" and len(pts) >= 3:
                distances.append(
                    self._distance_to_segment(
                        point,
                        pts[-1],
                        pts[0]
                    )
                )

            return min(distances)

        if typ == "ELLIPSE":
            center = entity.get("center")
            rx = entity.get("rx")
            ry = entity.get("ry")

            if center is None or rx is None or ry is None:
                return float("inf")

            center = (
                center
                if isinstance(center, QPointF)
                else QPointF(*center)
            )

            if rx == 0 or ry == 0:
                return float("inf")

            dx = point.x() - center.x()
            dy = point.y() - center.y()

            value = ((dx / rx) ** 2 + (dy / ry) ** 2)

            return abs(value - 1.0) * max(abs(rx), abs(ry))

        return float("inf")

    @staticmethod
    def _distance_to_segment(point, a, b):
        dx = b.x() - a.x()
        dy = b.y() - a.y()

        length2 = dx * dx + dy * dy

        if length2 == 0:
            return math.hypot(
                point.x() - a.x(),
                point.y() - a.y()
            )

        t = (
            (point.x() - a.x()) * dx
            + (point.y() - a.y()) * dy
        ) / length2

        t = max(0.0, min(1.0, t))

        px = a.x() + t * dx
        py = a.y() + t * dy

        return math.hypot(
            point.x() - px,
            point.y() - py
        )

    # =====================================================
    # COMMAND CLICK
    # =====================================================

    def handle_command_click(self, point):
        point = QPointF(point)
        cmd = self.active_command

        # =============================================
        # MOVE
        # =============================================

        if cmd == "MOVE":

            if self.selected_entity < 0:
                self.statusBarMessage.emit(
                    "MOVE: ????? ?? Entity ?? ?????? ????"
                ) if hasattr(self, "statusBarMessage") else None
                self.cancel_command()
                return

            if len(self.command_points) == 0:

                self.command_points.append(point)
                self.preview_point = point
                self.update()
                return

            base = self.command_points[0]

            dx = point.x() - base.x()
            dy = point.y() - base.y()

            entity = self.entities[self.selected_entity]

            typ = str(
                entity.get("type", "")
            ).upper()

            def move_point(p):
                if isinstance(p, QPointF):
                    return (
                        p.x() + dx,
                        p.y() + dy
                    )

                return (
                    float(p[0]) + dx,
                    float(p[1]) + dy
                )

            if typ in ("LINE", "RECTANG", "RECTANGLE"):

                p1 = entity.get(
                    "p1",
                    entity.get("start")
                )

                p2 = entity.get(
                    "p2",
                    entity.get("end")
                )

                if p1 is not None and p2 is not None:

                    entity["p1"] = move_point(p1)
                    entity["p2"] = move_point(p2)

                    entity["start"] = entity["p1"]
                    entity["end"] = entity["p2"]

            elif typ in ("CIRCLE", "ARC", "ELLIPSE"):

                center = entity.get("center")

                if center is not None:
                    entity["center"] = move_point(center)

            elif typ == "POINT":

                p = entity.get("point")

                if p is not None:
                    entity["point"] = move_point(p)

            elif typ in ("PLINE", "POLYGON"):

                points = entity.get("points", [])

                entity["points"] = [
                    move_point(p)
                    for p in points
                ]

            self._finish_command("MOVE")
            return

        # =============================================
        # LINE
        # =============================================

        if cmd == "LINE":

            self.command_points.append(point)

            if len(self.command_points) == 2:

                p1, p2 = self.command_points

                self._add_entity({
                    "type": "LINE",
                    "start": QPointF(p1),
                    "end": QPointF(p2),
                    "p1": QPointF(p1),
                    "p2": QPointF(p2),
                }, "LINE")

            return

        # =============================================
        # RECTANG
        # =============================================

        if cmd in ("RECTANG", "RECTANGLE"):

            self.command_points.append(point)

            if len(self.command_points) == 2:

                p1, p2 = self.command_points

                self._add_entity({
                    "type": "RECTANG",
                    "start": QPointF(p1),
                    "end": QPointF(p2),
                    "p1": QPointF(p1),
                    "p2": QPointF(p2),
                }, "RECTANG")

            return

        # =============================================
        # CIRCLE
        # =============================================

        if cmd == "CIRCLE":

            self.command_points.append(point)

            if len(self.command_points) == 2:

                center = self.command_points[0]

                radius = self._distance(
                    center,
                    self.command_points[1]
                )

                if radius > 0:

                    self._add_entity({
                        "type": "CIRCLE",
                        "center": QPointF(center),
                        "radius": radius,
                    }, "CIRCLE")

            return

        # =============================================
        # POINT
        # =============================================

        if cmd == "POINT":

            self._add_entity({
                "type": "POINT",
                "point": QPointF(point),
            }, "POINT")

            return

        # =============================================
        # PLINE
        # =============================================

        if cmd in ("PLINE", "POLYLINE"):

            self.command_points.append(point)
            self.update()
            return

        # =============================================
        # ARC
        # =============================================

        if cmd == "ARC":

            self.command_points.append(point)

            if len(self.command_points) == 3:

                center, start_point, end_point = (
                    self.command_points
                )

                radius = self._distance(
                    center,
                    start_point
                )

                if radius > 0:

                    start = math.degrees(
                        math.atan2(
                            start_point.y() - center.y(),
                            start_point.x() - center.x(),
                        )
                    )

                    end = math.degrees(
                        math.atan2(
                            end_point.y() - center.y(),
                            end_point.x() - center.x(),
                        )
                    )

                    self._add_entity({
                        "type": "ARC",
                        "center": QPointF(center),
                        "radius": radius,
                        "start": start,
                        "end": end,
                        "start_angle": start,
                        "end_angle": end,
                    }, "ARC")

            return

        # =============================================
        # ELLIPSE
        # =============================================

        if cmd == "ELLIPSE":

            self.command_points.append(point)

            if len(self.command_points) == 3:

                center, x_point, y_point = (
                    self.command_points
                )

                rx = self._distance(
                    center,
                    x_point
                )

                ry = abs(
                    y_point.y() - center.y()
                )

                if rx > 0 and ry > 0:

                    self._add_entity({
                        "type": "ELLIPSE",
                        "center": (
                            center.x(),
                            center.y()
                        ),
                        "rx": rx,
                        "ry": ry,
                    }, "ELLIPSE")

            return

        # =============================================
        # POLYGON
        # =============================================

        if cmd == "POLYGON":

            self.command_points.append(point)

            if len(self.command_points) == 2:

                center, edge = (
                    self.command_points
                )

                radius = self._distance(
                    center,
                    edge
                )

                sides = max(
                    3,
                    int(self.polygon_sides)
                )

                points = []

                for i in range(sides):

                    a = (
                        2.0 *
                        math.pi *
                        i /
                        sides
                    )

                    points.append((
                        center.x() +
                        radius *
                        math.cos(a),

                        center.y() +
                        radius *
                        math.sin(a),
                    ))

                self._add_entity({
                    "type": "POLYGON",
                    "points": points,
                }, "POLYGON")

            return

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = False
            self.setCursor(
                Qt.CursorShape.CrossCursor
                if self.active_command
                else Qt.CursorShape.ArrowCursor
            )
            event.accept()
            return
        super().mouseReleaseEvent(event)

    # =====================================================
    # ZOOM
    # =====================================================

    def wheelEvent(self, event):
        mouse_pos = event.position()
        old_world = self.screen_to_world(mouse_pos)
        delta = event.angleDelta().y()

        if delta > 0:
            factor = 1.2
        elif delta < 0:
            factor = 1.0 / 1.2
        else:
            return

        self.zoom = max(0.05, min(self.zoom * factor, 100.0))
        new_world = self.screen_to_world(mouse_pos)
        self.pan_x += new_world.x() - old_world.x()
        self.pan_y += new_world.y() - old_world.y()
        self.update()
        event.accept()

    # =====================================================
    # HELPERS
    # =====================================================

    def clear(self, color):
        self.background = color
        self.update()

    def update_canvas(self):
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
