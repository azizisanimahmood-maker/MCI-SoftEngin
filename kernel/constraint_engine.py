from __future__ import annotations


class ConstraintEngine:

    def __init__(self):

        self.constraints = []

    def add(self, constraint):

        self.constraints.append(constraint)

    def remove(self, constraint):

        if constraint in self.constraints:
            self.constraints.remove(constraint)

    def clear(self):

        self.constraints.clear()

    def solve(self):

        for constraint in self.constraints:
            constraint.solve()

    def update(self):

        self.solve()

    def count(self):

        return len(self.constraints)

    def serialize(self):

        return [
            c.serialize()
            for c in self.constraints
        ]

    def deserialize(self, data):

        self.constraints = data