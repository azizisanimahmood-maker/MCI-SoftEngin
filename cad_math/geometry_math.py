from __future__ import annotations

import math

from cad_math.vector import Vector2
from cad_math.tolerance import Tolerance


def distance(a: Vector2, b: Vector2) -> float:
    """Return the Euclidean distance between two 2D vectors."""
    dx = b.x - a.x
    dy = b.y - a.y
    return math.hypot(dx, dy)


def distance_squared(a: Vector2, b: Vector2) -> float:
    """Return squared Euclidean distance."""
    dx = b.x - a.x
    dy = b.y - a.y
    return dx * dx + dy * dy


def midpoint(a: Vector2, b: Vector2) -> Vector2:
    """Return the midpoint between two vectors."""
    return Vector2(
        (a.x + b.x) / 2.0,
        (a.y + b.y) / 2.0,
    )


def is_close(
    a: float,
    b: float,
    tolerance: float | None = None,
) -> bool:
    """Compare two values using the CAD tolerance."""
    if tolerance is None:
        tolerance = Tolerance.EPSILON

    return abs(a - b) <= tolerance


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """Clamp a value to a specified range."""
    return max(minimum, min(value, maximum))


def dot(a: Vector2, b: Vector2) -> float:
    """Return the 2D dot product."""
    return a.x * b.x + a.y * b.y


def cross(a: Vector2, b: Vector2) -> float:
    """Return the scalar 2D cross product."""
    return a.x * b.y - a.y * b.x


def length(v: Vector2) -> float:
    """Return the vector length."""
    return math.hypot(v.x, v.y)


def normalize(v: Vector2) -> Vector2:
    """Return a normalized copy of the vector."""
    magnitude = length(v)

    if magnitude <= Tolerance.EPSILON:
        return Vector2()

    return Vector2(
        v.x / magnitude,
        v.y / magnitude,
    )


class GeometryMath:
    """Common geometric helper functions."""

    distance = staticmethod(distance)
    distance_squared = staticmethod(distance_squared)
    midpoint = staticmethod(midpoint)
    is_close = staticmethod(is_close)
    clamp = staticmethod(clamp)
    dot = staticmethod(dot)
    cross = staticmethod(cross)
    length = staticmethod(length)
    normalize = staticmethod(normalize)
