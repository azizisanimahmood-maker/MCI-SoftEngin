from __future__ import annotations

from geometry.entity import Entity
from cad_math.vector import Vector2
from cad_math.transform import Transform


class Point(Entity):
    def __init__(self, x: float = 0.0, y: float = 0.0):
        super().__init__()
        self.position = Vector2(x, y)

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, value):
        self.position.x = value

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, value):
        self.position.y = value

    def move(self, dx: float, dy: float):
        self.position.x += dx
        self.position.y += dy

    def transform(self, matrix):
        self.position = Transform.apply_to_point(self.position, matrix)

    def clone(self):
        return Point(self.x, self.y)

    def bounding_box(self):
        return (self.x, self.y, self.x, self.y)

    def to_dict(self):
        return {
            "type": "Point",
            "x": self.x,
            "y": self.y,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["x"], data["y"])

    def __repr__(self):
        return f"Point({self.x}, {self.y})"