from dataclasses import dataclass
from typing import Union, List, Any, Optional, Iterable, Tuple, Literal

from chess.custom_typehints import Coord2D, Coord2DSet, Colour
from chess.model.pieces import Piece, King


@dataclass
class Block:
    """
    A block inside a chess board
    """
    x: int
    y: int
    piece: Optional[Piece] = None

    def colour(self) -> Optional[Colour]:
        return None if not self.piece else self.piece.colour

    def __str__(self) -> str:
        return f"{self.piece}"


class Board:

    def __init__(self, _length: int = 8) -> None:
        """
        A standard chess board that consists of 8x8 blocks by default
        :param _length: (8 by default) depicts the dimension of the board
        in a _length by _length manner
        """
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

    # def __str__(self) -> str:
    #     board: List = [None for i in range(9)]
    #     for i, row in enumerate(self.blocks):
    #         # board[i] = " ".join([str(p) for p in row])
    #         board[i+1] = " ".join(map(lambda p: f"{str(p):4}" if isinstance(p, int) or p.piece is not None else " .  ", [i] + row))
    #
    #     board[0] = "   " + " ".join([f"{i:>4}" for i in range(8)])
    #
    #     return "\n".join(board)

    # for file rank system later
    def __str__(self) -> str:
        board: List = [None for i in range(9)]
        file = "abcdefgh"
        for i, row in enumerate(self.blocks):
            # board[i] = " ".join([str(p) for p in row])
            board[i+1] = "".join(map(lambda p: f"{str(p):3}" if isinstance(p, int) or p.piece is not None else ".. ", [8-i] + row))

        board[0] = " " + "".join([f"{str(i):>3}" for i in file])

        return "\n".join(board)

    def put_piece(self, to_coord: Coord2D, piece: Piece) -> None:
        """
        Places a piece to the given 2D coordinate (x, y)
        :param to_coord: (x, y) coordinate of where to put the given piece
        :param piece: piece to be put on the board on to_coord
        :return: None
        """
        self.blocks[to_coord[1]][to_coord[0]].piece = piece

    def get_block_from_tuple(self, from_coord: Coord2D) -> Block:
        return self.blocks[from_coord[1]][from_coord[0]]

    def move_piece(self, from_coord: Coord2D, to_coord: Coord2D) -> None:
        """
        Move a piece from_coord to to_coord on the board. Both 2D coordinates are ordered x,y
        :param from_coord: origin of the piece to be moved
        :param to_coord: destination of the piece to be moved
        :return: None
        """
        piece: Optional[Piece] = self.blocks[from_coord[1]][from_coord[0]].piece
        self.blocks[from_coord[1]][from_coord[0]].piece = None
        self.blocks[to_coord[1]][to_coord[0]].piece = piece

    def remove_piece_at(self, from_coord: Coord2D) -> None:
        """
        Removes a piece at given coordinate
        :param from_coord: origin of the piece to be removed
        :return: None
        """
        self.blocks[from_coord[1]][from_coord[0]].piece = None

    def clear(self) -> None:
        """
        Clears the board blocks of pieces, sets it to None
        :return: None
        """
        for row in self.blocks:
            for block in row:
                block.piece = None

    def get_king_location(self, colour: Colour) -> Coord2D:
        for row in self.blocks:
            for block in row:
                # if block.piece is not None:
                if isinstance(block.piece, King) and block.colour() is colour:
                    return block.x, block.y

    def get_pieces_by_colour(self, colour: Colour, exclude_type: Iterable = None) -> Coord2DSet:
        """
        Get all pieces that are on the board by colour
        :param colour: the colour of pieces needed
        :param exclude_type: excluded type pieces
        :return: set of 2D tuples that contain all the pieces wanted by colour
        """
        # Needed to exclude king when generating
        # moves for the king to avoid recursion error
        if exclude_type is None:
            exclude_type = []

        coords: Coord2DSet = set()
        for j, row in enumerate(self.blocks):
            for i, block in enumerate(row):
                if block.colour() == colour and type(block.piece) not in exclude_type:
                    coords.add((i, j))
        return coords

    def reverse_pieces(self) -> None:
        """
        Reverses the board
        :return: None
        """
        length = len(self.blocks)
        for j in range(length//2):
            for b0, b1 in zip(self.blocks[j], self.blocks[length-j-1]):
                b0.piece, b1.piece = b1.piece, b0.piece
        # print(self.blocks)


def letter_to_coord(letter: str) -> Coord2D:
    letters = {letter: i for i, letter in enumerate("abcdefgh")}
    return letters[letter[0]], 7 - int(letter[1]) + 1
