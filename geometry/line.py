from __future__ import annotations

from geometry.entity import Entity
from math.vector import Vector2
from math.transform import Transform
from math.geometry_math import distance


class Line(Entity):

    def __init__(
        self,
        start: Vector2,
        end: Vector2
    ):

        super().__init__()

        self.start = start

        self.end = end

    @property
    def length(self):

        return distance(self.start, self.end)

    def clone(self):

        l = Line(
            self.start.copy(),
            self.end.copy()
        )

        l.layer = self.layer
        l.color = self.color
        l.lineweight = self.lineweight
        l.linetype = self.linetype
        l.visible = self.visible
        l.locked = self.locked

        return l

    def move(self, dx, dy):

        self.start.x += dx
        self.start.y += dy

        self.end.x += dx
        self.end.y += dy

    def rotate(
        self,
        angle,
        center
    ):

        m = (
            Transform.translation(-center.x, -center.y)
            @ Transform.rotation(angle)
            @ Transform.translation(center.x, center.y)
        )

        self.start = Transform.apply(m, self.start)

        self.end = Transform.apply(m, self.end)

    def scale(
        self,
        sx,
        sy,
        center
    ):

        m = (
            Transform.translation(-center.x, -center.y)
            @ Transform.scale(sx, sy)
            @ Transform.translation(center.x, center.y)
        )

        self.start = Transform.apply(m, self.start)

        self.end = Transform.apply(m, self.end)

    def bounding_box(self):

        return (
            Vector2(
                min(self.start.x, self.end.x),
                min(self.start.y, self.end.y)
            ),
            Vector2(
                max(self.start.x, self.end.x),
                max(self.start.y, self.end.y)
            )
        )

    def snap_points(self):

        return [
            self.start,
            self.end,
            (self.start + self.end) * 0.5
        ]

    def serialize(self):

        return {
            "type": "LINE",
            "start": (
                self.start.x,
                self.start.y
            ),
            "end": (
                self.end.x,
                self.end.y
            ),
            "layer": self.layer,
            "color": self.color
        }

    def deserialize(self, data):

        self.start = Vector2(*data["start"])

        self.end = Vector2(*data["end"])

        self.layer = data["layer"]

        self.color = tuple(data["color"])

    def __repr__(self):

        return (
            f"Line({self.start},{self.end})"
        )