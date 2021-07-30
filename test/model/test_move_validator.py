from unittest import TestCase

from chess.model.game import Game
from chess.model.board import Board
from chess.model.move_validator import generate_move
from chess.model.pieces import Pawn


class TestMoveValidator(TestCase):

    def test_generate_move(self):

        # generate initial game with board object
        game: Game = Game()
        board: Board = game.board

        # test initial moves for pawns at the start of a game
        for i in range(8):
            self.assertSetEqual({(i, 2), (i, 3)}, generate_move(board=board, coord=(i, 1)))
            self.assertSetEqual({(i, 5), (i, 4)}, generate_move(board=board, coord=(i, 6)))

        # initial moves for rooks
        self.assertSetEqual(set(), generate_move(board=board, coord=(0, 0)))
        self.assertSetEqual(set(), generate_move(board=board, coord=(0, 7)))
        self.assertSetEqual(set(), generate_move(board=board, coord=(7, 0)))
        self.assertSetEqual(set(), generate_move(board=board, coord=(7, 7)))


        # temporary test for unimplemented moves for other piece types
        # self.assertRaises(NotImplementedError, generate_move, board=board, coord=(0, 4))

    def test_pawn_blocked_at_front(self):
        board: Board = Board()
        board[1][0].piece = Pawn("BLACK")
        board[2][0].piece = Pawn("WHITE")
        self.assertSetEqual(set(), generate_move(board=board, coord=(0, 1)))

        board.clear()
        board[1][1].piece = Pawn("BLACK")
        board[3][1].piece = Pawn("WHITE")
        self.assertSetEqual({(1, 2)}, generate_move(board=board, coord=(1, 1)), msg=board)

        board.clear()
        board[6][0].piece = Pawn("WHITE")
        board[5][0].piece = Pawn("BLACK")
        self.assertSetEqual(set(), generate_move(board=board, coord=(0, 6)), msg=board)

        board.clear()
        board[6][1].piece = Pawn("WHITE")
        board[4][1].piece = Pawn("BLACK")
        self.assertSetEqual({(1, 5)}, generate_move(board=board, coord=(1, 4)), msg=board)

        board.clear()
        board[6][0].piece = Pawn("BLACK")
        self.assertSetEqual({(0, 7)}, generate_move(board=board, coord=(0, 6)), msg=board)
        board[1][0].piece = Pawn("WHITE")
        self.assertSetEqual({(0, 0)}, generate_move(board=board, coord=(0, 1)), msg=board)

    def test_pawn_take_move(self):
        board: Board = Board()

        # setup black and white pawn such that white pawn
        # is in position for black to take it
        # 1 PB |
        #  ----|----
        # 2    | PW
        board[1][0].piece = Pawn("BLACK", has_moved=True)
        board[2][1].piece = Pawn("WHITE")
        self.assertIn((1, 2), generate_move(board=board, coord=(0, 1)))

        # same setup but black pawn is in (1, 1) so can possibly
        # take (2, 2) which has a white pawn, and (0, 2) which is empty for now
        # 1    | PB |
        #  ----|----|----
        # 2    |    | PW
        board[1][1].piece = Pawn("BLACK")
        board[2][2].piece = Pawn("WHITE")
        self.assertIn((2, 2), generate_move(board=board, coord=(1, 1)), msg=board)

        # added white pawn to lower left side of black pawn at (1, 1)
        # 1    | PB |
        #  ----|----|----
        # 2 PW |    | PW
        board[2][0].piece = Pawn("WHITE")
        self.assertIn((0, 2), generate_move(board=board, coord=(1, 1)), msg=board)

        # changed colour of pawn at (x=0, y=2) from white to black hence
        # black pawn at (x=1, y=1) cannot take it
        # 1    | PB |
        #  ----|----|----
        # 2 PB |    | PW
        board[2][0].piece.colour = "BLACK"
        self.assertNotIn((0, 2), generate_move(board=board, coord=(1, 1)), msg=board)
