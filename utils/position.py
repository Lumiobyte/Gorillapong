from dataclasses import dataclass

@dataclass
class Position:
    x: int
    y: int

    def tuple(self):
        return (self.x, self.y)

    """
    x_min_limit: int = None
    x_max_limit: int = None
    y_min_limit: int = None
    y_max_limit: int = None
    """