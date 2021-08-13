from enum import Enum
from typing import Set, Tuple


class Colour(Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"


Coord2D = Tuple[int, int]
Coord2DSet = Set[Coord2D]

