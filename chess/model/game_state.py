from typing import List

from chess.custom_typehints import Colour
from chess.model.board import Board
from chess.model.player import Player


class GameState:

    def __init__(self, board: Board, player1: Player, player2: Player) -> None:
        self.board: Board = board

        if player1.colour == Colour.BLACK:
            self.black_player, self.white_player = player1, player2
        else:
            self.black_player, self.white_player = player2, player1

    def is_check(self, colour: Colour) -> bool:
        ...

