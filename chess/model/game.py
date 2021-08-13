from typing import Tuple, Set

from chess.custom_typehints import Coord2DSet, Colour
from chess.model.board import Board, Block
from chess.model.move_generator import generate_move
from chess.model.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Game:

    def __init__(self, board: Board = None) -> None:
        if not board:
            self.board: Board = Board()
        self._setup()
        # self.move_validator: MoveValidator = MoveValidator()

    def _setup(self) -> None:
        for i in range(8):
            self.board.put_piece((i, 1), Pawn(Colour.BLACK))
            self.board.put_piece((i, 6), Pawn(Colour.WHITE))

        for i, piece in enumerate([Rook, Knight, Bishop]):
            self.board.put_piece((i, 0), piece(Colour.BLACK))
            self.board.put_piece((7-i, 0), piece(Colour.BLACK))
            self.board.put_piece((i, 7), piece(Colour.WHITE))
            self.board.put_piece((7-i, 7), piece(Colour.WHITE))

        self.board.put_piece((3, 0), Queen(Colour.BLACK))
        self.board.put_piece((3, 7), Queen(Colour.WHITE))

        self.board.put_piece((4, 0), King(Colour.BLACK))
        self.board.put_piece((4, 7), King(Colour.WHITE))

    def move(self, from_coord: Tuple[int, int], to_coord: Tuple[int, int]) -> None:
        move_set: Coord2DSet = generate_move(board=self.board, from_coord=from_coord)
        if to_coord in move_set:
            self.board.move_piece(from_coord, to_coord)
