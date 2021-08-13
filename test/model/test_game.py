from unittest import TestCase

from chess.model.board import Board
from chess.model.game import Game


class TestGame(TestCase):
    def test__setup(self):
        game: Game = Game()
        board: Board = game.board
        self.assertIsNone(board[4][4].piece)

    def test_move_pawn(self):
        game = Game()
        game.move((0, 1), (0, 2))

        self.assertIsNone(game.board[1][0].piece)
        self.assertIsNotNone(game.board[2][0].piece)

