from __future__ import annotations

import math

from geometry.entity import Entity
from cad_math.vector import Vector2
from cad_math.transform import Transform


class Arc(Entity):

    def __init__(
        self,
        center: Vector2,
        radius: float,
        start_angle: float,
        end_angle: float
    ):

        super().__init__()

        self.center = center

        self.radius = radius

        self.start_angle = start_angle

        self.end_angle = end_angle

    @property
    def sweep(self):

        s = self.end_angle - self.start_angle

        if s < 0:
            s += math.tau

        return s

    @property
    def length(self):

        return self.radius * self.sweep

    def clone(self):

        a = Arc(
            self.center.copy(),
            self.radius,
            self.start_angle,
            self.end_angle
        )

        a.layer = self.layer
        a.color = self.color
        a.lineweight = self.lineweight
        a.linetype = self.linetype
        a.visible = self.visible
        a.locked = self.locked

        return a

    def move(self, dx, dy):

        self.center.x += dx
        self.center.y += dy

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

        self.center = Transform.apply(m, self.center)

        self.start_angle += angle
        self.end_angle += angle

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

        self.center = Transform.apply(m, self.center)

        self.radius *= (sx + sy) * 0.5

    def start_point(self):

        return Vector2(
            self.center.x + self.radius * math.cos(self.start_angle),
            self.center.y + self.radius * math.sin(self.start_angle)
        )

    def end_point(self):

        return Vector2(
            self.center.x + self.radius * math.cos(self.end_angle),
            self.center.y + self.radius * math.sin(self.end_angle)
        )

    def bounding_box(self):

        r = self.radius

        return (
            Vector2(
                self.center.x - r,
                self.center.y - r
            ),
            Vector2(
                self.center.x + r,
                self.center.y + r
            )
        )

    def snap_points(self):

        return [
            self.center,
            self.start_point(),
            self.end_point()
        ]

    def serialize(self):

        return {

            "type": "ARC",

            "center": (
                self.center.x,
                self.center.y
            ),

            "radius": self.radius,

            "start": self.start_angle,

            "end": self.end_angle,

            "layer": self.layer,

            "color": self.color
        }

    def deserialize(self, data):

        self.center = Vector2(*data["center"])

        self.radius = data["radius"]

        self.start_angle = data["start"]

        self.end_angle = data["end"]

        self.layer = data["layer"]

        self.color = tuple(data["color"])

    def __repr__(self):

        return (
            f"Arc(C={self.center},R={self.radius})"
        )
