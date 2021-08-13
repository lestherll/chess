from dataclasses import dataclass

from chess.custom_typehints import Colour


@dataclass
class Player:
    name: str
    colour: Colour
