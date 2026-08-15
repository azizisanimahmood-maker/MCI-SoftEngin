from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import uuid4


class Entity(ABC):

    def __init__(self):

        self.id = str(uuid4())

        self.layer = "0"

        self.color = (255, 255, 255)

        self.lineweight = 1.0

        self.linetype = "Continuous"

        self.visible = True

        self.locked = False

        self.selected = False

    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def move(self, dx: float, dy: float):
        pass

    @abstractmethod
    def rotate(self,
               angle: float,
               center):
        pass

    @abstractmethod
    def scale(self,
              sx: float,
              sy: float,
              center):
        pass

    @abstractmethod
    def bounding_box(self):
        pass

    @abstractmethod
    def snap_points(self):
        pass

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self, data):
        pass
