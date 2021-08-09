from dataclasses import dataclass
from typing import Union, List, Any, Optional, Iterable, Tuple, Literal

from chess.custom_typehints import Coord2D, Coord2DSet, Colour
from chess.model.pieces import Piece, King


@dataclass
class Block:
    x: int
    y: int
    piece: Optional[Piece] = None

    def colour(self) -> Optional[Literal["BLACK", "WHITE"]]:
        return None if not self.piece else self.piece.colour

    # def __repr__(self) -> str:
    #     return f"Block(x={self.x}, y={self.y}, piece={self.piece})"

    def __str__(self) -> str:
        return f"{self.piece}"

    # def __eq__(self, other: Any) -> bool:
    #     if isinstance(other, Block):
    #         if other.x == self.x and other.y == self.y:
    #             return True
    #     return False


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

    def __repr__(self) -> str:
        return f"Board(blocks={self.blocks})"

    def __str__(self) -> str:
        board: List = [None for i in range(8)]
        for i, row in enumerate(self.blocks):
            board[i] = " ".join(map(str, row))

        return "\n".join(board)

    def put_piece(self, to_coord: Coord2D, piece: Piece) -> None:
        self.blocks[to_coord[1]][to_coord[0]].piece = piece

    def move_piece(self, from_coord: Coord2D, to_coord: Coord2D) -> None:
        piece: Optional[Piece] = self.blocks[from_coord[1]][from_coord[0]].piece
        self.blocks[from_coord[1]][from_coord[0]].piece = None
        self.blocks[to_coord[1]][to_coord[0]].piece = piece

    def remove_piece_at(self, from_coord: Coord2D) -> None:
        self.blocks[from_coord[1]][from_coord[0]].piece = None

    def clear(self) -> None:
        for row in self.blocks:
            for block in row:
                block.piece = None

    def get_pieces_by_colour(self, colour: Colour, exclude_type: Iterable = None) -> Coord2DSet:
        # Needed to exclude king when generating moves for the king
        # to avoid recursion error
        if exclude_type is None:
            exclude_type = []

        coords: Coord2DSet = set()
        for j, row in enumerate(self.blocks):
            for i, block in enumerate(row):
                if block.colour() == colour and type(block.piece) not in exclude_type:
                    coords.add((i, j))
        return coords

    def reverse_pieces(self) -> None:
        length = len(self.blocks)
        for j in range(length//2):
            for b0, b1 in zip(self.blocks[j], self.blocks[length-j-1]):
                b0.piece, b1.piece = b1.piece, b0.piece
        # print(self.blocks)

def letter_to_coord(letter) -> Coord2D:
    letters = {letter: i for letter, i in zip("HGFEDCBA", range(1, 9))}
    return letters[letter[0]], int(letter[1])
