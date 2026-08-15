from __future__ import annotations

from geometry.entity import Entity


class ModifyEngine:

    def move(
        self,
        entities: list[Entity],
        dx: float,
        dy: float
    ):

        for entity in entities:
            entity.move(dx, dy)

    def rotate(
        self,
        entities: list[Entity],
        angle: float,
        center
    ):

        for entity in entities:
            entity.rotate(
                angle,
                center
            )

    def scale(
        self,
        entities: list[Entity],
        sx: float,
        sy: float,
        center
    ):

        for entity in entities:
            entity.scale(
                sx,
                sy,
                center
            )

    def copy(
        self,
        entities: list[Entity],
        dx: float,
        dy: float
    ):

        result = []

        for entity in entities:

            clone = entity.clone()

            clone.move(dx, dy)

            result.append(clone)

        return result

    def mirror(
        self,
        entities,
        axis
    ):

        pass

    def offset(
        self,
        entity,
        distance
    ):

        pass

    def trim(
        self,
        entity,
        cutter
    ):

        pass

    def extend(
        self,
        entity,
        boundary
    ):

        pass

    def chamfer(
        self,
        entity1,
        entity2,
        distance
    ):

        pass

    def fillet(
        self,
        entity1,
        entity2,
        radius
    ):

        pass
