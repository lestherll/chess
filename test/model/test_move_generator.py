from unittest import TestCase

from chess.custom_typehints import Coord2DSet
from chess.model.game import Game
from chess.model.board import Board
from chess.model.move_generator import generate_move
from chess.model.pieces import Pawn, Rook, Bishop, Queen, Knight, King


class TestMoveValidator(TestCase):

    def test_generate_move(self):
        # generate initial game with board object
        game: Game = Game()
        board: Board = game.board

        # test initial moves for pawns at the start of a game
        for i in range(8):
            self.assertSetEqual({(i, 2), (i, 3)}, generate_move(board=board, from_coord=(i, 1)))
            self.assertSetEqual({(i, 5), (i, 4)}, generate_move(board=board, from_coord=(i, 6)))

        # initial moves for rooks
        self.assertFalse(generate_move(board=board, from_coord=(0, 0)))
        self.assertFalse(generate_move(board=board, from_coord=(0, 7)))
        self.assertFalse(generate_move(board=board, from_coord=(7, 0)))
        self.assertFalse(generate_move(board=board, from_coord=(7, 7)))

        # initial moves for knights
        self.assertSetEqual({(0, 2), (2, 2)}, generate_move(board=board, from_coord=(1, 0)))
        self.assertSetEqual({(5, 2), (7, 2)}, generate_move(board=board, from_coord=(6, 0)))
        self.assertSetEqual({(0, 5), (2, 5)}, generate_move(board=board, from_coord=(1, 7)))
        self.assertSetEqual({(5, 5), (7, 5)}, generate_move(board=board, from_coord=(6, 7)))

        # initial moves for bishop
        self.assertFalse(generate_move(board=board, from_coord=(2, 0)))
        self.assertFalse(generate_move(board=board, from_coord=(5, 0)))
        self.assertFalse(generate_move(board=board, from_coord=(2, 7)))
        self.assertFalse(generate_move(board=board, from_coord=(5, 7)))

        # initial moves for queens
        self.assertFalse(generate_move(board=board, from_coord=(0, 4)))
        self.assertFalse(generate_move(board=board, from_coord=(7, 4)))

        # initial moves for kings
        self.assertFalse(generate_move(board=board, from_coord=(0, 5)))
        self.assertFalse(generate_move(board=board, from_coord=(7, 5)))

        # temporary test for unimplemented moves for other piece types
        # self.assertRaises(NotImplementedError, generate_move, board=board, coord=(0, 4))

    def test_pawn_blocked_at_front(self):
        board: Board = Board()
        board.put_piece((1, 0), Pawn("BLACK"))
        board.put_piece((0, 2), Pawn("WHITE"))
        self.assertSetEqual(set(), generate_move(board=board, from_coord=(0, 1)))

        board.clear()
        board.put_piece((1, 1), Pawn("BLACK"))
        board.put_piece((1, 3), Pawn("WHITE"))
        self.assertSetEqual({(1, 2)}, generate_move(board=board, from_coord=(1, 1)))

        board.clear()
        board.put_piece((0, 6), Pawn("WHITE"))
        board.put_piece((0, 5), Pawn("BLACK"))
        self.assertSetEqual(set(), generate_move(board=board, from_coord=(0, 6)))

        board.clear()
        board.put_piece((1, 6), Pawn("WHITE"))
        board.put_piece((1, 4), Pawn("BLACK"))
        self.assertSetEqual({(1, 5)}, generate_move(board=board, from_coord=(1, 4)))

        board.clear()
        board.put_piece((0, 6), Pawn("BLACK"))
        self.assertSetEqual({(0, 7)}, generate_move(board=board, from_coord=(0, 6)))
        board.put_piece((0, 1), Pawn("WHITE"))
        self.assertSetEqual({(0, 0)}, generate_move(board=board, from_coord=(0, 1)))

    def test_pawn_take_move(self):
        board: Board = Board()

        # setup black and white pawn such that white pawn
        # is in position for black to take it
        # 1 PB |
        #  ----|----
        # 2    | PW
        board.put_piece((0, 1), Pawn("BLACK", has_moved=True))
        board.put_piece((1, 2), Pawn("WHITE"))
        self.assertIn((1, 2), generate_move(board=board, from_coord=(0, 1)))

        # same setup but black pawn is in (1, 1) so can possibly
        # take (2, 2) which has a white pawn, and (0, 2) which is empty for now
        # 1    | PB |
        #  ----|----|----
        # 2    |    | PW
        board.put_piece((1, 1), Pawn("BLACK"))
        board.put_piece((2, 2), Pawn("WHITE"))
        self.assertIn((2, 2), generate_move(board=board, from_coord=(1, 1)))

        # added white pawn to lower left side of black pawn at (1, 1)
        # 1    | PB |
        #  ----|----|----
        # 2 PW |    | PW
        board.put_piece((0, 2), Pawn("WHITE"))
        self.assertIn((0, 2), generate_move(board=board, from_coord=(1, 1)))

        # changed colour of pawn at (x=0, y=2) from white to black hence
        # black pawn at (x=1, y=1) cannot take it
        # 1    | PB |
        #  ----|----|----
        # 2 PB |    | PW
        board[2][0].piece.colour = "BLACK"
        self.assertNotIn((0, 2), generate_move(board=board, from_coord=(1, 1)), msg=board)

    def test_rook_basic_move(self):
        # prepare 4x4 empty board with 1 white rook at (0, 0)
        board: Board = Board(_length=4)
        board.put_piece((0, 0), Rook("WHITE"))

        # check moveset
        expected_moveset: Coord2DSet = {
            (1, 0), (2, 0), (3, 0),
            (0, 1), (0, 2), (0, 3)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(0, 0))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_rook_blocked_move_by_ally(self):
        # prepare 4x4 empty board with 1 white rook at (0, 0)
        board: Board = Board(_length=4)
        board.put_piece((0, 0), Rook("WHITE"))
        board.put_piece((1, 0), Pawn("WHITE"))

        #
        expected_moveset: Coord2DSet = {
            (0, 1), (0, 2), (0, 3)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(0, 0))
        self.assertSetEqual(expected_moveset, actual_moveset)

        board.put_piece((0, 1), Pawn("WHITE"))
        expected_moveset = set()
        actual_moveset = generate_move(board=board, from_coord=(0, 0))
        self.assertSetEqual(expected_moveset, actual_moveset)

        board.remove_piece_at(from_coord=(1, 0))
        expected_moveset = {
            (1, 0), (2, 0), (3, 0)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(0, 0))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_rook_blocked_move_by_enemy(self):
        board: Board = Board(_length=4)
        board.put_piece((0, 0), Rook("WHITE"))
        board.put_piece((1, 0), Pawn("BLACK"))  # enemy piece

        # (1, 0) is the coordinate of the enemy piece
        expected_moveset: Coord2DSet = {
            (0, 1), (0, 2), (0, 3),
            (1, 0)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(0, 0))
        self.assertSetEqual(expected_moveset, actual_moveset)

        board.put_piece((0, 2), Pawn("BLACK"))
        expected_moveset: Coord2DSet = {
            (0, 1), (0, 2),
            (1, 0)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(0, 0))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_bishop_basic_move(self):
        board: Board = Board(_length=4)
        board.put_piece((2, 2), Bishop("WHITE"))

        expected_moveset: Coord2DSet = {
            (1, 1), (0, 0),
            (1, 3),
            (3, 1),
            (3, 3)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(2, 2))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_bishop_blocked_move_by_ally(self):
        board: Board = Board(_length=4)
        board.put_piece((2, 2), Bishop("WHITE"))
        board.put_piece((1, 1), Pawn("WHITE"))
        board.put_piece((3, 3), Pawn("WHITE"))

        expected_moveset: Coord2DSet = {
            (1, 3),
            (3, 1)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(2, 2))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_bishop_blocked_move_by_enemy(self):
        board: Board = Board(_length=4)
        board.put_piece((2, 2), Bishop("WHITE"))
        board.put_piece((1, 1), Pawn("BLACK"))
        board.put_piece((3, 3), Pawn("BLACK"))

        expected_moveset: Coord2DSet = {
            (1, 1),
            (1, 3),
            (3, 1),
            (3, 3)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(2, 2))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_queen_basic_move(self):
        board: Board = Board(_length=4)
        board.put_piece((2, 2), Queen("WHITE"))

        expected_moveset: Coord2DSet = {
            (0, 2), (1, 2), (3, 2),
            (2, 0), (2, 1), (2, 3),
            (0, 0), (1, 1), (3, 3),
            (1, 3), (3, 1)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(2, 2))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_knight_basic_move(self):
        board: Board = Board()
        board.put_piece((2, 2), Knight("WHITE"))

        expected_moveset: Coord2DSet = {
            (0, 1), (1, 0), (3, 0), (4, 1),
            (4, 3), (3, 4), (1, 4), (0, 3)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(2, 2))
        self.assertSetEqual(expected_moveset, actual_moveset, msg=actual_moveset)

    def test_king_basic_move(self):
        board: Board = Board(_length=3)
        board.put_piece((1, 1), King("BLACK"))

        expected_moveset: Coord2DSet = {
            (0, 0), (1, 0), (2, 0),
            (0, 1), (2, 1),
            (0, 2), (1, 2), (2, 2)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(1, 1))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_king_possible_move_into_bishop_check(self):
        board: Board = Board(_length=3)
        board.put_piece((1, 1), King("BLACK"))
        board.put_piece((1, 2), Bishop("WHITE"))

        expected_moveset: Coord2DSet = {
            (0, 0), (1, 0), (2, 0),

            (0, 2), (1, 2), (2, 2)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(1, 1))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_black_king_possible_move_into_pawn_check(self):
        board: Board = Board(_length=3)
        board.put_piece((1, 1), King("BLACK"))
        board.put_piece((1, 2), Pawn("WHITE"))

        expected_moveset: Coord2DSet = {
            (0, 0), (1, 0), (2, 0),

            (0, 2), (1, 2), (2, 2)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(1, 1))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_white_king_possible_move_into_pawn_check(self):
        board: Board = Board(_length=3)
        board.put_piece((1, 1), King("WHITE"))
        board.put_piece((1, 0), Pawn("BLACK"))

        expected_moveset: Coord2DSet = {
            (0, 0), (1, 0), (2, 0),

            (0, 2), (1, 2), (2, 2)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(1, 1))
        self.assertSetEqual(expected_moveset, actual_moveset)
