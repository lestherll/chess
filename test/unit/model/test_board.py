from unittest import TestCase

from chess.model.game import Game
from chess.model.board import Board


class TestBoard(TestCase):

    def test_board_length(self):
        board: Board = Board()
        self.assertEqual(8, len(board))

        board = Board(_length=4)
        self.assertEqual(4, len(board))

    def test_clear(self):
        game: Game = Game()
        board: Board = game.board
        board.clear()
        for row in board:
            for block in row:
                self.assertIsNone(block.piece)
