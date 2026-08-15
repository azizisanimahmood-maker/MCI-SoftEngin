from __future__ import annotations

from geometry.point import Point
from geometry.line import Line
from geometry.circle import Circle
from geometry.arc import Arc
from geometry.ellipse import Ellipse
from geometry.polyline import Polyline
from geometry.spline import Spline
from geometry.polygon import Polygon


class EntityRenderer:

    def draw(
        self,
        canvas,
        entity
    ):

        if isinstance(entity, Point):
            self.draw_point(canvas, entity)

        elif isinstance(entity, Line):
            self.draw_line(canvas, entity)

        elif isinstance(entity, Circle):
            self.draw_circle(canvas, entity)

        elif isinstance(entity, Arc):
            self.draw_arc(canvas, entity)

        elif isinstance(entity, Ellipse):
            self.draw_ellipse(canvas, entity)

        elif isinstance(entity, Polyline):
            self.draw_polyline(canvas, entity)

        elif isinstance(entity, Spline):
            self.draw_spline(canvas, entity)

        elif isinstance(entity, Polygon):
            self.draw_polygon(canvas, entity)

    def draw_point(self, canvas, point):

        canvas.draw_point(
            point.x,
            point.y,
            point.color
        )

    def draw_line(self, canvas, line):

        canvas.draw_line(
            line.start,
            line.end,
            line.color
        )

    def draw_circle(self, canvas, circle):

        canvas.draw_circle(
            circle.center,
            circle.radius,
            circle.color
        )

    def draw_arc(self, canvas, arc):

        canvas.draw_arc(
            arc.center,
            arc.radius,
            arc.start_angle,
            arc.end_angle,
            arc.color
        )

    def draw_ellipse(self, canvas, ellipse):

        canvas.draw_ellipse(
            ellipse.center,
            ellipse.rx,
            ellipse.ry,
            ellipse.rotation,
            ellipse.color
        )

    def draw_polyline(self, canvas, polyline):

        canvas.draw_polyline(
            polyline.vertices,
            polyline.color,
            polyline.closed
        )

    def draw_spline(self, canvas, spline):

        canvas.draw_spline(
            spline.control_points,
            spline.color
        )

    def draw_polygon(self, canvas, polygon):

        canvas.draw_polygon(
            polygon.vertices,
            polygon.color
        )
