from __future__ import annotations

from geometry.entity import Entity
from cad_math.vector import Vector2
from cad_math.transform import Transform


class Spline(Entity):

    def __init__(self):

        super().__init__()

        self.control_points: list[Vector2] = []

        self.degree = 3

        self.closed = False

    def add_point(self, point: Vector2):

        self.control_points.append(point)

    def clone(self):

        s = Spline()

        s.control_points = [
            p.copy()
            for p in self.control_points
        ]

        s.degree = self.degree

        s.closed = self.closed

        s.layer = self.layer
        s.color = self.color
        s.lineweight = self.lineweight
        s.linetype = self.linetype
        s.visible = self.visible
        s.locked = self.locked

        return s

    def move(self, dx, dy):

        for p in self.control_points:

            p.x += dx
            p.y += dy

    def rotate(self, angle, center):

        m = (
            Transform.translation(-center.x, -center.y)
            @ Transform.rotation(angle)
            @ Transform.translation(center.x, center.y)
        )

        self.control_points = [
            Transform.apply(m, p)
            for p in self.control_points
        ]

    def scale(self, sx, sy, center):

        m = (
            Transform.translation(-center.x, -center.y)
            @ Transform.scale(sx, sy)
            @ Transform.translation(center.x, center.y)
        )

        self.control_points = [
            Transform.apply(m, p)
            for p in self.control_points
        ]

    def bounding_box(self):

        xs = [p.x for p in self.control_points]
        ys = [p.y for p in self.control_points]

        return (
            Vector2(min(xs), min(ys)),
            Vector2(max(xs), max(ys))
        )

    def snap_points(self):

        return self.control_points

    def serialize(self):

        return {

            "type": "SPLINE",

            "degree": self.degree,

            "closed": self.closed,

            "points": [
                (p.x, p.y)
                for p in self.control_points
            ],

            "layer": self.layer,

            "color": self.color
        }

    def deserialize(self, data):

        self.degree = data["degree"]

        self.closed = data["closed"]

        self.control_points = [
            Vector2(x, y)
            for x, y in data["points"]
        ]

        self.layer = data["layer"]

        self.color = tuple(data["color"])

    def __repr__(self):

        return (
            f"Spline({len(self.control_points)} pts)"
        )
