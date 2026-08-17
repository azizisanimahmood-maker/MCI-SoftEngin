from __future__ import annotations

import math
from PySide6.QtCore import QPointF


class DrawingCommands:
    """
    موتور مرکزی فرمان‌های ترسیمی MCI SoftEngine

    تمام فرمان‌های ترسیمی و ویرایشی از این کلاس عبور می‌کنند.
    """

    def __init__(self, canvas):

        self.canvas = canvas

        # تاریخچه برای UNDO
        self.history = []

    # =====================================================
    # GENERAL
    # =====================================================

    def execute(self, text):

        text = text.strip()

        if not text:
            return ""

        parts = text.split()

        command = parts[0].upper()

        try:

            # -------------------------------------------------
            # DRAW
            # -------------------------------------------------

            if command == "LINE":
                return self.line(parts)

            if command in ("PLINE", "POLYLINE"):
                return self.pline(parts)

            if command in ("RECTANG", "RECTANGLE"):
                return self.rectang(parts)

            if command == "CIRCLE":
                return self.circle(parts)

            if command == "ARC":
                return self.arc(parts)

            if command == "POINT":
                return self.point(parts)

            if command == "POLYGON":
                return self.polygon(parts)

            if command == "ELLIPSE":
                return self.ellipse(parts)

            # -------------------------------------------------
            # MODIFY
            # -------------------------------------------------

            if command == "MOVE":
                return self.move(parts)

            if command == "COPY":
                return self.copy(parts)

            if command == "ROTATE":
                return self.rotate(parts)

            if command == "SCALE":
                return self.scale(parts)

            if command == "MIRROR":
                return self.mirror(parts)

            if command == "OFFSET":
                return self.offset(parts)

            if command == "TRIM":
                return self.trim(parts)

            if command == "EXTEND":
                return self.extend(parts)

            if command in ("ERASE", "DELETE"):
                return self.erase(parts)

            # -------------------------------------------------
            # VIEW
            # -------------------------------------------------

            if command == "ZOOM":
                return self.zoom(parts)

            if command == "PAN":
                return self.pan(parts)

            if command in ("REDRAW", "REGEN"):
                self.canvas.update()
                return "REDRAW انجام شد"

            # -------------------------------------------------
            # GENERAL
            # -------------------------------------------------

            if command == "UNDO":
                return self.undo()

            if command in ("ERASEALL", "CLEAR"):
                return self.erase_all()

            if command == "HELP":
                return self.help()

            return f"فرمان ناشناخته: {command}"

        except Exception as error:

            return f"خطا: {error}"

    # =====================================================
    # POINT PARSER
    # =====================================================

    def parse_point(
        self,
        value,
        previous=None
    ):

        value = value.strip()

        relative = value.startswith("@")

        if relative:
            value = value[1:]

        # ---------------------------------------------
        # Polar coordinate
        # @distance<angle
        # ---------------------------------------------

        if "<" in value:

            distance_text, angle_text = value.split(
                "<",
                1
            )

            distance = float(
                distance_text
            )

            angle = math.radians(
                float(angle_text)
            )

            if previous is None:
                base_x = 0.0
                base_y = 0.0
            else:
                base_x = previous[0]
                base_y = previous[1]

            return (
                base_x + distance * math.cos(angle),
                base_y + distance * math.sin(angle)
            )

        # ---------------------------------------------
        # Cartesian
        # ---------------------------------------------

        if "," not in value:

            raise ValueError(
                f"مختصات نامعتبر: {value}"
            )

        x_text, y_text = value.split(
            ",",
            1
        )

        x = float(x_text)
        y = float(y_text)

        if relative:

            if previous is None:
                previous = (0.0, 0.0)

            return (
                previous[0] + x,
                previous[1] + y
            )

        return x, y

    # =====================================================
    # HISTORY
    # =====================================================

    def save_history(self):

        self.history.append(
            list(self.canvas.entities)
        )

        if len(self.history) > 50:

            self.history.pop(0)

    # =====================================================
    # LINE
    # =====================================================

    def line(self, parts):

        if len(parts) != 3:

            return "LINE: LINE x1,y1 x2,y2"

        self.save_history()

        p1 = self.parse_point(
            parts[1]
        )

        p2 = self.parse_point(
            parts[2],
            p1
        )

        self.canvas.entities.append({

            "type": "LINE",

            "start": p1,

            "end": p2,

            "p1": p1,

            "p2": p2,
        })

        self.canvas.update()

        return "LINE رسم شد"

    # =====================================================
    # PLINE
    # =====================================================

    def pline(self, parts):

        if len(parts) < 3:

            return (
                "PLINE: "
                "PLINE p1 p2 p3 ..."
            )

        self.save_history()

        points = []

        close = (
            parts[-1].upper() == "CLOSE"
        )

        point_parts = (
            parts[1:-1]
            if close
            else parts[1:]
        )

        for value in point_parts:

            previous = (
                points[-1]
                if points
                else None
            )

            points.append(
                self.parse_point(
                    value,
                    previous
                )
            )

        if len(points) < 2:

            return "حداقل دو نقطه لازم است"

        if close:

            points.append(
                points[0]
            )

        self.canvas.entities.append({

            "type": "PLINE",

            "points": points,
        })

        self.canvas.update()

        return "PLINE رسم شد"

    # =====================================================
    # RECTANG
    # =====================================================

    def rectang(self, parts):

        if len(parts) != 3:

            return (
                "RECTANG: "
                "RECTANG p1 p2"
            )

        self.save_history()

        p1 = self.parse_point(
            parts[1]
        )

        p2 = self.parse_point(
            parts[2],
            p1
        )

        self.canvas.entities.append({

            "type": "RECTANG",

            "start": p1,

            "end": p2,

            "p1": p1,

            "p2": p2,
        })

        self.canvas.update()

        return "RECTANG رسم شد"

    # =====================================================
    # CIRCLE
    # =====================================================

    def circle(self, parts):

        if len(parts) != 3:

            return (
                "CIRCLE: "
                "CIRCLE center radius"
            )

        self.save_history()

        center = self.parse_point(
            parts[1]
        )

        radius = float(
            parts[2]
        )

        if radius <= 0:

            return "شعاع باید مثبت باشد"

        self.canvas.entities.append({

            "type": "CIRCLE",

            "center": center,

            "radius": radius,
        })

        self.canvas.update()

        return "CIRCLE رسم شد"

    # =====================================================
    # ARC
    # =====================================================

    def arc(self, parts):

        if len(parts) != 5:

            return (
                "ARC: "
                "ARC center radius start end"
            )

        self.save_history()

        center = self.parse_point(
            parts[1]
        )

        radius = float(
            parts[2]
        )

        start = float(
            parts[3]
        )

        end = float(
            parts[4]
        )

        self.canvas.entities.append({

            "type": "ARC",

            "center": center,

            "radius": radius,

            "start": start,

            "end": end,

            "start_angle": start,

            "end_angle": end,
        })

        self.canvas.update()

        return "ARC رسم شد"

    # =====================================================
    # POINT
    # =====================================================

    def point(self, parts):

        if len(parts) != 2:

            return "POINT: POINT x,y"

        self.save_history()

        p = self.parse_point(
            parts[1]
        )

        self.canvas.entities.append({

            "type": "POINT",

            "point": p,
        })

        self.canvas.update()

        return "POINT ایجاد شد"

    # =====================================================
    # POLYGON
    # =====================================================

    def polygon(self, parts):

        if len(parts) != 4:

            return (
                "POLYGON: "
                "POLYGON sides center radius"
            )

        self.save_history()

        sides = int(parts[1])

        if sides < 3:

            return "حداقل 3 ضلع لازم است"

        center = self.parse_point(
            parts[2]
        )

        radius = float(
            parts[3]
        )

        points = []

        for i in range(sides):

            angle = (
                2.0 *
                math.pi *
                i /
                sides
            )

            x = (
                center[0]
                + radius *
                math.cos(angle)
            )

            y = (
                center[1]
                + radius *
                math.sin(angle)
            )

            points.append(
                (x, y)
            )

        self.canvas.entities.append({

            "type": "POLYGON",

            "points": points,
        })

        self.canvas.update()

        return "POLYGON رسم شد"

    # =====================================================
    # ELLIPSE
    # =====================================================

    def ellipse(self, parts):

        if len(parts) != 4:

            return (
                "ELLIPSE: "
                "ELLIPSE center rx ry"
            )

        self.save_history()

        center = self.parse_point(
            parts[1]
        )

        rx = float(
            parts[2]
        )

        ry = float(
            parts[3]
        )

        self.canvas.entities.append({

            "type": "ELLIPSE",

            "center": center,

            "rx": rx,

            "ry": ry,
        })

        self.canvas.update()

        return "ELLIPSE رسم شد"

    # =====================================================
    # MODIFY HELPERS
    # =====================================================

    def _point_xy(self, p):
        if isinstance(p, QPointF):
            return p.x(), p.y()
        return float(p[0]), float(p[1])

    def _translate_entity(
        self,
        entity,
        dx,
        dy
    ):
        typ = entity.get("type", "")

        dx = float(dx)
        dy = float(dy)

        if typ == "LINE":
            p1 = entity.get("p1", entity.get("start"))
            p2 = entity.get("p2", entity.get("end"))

            x1, y1 = self._point_xy(p1)
            x2, y2 = self._point_xy(p2)

            entity["p1"] = (x1 + dx, y1 + dy)
            entity["p2"] = (x2 + dx, y2 + dy)

            entity["start"] = entity["p1"]
            entity["end"] = entity["p2"]

        elif typ == "RECTANG":
            p1 = entity.get("p1", entity.get("start"))
            p2 = entity.get("p2", entity.get("end"))

            x1, y1 = self._point_xy(p1)
            x2, y2 = self._point_xy(p2)

            entity["p1"] = (x1 + dx, y1 + dy)
            entity["p2"] = (x2 + dx, y2 + dy)

            entity["start"] = entity["p1"]
            entity["end"] = entity["p2"]

        elif typ in ("CIRCLE", "ELLIPSE", "ARC"):
            center = entity.get("center")

            if center is None:
                return

            x, y = self._point_xy(center)

            entity["center"] = (
                x + dx,
                y + dy
            )

        elif typ == "POINT":
            p = entity.get("point")

            if p is None:
                return

            x, y = self._point_xy(p)

            entity["point"] = (
                x + dx,
                y + dy
            )

        elif typ in ("PLINE", "POLYGON"):
            points = entity.get("points") or []

            entity["points"] = [
                (
                    self._point_xy(p)[0] + dx,
                    self._point_xy(p)[1] + dy
                )
                for p in points
            ]

    # =====================================================
    # MOVE
    # =====================================================

    def move(self, parts):

        if len(parts) != 4:

            return (
                "MOVE: "
                "MOVE index dx dy"
            )

        index = int(parts[1])

        dx = float(parts[2])
        dy = float(parts[3])

        if not self._valid_index(index):

            return "شماره Entity نامعتبر است"

        self.save_history()

        self._translate_entity(
            self.canvas.entities[index],
            dx,
            dy
        )

        self.canvas.update()

        return "MOVE انجام شد"

    # =====================================================
    # COPY
    # =====================================================

    def copy(self, parts):

        if len(parts) != 4:

            return (
                "COPY: "
                "COPY index dx dy"
            )

        index = int(parts[1])

        dx = float(parts[2])
        dy = float(parts[3])

        if not self._valid_index(index):

            return "شماره Entity نامعتبر است"

        self.save_history()

        import copy

        new_entity = copy.deepcopy(
            self.canvas.entities[index]
        )

        self._translate_entity(
            new_entity,
            dx,
            dy
        )

        self.canvas.entities.append(
            new_entity
        )

        self.canvas.update()

        return "COPY انجام شد"

    # =====================================================
    # ROTATE
    # =====================================================

    def rotate(self, parts):

        if len(parts) != 5:

            return (
                "ROTATE: "
                "ROTATE index cx cy angle"
            )

        index = int(parts[1])

        cx = float(parts[2])
        cy = float(parts[3])

        angle = math.radians(
            float(parts[4])
        )

        if not self._valid_index(index):

            return "شماره Entity نامعتبر است"

        self.save_history()

        entity = self.canvas.entities[index]

        self._rotate_entity(
            entity,
            cx,
            cy,
            angle
        )

        self.canvas.update()

        return "ROTATE انجام شد"

    # =====================================================
    # ROTATE HELPER
    # =====================================================

    def _rotate_point(
        self,
        p,
        cx,
        cy,
        angle
    ):

        x = p[0] - cx
        y = p[1] - cy

        return (
            cx
            + x * math.cos(angle)
            - y * math.sin(angle),

            cy
            + x * math.sin(angle)
            + y * math.cos(angle)
        )

    def _rotate_entity(
        self,
        entity,
        cx,
        cy,
        angle
    ):

        typ = entity.get(
            "type",
            ""
        )

        if typ == "LINE":

            p1 = entity["p1"]
            p2 = entity["p2"]

            entity["p1"] = self._rotate_point(
                p1,
                cx,
                cy,
                angle
            )

            entity["p2"] = self._rotate_point(
                p2,
                cx,
                cy,
                angle
            )

            entity["start"] = entity["p1"]
            entity["end"] = entity["p2"]

        elif typ == "RECTANG":

            p1 = entity["p1"]
            p2 = entity["p2"]

            entity["p1"] = self._rotate_point(
                p1,
                cx,
                cy,
                angle
            )

            entity["p2"] = self._rotate_point(
                p2,
                cx,
                cy,
                angle
            )

            entity["start"] = entity["p1"]
            entity["end"] = entity["p2"]

        elif typ in (
            "CIRCLE",
            "ARC",
            "ELLIPSE"
        ):

            entity["center"] = self._rotate_point(
                entity["center"],
                cx,
                cy,
                angle
            )

            if typ == "ARC":

                entity["start"] += math.degrees(angle)
                entity["end"] += math.degrees(angle)

        elif typ == "POINT":

            entity["point"] = self._rotate_point(
                entity["point"],
                cx,
                cy,
                angle
            )

        elif typ in (
            "PLINE",
            "POLYGON"
        ):

            entity["points"] = [

                self._rotate_point(
                    p,
                    cx,
                    cy,
                    angle
                )

                for p in entity["points"]
            ]

    # =====================================================
    # SCALE
    # =====================================================

    def scale(self, parts):

        if len(parts) != 5:

            return (
                "SCALE: "
                "SCALE index cx cy factor"
            )

        index = int(parts[1])

        cx = float(parts[2])
        cy = float(parts[3])

        factor = float(parts[4])

        if not self._valid_index(index):

            return "شماره Entity نامعتبر است"

        if factor <= 0:

            return "ضریب Scale باید مثبت باشد"

        self.save_history()

        self._scale_entity(
            self.canvas.entities[index],
            cx,
            cy,
            factor
        )

        self.canvas.update()

        return "SCALE انجام شد"

    # =====================================================
    # SCALE HELPER
    # =====================================================

    def _scale_point(
        self,
        p,
        cx,
        cy,
        factor
    ):

        return (
            cx + (p[0] - cx) * factor,
            cy + (p[1] - cy) * factor
        )

    def _scale_entity(
        self,
        entity,
        cx,
        cy,
        factor
    ):

        typ = entity.get(
            "type",
            ""
        )

        if typ == "LINE":

            entity["p1"] = self._scale_point(
                entity["p1"],
                cx,
                cy,
                factor
            )

            entity["p2"] = self._scale_point(
                entity["p2"],
                cx,
                cy,
                factor
            )

            entity["start"] = entity["p1"]
            entity["end"] = entity["p2"]

        elif typ == "RECTANG":

            entity["p1"] = self._scale_point(
                entity["p1"],
                cx,
                cy,
                factor
            )

            entity["p2"] = self._scale_point(
                entity["p2"],
                cx,
                cy,
                factor
            )

            entity["start"] = entity["p1"]
            entity["end"] = entity["p2"]

        elif typ in (
            "CIRCLE",
            "ARC"
        ):

            entity["center"] = self._scale_point(
                entity["center"],
                cx,
                cy,
                factor
            )

            entity["radius"] *= factor

        elif typ == "ELLIPSE":

            entity["center"] = self._scale_point(
                entity["center"],
                cx,
                cy,
                factor
            )

            entity["rx"] *= factor
            entity["ry"] *= factor

        elif typ == "POINT":

            entity["point"] = self._scale_point(
                entity["point"],
                cx,
                cy,
                factor
            )

        elif typ in (
            "PLINE",
            "POLYGON"
        ):

            entity["points"] = [

                self._scale_point(
                    p,
                    cx,
                    cy,
                    factor
                )

                for p in entity["points"]
            ]

    # =====================================================
    # MIRROR
    # =====================================================

    def mirror(self, parts):

        if len(parts) != 6:

            return (
                "MIRROR: "
                "MIRROR index x1 y1 x2 y2"
            )

        index = int(parts[1])

        x1 = float(parts[2])
        y1 = float(parts[3])

        x2 = float(parts[4])
        y2 = float(parts[5])

        if not self._valid_index(index):

            return "شماره Entity نامعتبر است"

        self.save_history()

        self._mirror_entity(
            self.canvas.entities[index],
            x1,
            y1,
            x2,
            y2
        )

        self.canvas.update()

        return "MIRROR انجام شد"

    # =====================================================
    # MIRROR HELPER
    # =====================================================

    def _mirror_point(
        self,
        p,
        x1,
        y1,
        x2,
        y2
    ):

        dx = x2 - x1
        dy = y2 - y1

        length2 = (
            dx * dx +
            dy * dy
        )

        if length2 == 0:

            return p

        t = (
            (p[0] - x1) * dx
            + (p[1] - y1) * dy
        ) / length2

        proj_x = x1 + t * dx
        proj_y = y1 + t * dy

        return (
            2 * proj_x - p[0],
            2 * proj_y - p[1]
        )

    def _mirror_entity(
        self,
        entity,
        x1,
        y1,
        x2,
        y2
    ):

        typ = entity.get(
            "type",
            ""
        )

        if typ == "LINE":

            entity["p1"] = self._mirror_point(
                entity["p1"],
                x1,
                y1,
                x2,
                y2
            )

            entity["p2"] = self._mirror_point(
                entity["p2"],
                x1,
                y1,
                x2,
                y2
            )

            entity["start"] = entity["p1"]
            entity["end"] = entity["p2"]

        elif typ == "RECTANG":

            entity["p1"] = self._mirror_point(
                entity["p1"],
                x1,
                y1,
                x2,
                y2
            )

            entity["p2"] = self._mirror_point(
                entity["p2"],
                x1,
                y1,
                x2,
                y2
            )

            entity["start"] = entity["p1"]
            entity["end"] = entity["p2"]

        elif typ in (
            "CIRCLE",
            "ARC",
            "ELLIPSE"
        ):

            entity["center"] = self._mirror_point(
                entity["center"],
                x1,
                y1,
                x2,
                y2
            )

        elif typ == "POINT":

            entity["point"] = self._mirror_point(
                entity["point"],
                x1,
                y1,
                x2,
                y2
            )

        elif typ in (
            "PLINE",
            "POLYGON"
        ):

            entity["points"] = [

                self._mirror_point(
                    p,
                    x1,
                    y1,
                    x2,
                    y2
                )

                for p in entity["points"]
            ]

    # =====================================================
    # OFFSET
    # =====================================================

    def offset(self, parts):

        if len(parts) != 3:

            return (
                "OFFSET: "
                "OFFSET index distance"
            )

        index = int(parts[1])

        distance = float(
            parts[2]
        )

        if not self._valid_index(index):

            return "شماره Entity نامعتبر است"

        entity = self.canvas.entities[index]

        import copy

        new_entity = copy.deepcopy(
            entity
        )

        typ = entity.get(
            "type",
            ""
        )

        # LINE
        if typ == "LINE":

            p1 = entity["p1"]
            p2 = entity["p2"]

            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            length = math.hypot(
                dx,
                dy
            )

            if length == 0:

                return "خط طول صفر دارد"

            nx = -dy / length
            ny = dx / length

            dx = nx * distance
            dy = ny * distance

            new_entity["p1"] = (
                p1[0] + dx,
                p1[1] + dy
            )

            new_entity["p2"] = (
                p2[0] + dx,
                p2[1] + dy
            )

            new_entity["start"] = new_entity["p1"]
            new_entity["end"] = new_entity["p2"]

        # CIRCLE
        elif typ == "CIRCLE":

            new_radius = (
                entity["radius"]
                + distance
            )

            if new_radius <= 0:

                return "شعاع نامعتبر است"

            new_entity["radius"] = new_radius

        else:

            return (
                "OFFSET فعلاً برای LINE و CIRCLE فعال است"
            )

        self.save_history()

        self.canvas.entities.append(
            new_entity
        )

        self.canvas.update()

        return "OFFSET انجام شد"

    # =====================================================
    # TRIM
    # =====================================================

    def trim(self, parts):

        return (
            "TRIM: انتخاب تعاملی در مرحله بعد "
            "به Canvas اضافه می‌شود"
        )

    # =====================================================
    # EXTEND
    # =====================================================

    def extend(self, parts):

        return (
            "EXTEND: انتخاب تعاملی در مرحله بعد "
            "به Canvas اضافه می‌شود"
        )

    # =====================================================
    # ERASE
    # =====================================================

    def erase(self, parts):

        if len(parts) != 2:

            return (
                "ERASE: "
                "ERASE index"
            )

        index = int(parts[1])

        if not self._valid_index(index):

            return "شماره Entity نامعتبر است"

        self.save_history()

        self.canvas.entities.pop(
            index
        )

        self.canvas.update()

        return "ERASE انجام شد"

    # =====================================================
    # ZOOM
    # =====================================================

    def zoom(self, parts):

        if len(parts) != 2:

            return (
                "ZOOM ALL / EXTENTS / factor"
            )

        option = parts[1].upper()

        if option in (
            "ALL",
            "EXTENTS"
        ):

            self.canvas.zoom = 1.0
            self.canvas.pan_x = 0.0
            self.canvas.pan_y = 0.0

            self.canvas.update()

            return "ZOOM ALL انجام شد"

        factor = float(
            parts[1]
        )

        if factor <= 0:

            return "ضریب Zoom نامعتبر است"

        self.canvas.zoom *= factor

        self.canvas.zoom = max(
            0.05,
            min(
                self.canvas.zoom,
                100.0
            )
        )

        self.canvas.update()

        return "ZOOM انجام شد"

    # =====================================================
    # PAN
    # =====================================================

    def pan(self, parts):

        if len(parts) != 3:

            return (
                "PAN: "
                "PAN dx dy"
            )

        dx = float(parts[1])
        dy = float(parts[2])

        self.canvas.pan_x += dx
        self.canvas.pan_y += dy

        self.canvas.update()

        return "PAN انجام شد"

    # =====================================================
    # UNDO
    # =====================================================

    def undo(self):

        if not self.history:

            return "عملی برای Undo وجود ندارد"

        self.canvas.entities = (
            self.history.pop()
        )

        self.canvas.update()

        return "UNDO انجام شد"

    # =====================================================
    # ERASE ALL
    # =====================================================

    def erase_all(self):

        if self.canvas.entities:

            self.save_history()

        self.canvas.entities.clear()

        self.canvas.update()

        return "تمام اشیا پاک شدند"

    # =====================================================
    # VALID INDEX
    # =====================================================

    def _valid_index(self, index):

        return (
            0 <= index
            < len(self.canvas.entities)
        )

    # =====================================================
    # HELP
    # =====================================================

    def help(self):

        return (
            "DRAW: "
            "LINE PLINE RECTANG CIRCLE ARC "
            "POINT POLYGON ELLIPSE | "

            "MODIFY: "
            "MOVE COPY ROTATE SCALE MIRROR "
            "OFFSET TRIM EXTEND ERASE | "

            "VIEW: "
            "ZOOM PAN REDRAW | "

            "GENERAL: "
            "UNDO ERASEALL CLEAR HELP"
        )