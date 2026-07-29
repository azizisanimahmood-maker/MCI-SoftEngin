from __future__ import annotations

import math

from math.vector import Vector2
from math.tolerance import Tolerance


def distance(p1: Vector2, p2: Vector2) -> float:
    return (p2 - p1).length


def midpoint(p1: Vector2, p2: Vector2) -> Vector2:
    return Vector2(
        (p1.x + p2.x) * 0.5,
        (p1.y + p2.y) * 0.5
    )


def lerp(p1: Vector2, p2: Vector2, t: float) -> Vector2:
    return p1 + (p2 - p1) * t


def angle(p1: Vector2, p2: Vector2) -> float:
    return math.atan2(
        p2.y - p1.y,
        p2.x - p1.x
    )


def polar(origin: Vector2,
          radius: float,
          angle: float) -> Vector2:

    return Vector2(
        origin.x + radius * math.cos(angle),
        origin.y + radius * math.sin(angle)
    )


def collinear(a: Vector2,
              b: Vector2,
              c: Vector2) -> bool:

    ab = b - a
    ac = c - a

    return Tolerance.zero(ab.cross(ac))


def between(a: Vector2,
            b: Vector2,
            c: Vector2) -> bool:

    return (
        min(a.x, b.x) - Tolerance.EPSILON <= c.x <= max(a.x, b.x) + Tolerance.EPSILON
        and
        min(a.y, b.y) - Tolerance.EPSILON <= c.y <= max(a.y, b.y) + Tolerance.EPSILON
    )