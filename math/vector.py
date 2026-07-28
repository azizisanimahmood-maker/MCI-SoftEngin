from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(slots=True)
class Vector2:
    x: float = 0.0
    y: float = 0.0

    def copy(self) -> "Vector2":
        return Vector2(self.x, self.y)

    def to_tuple(self):
        return (self.x, self.y)

    @property
    def length(self) -> float:
        return math.hypot(self.x, self.y)

    @property
    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y

    def normalized(self) -> "Vector2":
        l = self.length
        if l == 0:
            return Vector2()
        return Vector2(self.x / l, self.y / l)

    def normalize(self):
        l = self.length
        if l == 0:
            return
        self.x /= l
        self.y /= l

    def dot(self, other: "Vector2") -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other: "Vector2") -> float:
        return self.x * other.y - self.y * other.x

    def distance_to(self, other: "Vector2") -> float:
        return (self - other).length

    def angle_to(self, other: "Vector2") -> float:
        d = self.dot(other)
        l = self.length * other.length
        if l == 0:
            return 0.0
        return math.acos(max(-1.0, min(1.0, d / l)))

    def rotate(self, angle: float) -> "Vector2":
        c = math.cos(angle)
        s = math.sin(angle)
        return Vector2(
            self.x * c - self.y * s,
            self.x * s + self.y * c,
        )

    def perpendicular(self) -> "Vector2":
        return Vector2(-self.y, self.x)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, value: float):
        return Vector2(self.x * value, self.y * value)

    def __truediv__(self, value: float):
        return Vector2(self.x / value, self.y / value)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __repr__(self):
        return f"Vector2({self.x:.6f}, {self.y:.6f})"