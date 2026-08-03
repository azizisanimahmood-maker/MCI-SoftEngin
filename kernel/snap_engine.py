from __future__ import annotations

from math.vector import Vector2


class SnapEngine:

    def __init__(self):

        self.enabled = True

        self.snap_distance = 10.0

    def nearest(self,
                cursor: Vector2,
                entities):

        best_point = None

        best_distance = float("inf")

        for entity in entities:

            for point in entity.snap_points():

                d = cursor.distance_to(point)

                if d < best_distance:

                    best_distance = d

                    best_point = point

        if best_distance <= self.snap_distance:

            return best_point

        return None

    def endpoint(self, entity):

        pts = entity.snap_points()

        if len(pts) >= 2:

            return [
                pts[0],
                pts[-1]
            ]

        return pts

    def midpoint(self, entity):

        pts = entity.snap_points()

        if len(pts) >= 2:

            return [
                (pts[0] + pts[-1]) * 0.5
            ]

        return []

    def center(self, entity):

        if hasattr(entity, "center"):

            return entity.center

        return None

    def intersection(
            self,
            entity_a,
            entity_b):

        return None

    def clear(self):

        pass