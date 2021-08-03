from typing import Tuple, Set

from chess.custom_typehints import Coord2DSet
from chess.model.board import Board, Block
from chess.model.move_validator import MoveValidator, generate_move
from chess.model.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Game:

    def __init__(self, board: Board = None) -> None:
        if not board:
            self.board: Board = Board()
        self._setup()
        self.move_validator: MoveValidator = MoveValidator()

    def _setup(self) -> None:
        for i in range(8):
            self.board[1][i].piece = Pawn("BLACK")
            self.board[6][i].piece = Pawn("WHITE")

        for i, piece in enumerate([Rook, Knight, Bishop]):
            self.board[0][i].piece = piece("BLACK")
            self.board[0][7 - i].piece = piece("BLACK")
            self.board[7][i].piece = piece("WHITE")
            self.board[7][7 - i].piece = piece("WHITE")

        self.board[0][3].piece = Queen("BLACK")
        self.board[7][3].piece = Queen("WHITE")

        self.board[0][4].piece = King("BLACK")
        self.board[7][4].piece = King("WHITE")

    def move(self, from_coord: Tuple[int, int], to_coord: Tuple[int, int]) -> None:
        from_block: Block = self.board[from_coord[1]][from_coord[0]]
        to_block: Block = self.board[to_coord[1]][to_coord[0]]

        move_set: Coord2DSet = generate_move(board=self.board, from_coord=from_coord)

        if to_coord in move_set:
            self.board.move_piece(from_coord, to_coord)
