from __future__ import annotations

from geometry.entity import Entity
from cad_math.vector import Vector2
from cad_math.transform import Transform


class Polygon(Entity):

    def __init__(self):

        super().__init__()

        self.vertices: list[Vector2] = []

    def add_vertex(self, point: Vector2):

        self.vertices.append(point)

    def clone(self):

        p = Polygon()

        p.vertices = [
            v.copy()
            for v in self.vertices
        ]

        p.layer = self.layer
        p.color = self.color
        p.lineweight = self.lineweight
        p.linetype = self.linetype
        p.visible = self.visible
        p.locked = self.locked

        return p

    def move(self, dx, dy):

        for v in self.vertices:

            v.x += dx
            v.y += dy

    def rotate(self, angle, center):

        m = (
            Transform.translation(-center.x, -center.y)
            @ Transform.rotation(angle)
            @ Transform.translation(center.x, center.y)
        )

        self.vertices = [
            Transform.apply(m, v)
            for v in self.vertices
        ]

    def scale(self, sx, sy, center):

        m = (
            Transform.translation(-center.x, -center.y)
            @ Transform.scale(sx, sy)
            @ Transform.translation(center.x, center.y)
        )

        self.vertices = [
            Transform.apply(m, v)
            for v in self.vertices
        ]

    def bounding_box(self):

        xs = [v.x for v in self.vertices]
        ys = [v.y for v in self.vertices]

        return (
            Vector2(min(xs), min(ys)),
            Vector2(max(xs), max(ys))
        )

    def snap_points(self):

        return self.vertices

    def serialize(self):

        return {

            "type": "POLYGON",

            "vertices": [
                (v.x, v.y)
                for v in self.vertices
            ],

            "layer": self.layer,

            "color": self.color
        }

    def deserialize(self, data):

        self.vertices = [
            Vector2(x, y)
            for x, y in data["vertices"]
        ]

        self.layer = data["layer"]

        self.color = tuple(data["color"])

    def __repr__(self):

        return (
            f"Polygon({len(self.vertices)} vertices)"
        )
