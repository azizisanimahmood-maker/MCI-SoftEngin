from __future__ import annotations

from geometry.entity import Entity


class SelectionEngine:

    def __init__(self):

        self._selection: list[Entity] = []

    def clear(self):

        for entity in self._selection:
            entity.selected = False

        self._selection.clear()

    def add(self, entity: Entity):

        if entity not in self._selection:

            entity.selected = True

            self._selection.append(entity)

    def remove(self, entity: Entity):

        if entity in self._selection:

            entity.selected = False

            self._selection.remove(entity)

    def toggle(self, entity: Entity):

        if entity in self._selection:
            self.remove(entity)
        else:
            self.add(entity)

    def select_all(self, entities):

        self.clear()

        for entity in entities:
            self.add(entity)

    def current(self):

        return list(self._selection)

    def count(self):

        return len(self._selection)

    def first(self):

        if self._selection:
            return self._selection[0]

        return None

    def is_selected(self, entity: Entity):

        return entity in self._selection
