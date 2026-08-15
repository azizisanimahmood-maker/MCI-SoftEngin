from __future__ import annotations


class PreviewRenderer:

    def __init__(self):

        self.enabled = False

        self.preview_entity = None

        self.color = (255, 255, 0)

    def set_preview(self, entity):

        self.preview_entity = entity

        self.enabled = True

    def clear(self):

        self.preview_entity = None

        self.enabled = False

    def draw(self, canvas):

        if not self.enabled:
            return

        if self.preview_entity is None:
            return

        canvas.draw_preview(
            self.preview_entity,
            self.color
        )
