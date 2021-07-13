from typing import Union

from chess.model.pieces import Piece


class Block:

    def __init__(self, x: int, y: int, piece: Union[None, Piece] = None) -> None:
        self.x: int = x
        self.y: int = y
        self.piece = piece

    def __repr__(self) -> str:
        return f"Block(x={self.x}, y={self.y}, piece={self.piece})"

