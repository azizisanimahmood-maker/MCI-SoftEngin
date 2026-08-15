from __future__ import annotations

from copy import deepcopy


class History:

    def __init__(self):

        self.undo_stack = []

        self.redo_stack = []

    def push(self, document):

        self.undo_stack.append(
            deepcopy(document)
        )

        self.redo_stack.clear()

    def undo(self, document):

        if not self.undo_stack:

            return document

        self.redo_stack.append(
            deepcopy(document)
        )

        return self.undo_stack.pop()

    def redo(self, document):

        if not self.redo_stack:

            return document

        self.undo_stack.append(
            deepcopy(document)
        )

        return self.redo_stack.pop()

    def clear(self):

        self.undo_stack.clear()

        self.redo_stack.clear()

    def can_undo(self):

        return len(self.undo_stack) > 0

    def can_redo(self):

        return len(self.redo_stack) > 0
