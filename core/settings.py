from __future__ import annotations

class Settings:
    def __init__(self):
        self.theme = "dark"
        self.units = "mm"
        self.grid_enabled = True
        self.snap_enabled = True
        self.snap_tolerance = 10.0
        self.precision = 3

    def get(self, name, default=None):
        return getattr(self, name, default)

    def set(self, name, value):
        setattr(self, name, value)
