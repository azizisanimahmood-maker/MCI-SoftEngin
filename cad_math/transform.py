from __future__ import annotations

import math

from cad_math.matrix import Matrix3
from cad_math.vector import Vector2


class Transform:

    def __init__(self):
        self.matrix = Matrix3.identity()

    def translate(self, x: float, y: float):
        self.matrix = self.matrix * Matrix3.translation(x, y)

    def rotate(self, angle: float):
        c = math.cos(angle)
        s = math.sin(angle)
        self.matrix = self.matrix * Matrix3([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]
        ])

    def scale(self, sx: float, sy: float):
        self.matrix = self.matrix * Matrix3.scale(sx, sy)

    def apply(self, point: Vector2) -> Vector2:
        return self.matrix * point
