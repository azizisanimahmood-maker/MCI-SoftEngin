from __future__ import annotations

import math


class Tolerance:

    # Geometric tolerance
    EPSILON = 1e-9

    # Display tolerance
    DISPLAY = 1e-6

    # Angular tolerance (radian)
    ANGLE = 1e-8

    @staticmethod
    def equal(a: float, b: float) -> bool:
        return math.isclose(a, b, abs_tol=Tolerance.EPSILON)

    @staticmethod
    def less(a: float, b: float) -> bool:
        return a < b - Tolerance.EPSILON

    @staticmethod
    def greater(a: float, b: float) -> bool:
        return a > b + Tolerance.EPSILON

    @staticmethod
    def zero(value: float) -> bool:
        return abs(value) <= Tolerance.EPSILON

    @staticmethod
    def clamp(value: float) -> float:
        if Tolerance.zero(value):
            return 0.0
        return value

    @staticmethod
    def angle_equal(a: float, b: float) -> bool:
        return math.isclose(a, b, abs_tol=Tolerance.ANGLE)