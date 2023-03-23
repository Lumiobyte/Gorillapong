from dataclasses import dataclass
import math

@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar):
        return Position(self.x*scalar, self.y*scalar)
    def __truediv__(self, scalar):
        return Position(self.x/scalar, self.y/scalar)
    def __len__(self):
        return int(math.sqrt(self.x**2 + self.y**2))

    def tuple(self):
        return (self.x, self.y)

    """
    x_min_limit: int = None
    x_max_limit: int = None
    y_min_limit: int = None
    y_max_limit: int = None
    """