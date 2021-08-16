from unittest import TestCase

from chess.custom_typehints import Colour
from chess.model.board import Board
from chess.model.game import Game


class TestGame(TestCase):
    def test__setup(self):
        game: Game = Game()
        board: Board = game.board
        self.assertIsNone(board[4][4].piece)

    def test_move_pawn(self):
        game = Game()
        game.move((0, 6), (0, 5))

        self.assertIsNone(game.board[6][0].piece)
        self.assertIsNotNone(game.board[5][0].piece)
        self.assertIs(Colour.BLACK, game.turn())
        self.assertTupleEqual(((0, 6), (0, 5)), game.moves_made[0])
        self.assertEqual(2, game.turn_number)

