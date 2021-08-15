from typing import Tuple, Set, List

from chess.custom_typehints import Coord2DSet, Colour, GameStatus
from chess.model.board import Board, Block
from chess.model.move_generator import generate_move
from chess.model.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chess.model.player import Player


class GameState:

    def __init__(self, board: Board, player1: Player, player2: Player) -> None:
        self.board: Board = board
        self._is_white_turn: bool = True
        self.moves_made: List = []
        self.turn_number: int = 0
        self.status: GameStatus = GameStatus.NORMAL

        if player1.colour == Colour.BLACK:
            self.black_player, self.white_player = player1, player2
        else:
            self.black_player, self.white_player = player2, player1

    def is_check(self, colour: Colour) -> bool:
        ...

    def turn(self) -> bool:
        return Colour.WHITE if self._is_white_turn else Colour.BLACK

    def update(self) -> None:
        """Updates the status of the game whenever a move is made"""
        ...


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
