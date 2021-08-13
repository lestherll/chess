"""
All the custom typehints needed for the package
"""
from enum import Enum
from typing import Set, Tuple


Colour = Enum("Colour", ["BLACK", "WHITE"])
Coord2D = Tuple[int, int]
Coord2DSet = Set[Coord2D]

