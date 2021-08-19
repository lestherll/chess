from unittest import TestCase

from chess.custom_typehints import Coord2D, Colour
from chess.model.game import Game
from chess.model.board import Board


class TestBoard(TestCase):

    def test_board_length(self):
        board: Board = Board()
        self.assertEqual(8, len(board))

        board = Board(_length=4)
        self.assertEqual(4, len(board))

    def test_get_king_location(self):
        game: Game = Game()
        board: Board = game.board

        black_king_loc: Coord2D = board.get_king_location(Colour.BLACK)
        white_king_loc: Coord2D = board.get_king_location(Colour.WHITE)

        self.assertTupleEqual((4, 0), black_king_loc)
        self.assertTupleEqual((4, 7), white_king_loc)

        # move both kings manually using board method
        board.move_piece(black_king_loc, (3, 4))
        board.move_piece(white_king_loc, (3, 5))

        black_king_loc = board.get_king_location(Colour.BLACK)
        white_king_loc = board.get_king_location(Colour.WHITE)
        self.assertTupleEqual((3, 4), black_king_loc)
        self.assertTupleEqual((3, 5), white_king_loc)

    def test_clear(self):
        game: Game = Game()
        board: Board = game.board
        board.clear()
        for row in board:
            for block in row:
                self.assertIsNone(block.piece)
