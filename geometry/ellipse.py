from __future__ import annotations

from geometry.entity import Entity
from cad_math.vector import Vector2
from cad_math.transform import Transform


class Ellipse(Entity):

    def __init__(
        self,
        center: Vector2,
        rx: float,
        ry: float
    ):

        super().__init__()

        self.center = center

        self.rx = rx

        self.ry = ry

        self.rotation = 0.0

    def clone(self):

        e = Ellipse(
            self.center.copy(),
            self.rx,
            self.ry
        )

        e.rotation = self.rotation

        e.layer = self.layer
        e.color = self.color
        e.lineweight = self.lineweight
        e.linetype = self.linetype
        e.visible = self.visible
        e.locked = self.locked

        return e

    def move(self, dx, dy):

        self.center.x += dx
        self.center.y += dy

    def rotate(self, angle, center):

        m = (
            Transform.translation(-center.x, -center.y)
            @ Transform.rotation(angle)
            @ Transform.translation(center.x, center.y)
        )

        self.center = Transform.apply(
            m,
            self.center
        )

        self.rotation += angle

    def scale(self, sx, sy, center):

        m = (
            Transform.translation(-center.x, -center.y)
            @ Transform.scale(sx, sy)
            @ Transform.translation(center.x, center.y)
        )

        self.center = Transform.apply(
            m,
            self.center
        )

        self.rx *= sx
        self.ry *= sy

    def bounding_box(self):

        return (
            Vector2(
                self.center.x - self.rx,
                self.center.y - self.ry
            ),
            Vector2(
                self.center.x + self.rx,
                self.center.y + self.ry
            )
        )

    def snap_points(self):

        return [
            self.center
        ]

    def serialize(self):

        return {

            "type": "ELLIPSE",

            "center": (
                self.center.x,
                self.center.y
            ),

            "rx": self.rx,

            "ry": self.ry,

            "rotation": self.rotation,

            "layer": self.layer,

            "color": self.color
        }

    def deserialize(self, data):

        self.center = Vector2(
            *data["center"]
        )

        self.rx = data["rx"]

        self.ry = data["ry"]

        self.rotation = data["rotation"]

        self.layer = data["layer"]

        self.color = tuple(
            data["color"]
        )

    def __repr__(self):

        return (
            f"Ellipse(C={self.center})"
        )
