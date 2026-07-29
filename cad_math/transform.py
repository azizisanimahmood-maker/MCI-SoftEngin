from __future__ import annotations

import math

from math.matrix import Matrix3
from math.vector import Vector2


class Transform:

    @staticmethod
    def identity() -> Matrix3:
        return Matrix3.identity()

    @staticmethod
    def translation(dx: float, dy: float) -> Matrix3:
        return Matrix3(
            1.0, 0.0, dx,
            0.0, 1.0, dy,
            0.0, 0.0, 1.0
        )

    @staticmethod
    def scale(sx: float, sy: float) -> Matrix3:
        return Matrix3(
            sx, 0.0, 0.0,
            0.0, sy, 0.0,
            0.0, 0.0, 1.0
        )

    @staticmethod
    def rotation(angle: float) -> Matrix3:

        c = math.cos(angle)
        s = math.sin(angle)

        return Matrix3(
             c, -s, 0.0,
             s,  c, 0.0,
           0.0,0.0,1.0
        )

    @staticmethod
    def apply(matrix: Matrix3, point: Vector2) -> Vector2:

        x = matrix.m11 * point.x + matrix.m12 * point.y + matrix.m13
        y = matrix.m21 * point.x + matrix.m22 * point.y + matrix.m23

        return Vector2(x, y)