from __future__ import annotations


class Renderer:

    def __init__(self):

        self.background = (30, 30, 30)

        self.grid_visible = True

        self.antialias = True

    def begin_frame(self, canvas):

        canvas.clear(self.background)

    def end_frame(self, canvas):

        canvas.update()

    def render(self, canvas, entities):

        self.begin_frame(canvas)

        for entity in entities:
            self.draw_entity(canvas, entity)

        self.end_frame(canvas)

    def draw_entity(self, canvas, entity):

        pass