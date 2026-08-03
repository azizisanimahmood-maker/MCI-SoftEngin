from __future__ import annotations


class SelectionRenderer:

    def __init__(self):

        self.color = (0, 180, 255)

        self.grip_size = 6

    def draw(self, canvas, entity):

        if not entity.selected:
            return

        bbox = entity.bounding_box()

        canvas.draw_rectangle(
            bbox[0],
            bbox[1],
            self.color
        )

        for point in entity.snap_points():

            self.draw_grip(
                canvas,
                point
            )

    def draw_grip(
        self,
        canvas,
        point
    ):

        canvas.draw_square(
            point,
            self.grip_size,
            self.color
        )