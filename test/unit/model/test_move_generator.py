from typing import Tuple
from unittest import TestCase

from chess.custom_typehints import Coord2DSet, Colour, Coord2D
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
        board.put_piece((1, 0), Pawn(Colour.WHITE))
        board.put_piece((0, 2), Pawn(Colour.WHITE))
        self.assertSetEqual(set(), generate_move(board=board, from_coord=(0, 1)))

        board.clear()
        board.put_piece((1, 1), Pawn(Colour.BLACK))
        board.put_piece((1, 3), Pawn(Colour.WHITE))
        self.assertSetEqual({(1, 2)}, generate_move(board=board, from_coord=(1, 1)))

        board.clear()
        board.put_piece((0, 6), Pawn(Colour.WHITE))
        board.put_piece((0, 5), Pawn(Colour.BLACK))
        self.assertSetEqual(set(), generate_move(board=board, from_coord=(0, 6)))

        board.clear()
        board.put_piece((1, 6), Pawn(Colour.WHITE))
        board.put_piece((1, 4), Pawn(Colour.BLACK))
        self.assertSetEqual({(1, 5)}, generate_move(board=board, from_coord=(1, 4)))

        board.clear()
        board.put_piece((0, 6), Pawn(Colour.BLACK))
        self.assertSetEqual({(0, 7)}, generate_move(board=board, from_coord=(0, 6)))
        board.put_piece((0, 1), Pawn(Colour.WHITE))
        self.assertSetEqual({(0, 0)}, generate_move(board=board, from_coord=(0, 1)))

    def test_pawn_take_move(self):
        board: Board = Board()

        # setup black and white pawn such that white pawn
        # is in position for black to take it
        # 1 PB |
        #  ----|----
        # 2    | PW
        board.put_piece((0, 1), Pawn(Colour.BLACK, has_moved=True))
        board.put_piece((1, 2), Pawn(Colour.WHITE))
        self.assertIn((1, 2), generate_move(board=board, from_coord=(0, 1)))

        # same setup but black pawn is in (1, 1) so can possibly
        # take (2, 2) which has a white pawn, and (0, 2) which is empty for now
        # 1    | PB |
        #  ----|----|----
        # 2    |    | PW
        board.put_piece((1, 1), Pawn(Colour.BLACK))
        board.put_piece((2, 2), Pawn(Colour.WHITE))
        self.assertIn((2, 2), generate_move(board=board, from_coord=(1, 1)))

        # added white pawn to lower left side of black pawn at (1, 1)
        # 1    | PB |
        #  ----|----|----
        # 2 PW |    | PW
        board.put_piece((0, 2), Pawn(Colour.WHITE))
        self.assertIn((0, 2), generate_move(board=board, from_coord=(1, 1)))

        # changed colour of pawn at (x=0, y=2) from white to black hence
        # black pawn at (x=1, y=1) cannot take it
        # 1    | PB |
        #  ----|----|----
        # 2 PB |    | PW
        board[2][0].piece.colour = Colour.BLACK
        self.assertNotIn((0, 2), generate_move(board=board, from_coord=(1, 1)), msg=board)

    def test_rook_basic_move(self):
        # prepare 4x4 empty board with 1 white rook at (0, 0)
        board: Board = Board(_length=4)
        board.put_piece((0, 0), Rook(Colour.WHITE))

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
        board.put_piece((0, 0), Rook(Colour.WHITE))
        board.put_piece((1, 0), Pawn(Colour.WHITE))

        #
        expected_moveset: Coord2DSet = {
            (0, 1), (0, 2), (0, 3)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(0, 0))
        self.assertSetEqual(expected_moveset, actual_moveset)

        board.put_piece((0, 1), Pawn(Colour.WHITE))
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
        board.put_piece((0, 0), Rook(Colour.WHITE))
        board.put_piece((1, 0), Pawn(Colour.BLACK))  # enemy piece

        # (1, 0) is the coordinate of the enemy piece
        expected_moveset: Coord2DSet = {
            (0, 1), (0, 2), (0, 3),
            (1, 0)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(0, 0))
        self.assertSetEqual(expected_moveset, actual_moveset)

        board.put_piece((0, 2), Pawn(Colour.BLACK))
        expected_moveset: Coord2DSet = {
            (0, 1), (0, 2),
            (1, 0)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(0, 0))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_bishop_basic_move(self):
        board: Board = Board(_length=4)
        board.put_piece((2, 2), Bishop(Colour.WHITE))

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
        board.put_piece((2, 2), Bishop(Colour.WHITE))
        board.put_piece((1, 1), Pawn(Colour.WHITE))
        board.put_piece((3, 3), Pawn(Colour.WHITE))

        expected_moveset: Coord2DSet = {
            (1, 3),
            (3, 1)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(2, 2))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_bishop_blocked_move_by_enemy(self):
        board: Board = Board(_length=4)
        board.put_piece((2, 2), Bishop(Colour.WHITE))
        board.put_piece((1, 1), Pawn(Colour.BLACK))
        board.put_piece((3, 3), Pawn(Colour.BLACK))

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
        board.put_piece((2, 2), Queen(Colour.WHITE))

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
        board.put_piece((2, 2), Knight(Colour.WHITE))

        expected_moveset: Coord2DSet = {
            (0, 1), (1, 0), (3, 0), (4, 1),
            (4, 3), (3, 4), (1, 4), (0, 3)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(2, 2))
        self.assertSetEqual(expected_moveset, actual_moveset, msg=actual_moveset)

    def test_king_basic_move(self):
        board: Board = Board(_length=3)
        board.put_piece((1, 1), King(Colour.WHITE))

        expected_moveset: Coord2DSet = {
            (0, 0), (1, 0), (2, 0),
            (0, 1), (2, 1),
            (0, 2), (1, 2), (2, 2)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(1, 1))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_king_possible_move_into_bishop_check(self):
        board: Board = Board(_length=3)
        board.put_piece((1, 1), King(Colour.BLACK))
        board.put_piece((1, 2), Bishop(Colour.WHITE))

        expected_moveset: Coord2DSet = {
            (0, 0), (1, 0), (2, 0),

            (0, 2), (1, 2), (2, 2)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(1, 1))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_black_king_possible_move_into_pawn_check(self):
        board: Board = Board(_length=3)
        board.put_piece((1, 1), King(Colour.BLACK))
        board.put_piece((1, 2), Pawn(Colour.WHITE))

        expected_moveset: Coord2DSet = {
            (0, 0), (1, 0), (2, 0),

            (0, 2), (1, 2), (2, 2)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(1, 1))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_white_king_possible_move_into_pawn_check(self):
        board: Board = Board(_length=3)
        board.put_piece((1, 1), King(Colour.WHITE))
        board.put_piece((1, 0), Pawn(Colour.BLACK))

        expected_moveset: Coord2DSet = {
            (0, 0), (1, 0), (2, 0),

            (0, 2), (1, 2), (2, 2)
        }
        actual_moveset: Coord2DSet = generate_move(board=board, from_coord=(1, 1))
        self.assertSetEqual(expected_moveset, actual_moveset)

    def test_king_castling(self):
        # test will fail if board column length is less than 5
        # behaviour is undefined for column length greater than 8
        # only tests for instances where there are no pieces
        # between the rook and the king
        board: Board = Board()
        board.put_piece((4, 7), King(Colour.WHITE))
        board.put_piece((0, 7), Rook(Colour.WHITE))

        king_moveset: Coord2DSet = generate_move(board=board, from_coord=(4, 7))
        self.assertIn((2, 7), king_moveset)

        # king can castle when piece at the other side
        # is rook and is of the same colour as king
        board.put_piece((7, 7), Rook(Colour.WHITE))
        king_moveset: Coord2DSet = generate_move(board=board, from_coord=(4, 7))
        self.assertIn((6, 7), king_moveset)

        # cannot castle when colour is not the same
        board[7][7].piece.colour = Colour.BLACK
        king_moveset: Coord2DSet = generate_move(board=board, from_coord=(4, 7))
        self.assertNotIn((6, 7), king_moveset)

        # can castle again when the colour is the same
        board[7][4].piece.colour = Colour.BLACK
        king_moveset: Coord2DSet = generate_move(board=board, from_coord=(4, 7))
        self.assertIn((6, 7), king_moveset)

        # cannot castle again when the piece at the other side
        # is not a rook and is not the same colour as King
        board[7][7].piece = Bishop(Colour.BLACK)
        king_moveset: Coord2DSet = generate_move(board=board, from_coord=(4, 7))
        self.assertNotIn((6, 7), king_moveset)

    def test_king_castling_blocked(self):
        game: Game = Game()
        board: Board = game.board
        king_coord: Coord2D = board.get_king_location(Colour.BLACK)
        king_moveset: Coord2DSet = generate_move(board=board, from_coord=king_coord)

        # castling destinations
        left_castle: Coord2D = (king_coord[0] - 2, king_coord[1])
        right_castle: Coord2D = (king_coord[0] + 2, king_coord[1])
        self.assertNotIn(left_castle, king_moveset)
        self.assertNotIn(right_castle, king_moveset)

        # gradually remove pieces blocking the possible castle moves
        # remove one piece from both sides of the king
        board.remove_piece_at((king_coord[0] - 1, king_coord[1]))
        board.remove_piece_at((king_coord[0] + 1, king_coord[1]))
        king_moveset = generate_move(board=board, from_coord=king_coord)
        self.assertNotIn(left_castle, king_moveset)
        self.assertNotIn(right_castle, king_moveset)

        # remove one piece from both sides of the king again
        board.remove_piece_at((king_coord[0] - 2, king_coord[1]))
        board.remove_piece_at((king_coord[0] + 2, king_coord[1]))
        king_moveset = generate_move(board=board, from_coord=king_coord)

        self.assertNotIn(left_castle, king_moveset)
        self.assertIn(right_castle, king_moveset)  # right castle should now be possible

        # remove last piece on left side blocking rook and king
        board.remove_piece_at((king_coord[0] - 3, king_coord[1]))
        king_moveset = generate_move(board=board, from_coord=king_coord)
        self.assertIn(left_castle, king_moveset)  # left castle should now be possible

    def test_en_passant_white_target(self):
        board: Board = Board()
        board.put_piece((1, 4), Pawn(Colour.BLACK))
        board.put_piece((2, 4), Pawn(Colour.WHITE))

        last_move: Tuple[Coord2D, Coord2D] = ((2, 6), (2, 4))
        # 2,5 must be in moveset
        pawn_moveset: Coord2DSet = generate_move(board=board, from_coord=(1, 4), last_move=last_move)
        self.assertIn((2, 5), pawn_moveset)

        board.put_piece((0, 4), Pawn(Colour.WHITE))
        last_move = ((0, 6), (0, 4))
        pawn_moveset = generate_move(board=board, from_coord=(1, 4), last_move=last_move)
        self.assertIn((0, 5), pawn_moveset)

    def test_en_passant_black_target(self):
        board: Board = Board()
        board.put_piece((0, 3), Pawn(Colour.WHITE))
        board.put_piece((1, 3), Pawn(Colour.BLACK))

        last_move: Tuple[Coord2D, Coord2D] = ((1, 1), (1, 3))
        pawn_moveset: Coord2DSet = generate_move(board=board, from_coord=(0, 3), last_move=last_move)
        self.assertIn((1, 2), pawn_moveset)
