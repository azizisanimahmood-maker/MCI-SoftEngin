from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Matrix3:
    m11: float = 1.0
    m12: float = 0.0
    m13: float = 0.0

    m21: float = 0.0
    m22: float = 1.0
    m23: float = 0.0

    m31: float = 0.0
    m32: float = 0.0
    m33: float = 1.0

    @staticmethod
    def identity():
        return Matrix3()

    def copy(self):
        return Matrix3(
            self.m11, self.m12, self.m13,
            self.m21, self.m22, self.m23,
            self.m31, self.m32, self.m33,
        )

    def to_list(self):
        return [
            [self.m11, self.m12, self.m13],
            [self.m21, self.m22, self.m23],
            [self.m31, self.m32, self.m33],
        ]

    def __matmul__(self, other: "Matrix3") -> "Matrix3":

        a = self
        b = other

        return Matrix3(

            a.m11*b.m11 + a.m12*b.m21 + a.m13*b.m31,
            a.m11*b.m12 + a.m12*b.m22 + a.m13*b.m32,
            a.m11*b.m13 + a.m12*b.m23 + a.m13*b.m33,

            a.m21*b.m11 + a.m22*b.m21 + a.m23*b.m31,
            a.m21*b.m12 + a.m22*b.m22 + a.m23*b.m32,
            a.m21*b.m13 + a.m22*b.m23 + a.m23*b.m33,

            a.m31*b.m11 + a.m32*b.m21 + a.m33*b.m31,
            a.m31*b.m12 + a.m32*b.m22 + a.m33*b.m32,
            a.m31*b.m13 + a.m32*b.m23 + a.m33*b.m33,
        )

    def __repr__(self):
        return (
            "Matrix3(\n"
            f"  [{self.m11:.3f}, {self.m12:.3f}, {self.m13:.3f}],\n"
            f"  [{self.m21:.3f}, {self.m22:.3f}, {self.m23:.3f}],\n"
            f"  [{self.m31:.3f}, {self.m32:.3f}, {self.m33:.3f}]\n"
            ")"
        )