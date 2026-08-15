from __future__ import annotations

from cad_math.vector import Vector2


class IntersectionEngine:

    def line_line(
        self,
        line1,
        line2
    ):

        x1 = line1.start.x
        y1 = line1.start.y

        x2 = line1.end.x
        y2 = line1.end.y

        x3 = line2.start.x
        y3 = line2.start.y

        x4 = line2.end.x
        y4 = line2.end.y

        den = (
            (x1 - x2) * (y3 - y4)
            -
            (y1 - y2) * (x3 - x4)
        )

        if den == 0:

            return None

        px = (
            (x1 * y2 - y1 * x2) * (x3 - x4)
            -
            (x1 - x2) * (x3 * y4 - y3 * x4)
        ) / den

        py = (
            (x1 * y2 - y1 * x2) * (y3 - y4)
            -
            (y1 - y2) * (x3 * y4 - y3 * x4)
        ) / den

        return Vector2(px, py)

    def line_circle(
        self,
        line,
        circle
    ):

        return []

    def circle_circle(
        self,
        c1,
        c2
    ):

        return []

    def line_arc(
        self,
        line,
        arc
    ):

        return []

    def arc_arc(
        self,
        a1,
        a2
    ):

        return []

    def polyline_line(
        self,
        polyline,
        line
    ):

        return []

    def spline_line(
        self,
        spline,
        line
    ):

        return []
