"""
All the custom typehints needed for the package
"""
from enum import Enum
from typing import Set, Tuple

Colour = Enum("Colour", ["BLACK", "WHITE"])
GameStatus = Enum("GameStatus",
                  ["NORMAL", "DRAW", "WHITE_WIN", "BLACK_WIN", "WHITE_CHECKS_BLACK", "BLACK_CHECKS_WHITE"])
Coord2D = Tuple[int, int]
Coord2DSet = Set[Coord2D]
