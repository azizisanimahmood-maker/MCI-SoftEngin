from __future__ import annotations


class GridRenderer:

    def __init__(self):

        self.spacing = 20

        self.color = (60, 60, 60)

        self.axis_color = (120, 120, 120)

        self.visible = True

    def draw(self, canvas):

        if not self.visible:
            return

        width = canvas.width()

        height = canvas.height()

        x = 0

        while x < width:

            canvas.draw_line_xy(
                x,
                0,
                x,
                height,
                self.color
            )

            x += self.spacing

        y = 0

        while y < height:

            canvas.draw_line_xy(
                0,
                y,
                width,
                y,
                self.color
            )

            y += self.spacing

        canvas.draw_line_xy(
            width // 2,
            0,
            width // 2,
            height,
            self.axis_color
        )

        canvas.draw_line_xy(
            0,
            height // 2,
            width,
            height // 2,
            self.axis_color
        )

    def zoom(self, factor):

        self.spacing *= factor

        if self.spacing < 5:
            self.spacing = 5

        if self.spacing > 200:
            self.spacing = 200