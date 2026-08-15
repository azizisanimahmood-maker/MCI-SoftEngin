from __future__ import annotations

from geometry.entity import Entity
from cad_math.vector import Vector2
from cad_math.transform import Transform


class Circle(Entity):

    def __init__(
        self,
        center: Vector2,
        radius: float
    ):

        super().__init__()

        self.center = center

        self.radius = radius

    def clone(self):

        c = Circle(
            self.center.copy(),
            self.radius
        )

        c.layer = self.layer
        c.color = self.color
        c.lineweight = self.lineweight
        c.linetype = self.linetype
        c.visible = self.visible
        c.locked = self.locked

        return c

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

        self.center = Transform.apply(
            m,
            self.center
        )

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

        self.center = Transform.apply(
            m,
            self.center
        )

        self.radius *= (sx + sy) * 0.5

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
            self.center
        ]

    def serialize(self):

        return {

            "type": "CIRCLE",

            "center": (
                self.center.x,
                self.center.y
            ),

            "radius": self.radius,

            "layer": self.layer,

            "color": self.color
        }

    def deserialize(self, data):

        self.center = Vector2(
            *data["center"]
        )

        self.radius = data["radius"]

        self.layer = data["layer"]

        self.color = tuple(
            data["color"]
        )

    def __repr__(self):

        return (
            f"Circle(C={self.center},R={self.radius})"
        )
