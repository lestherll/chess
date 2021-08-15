from typing import List

from chess.custom_typehints import Colour, GameStatus
from chess.model.board import Board
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