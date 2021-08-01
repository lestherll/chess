from typing import Union, List, Any, Optional, Iterable, Tuple, Literal

from chess.custom_typehints import Coord2D
from chess.model.pieces import Piece


class Block:

    def __init__(self, x: int, y: int, piece: Optional[Piece] = None) -> None:
        self.x: int = x
        self.y: int = y
        self.piece: Optional[Piece] = piece

    def colour(self) -> Union[Literal["BLACK", "WHITE"], None]:
        return None if not self.piece else self.piece.colour

    def __repr__(self) -> str:
        return f"Block(x={self.x}, y={self.y}, piece={self.piece})"

    def __str__(self) -> str:
        return f"{self.piece}"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Block):
            if other.x == self.x and other.y == self.y:
                return True
        return False


class Board:

    def __init__(self, _length: int = 8) -> None:
        self.blocks: List[List[Block]] = [[Block(x=i, y=j) for i in range(_length)]
                                          for j in range(_length)]

    def __len__(self) -> int:
        return len(self.blocks)

    def __getitem__(self, pos: Union[int, Block]) -> Union[Block, List[Block], IndexError]:
        if isinstance(pos, Block):
            return self.blocks[pos.y][pos.x]
        return self.blocks[pos]

    def __str__(self) -> str:
        board: List = [None for i in range(8)]
        for i, row in enumerate(self.blocks):
            board[i] = " ".join(map(str, row))

        return "\n".join(board)

    def put_piece(self, to_coord: Coord2D, piece: Piece) -> None:
        self[to_coord[1]][to_coord[0]].piece = piece

    def move_piece(self, from_coord: Coord2D, to_coord: Coord2D) -> None:
        piece: Optional[Piece] = self[from_coord[1]][from_coord[0]].piece
        self[from_coord[1]][from_coord[0]].piece = None
        self[to_coord[1]][to_coord[0]].piece = piece

    def remove_piece_at(self, from_coord: Coord2D) -> None:
        self[from_coord[1]][from_coord[0]].piece = None

    def clear(self) -> None:
        for row in self.blocks:
            for block in row:
                block.piece = None


def letter_to_coord(letter):
    letters = {letter: i for letter, i in zip("ABCDEFGH", range(1, 9))}
    return letters[letter[0]], int(letter[1])
