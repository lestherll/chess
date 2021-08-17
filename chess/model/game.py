from typing import Tuple, Set, List

from chess.custom_typehints import Colour, GameStatus, Coord2D, Coord2DSet
from chess.model.board import Board, Block
from chess.model.move_generator import generate_move, get_attack_coords
from chess.model.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chess.model.player import Player


def is_in_check(board: Board, colour: Colour) -> bool:
    enemy_colour: Colour = Colour.WHITE if colour == Colour.BLACK else Colour.BLACK
    king_loc: Coord2D = board.get_king_location(colour)
    return king_loc in get_attack_coords(board=board, colour=enemy_colour)


class Game:

    def __init__(self, board: Board = None, *, is_white_turn: bool = True) -> None:
        if not board:
            self.board: Board = Board()
        self.black_player: Player = Player("BLACK", Colour.BLACK)
        self.white_player: Player = Player("WHITE", Colour.WHITE)
        self._is_white_turn: bool = is_white_turn
        self.moves_made: List = []
        self.turn_number: int = 1
        self.status: GameStatus = GameStatus.NORMAL
        self._setup()

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

    def turn(self) -> bool:
        return Colour.WHITE if self._is_white_turn else Colour.BLACK

    def _enemy(self) -> Colour:
        return Colour.BLACK if self._is_white_turn else Colour.WHITE

    # TODO: pieces can block check paths from enemy
    # TODO: when in check, player can only move king or block the check
    # TODO: rook pair also moves when the king castles
    def move(self, from_coord: Coord2D, to_coord: Coord2D) -> None:
        block: Block = self.board.get_block_from_tuple(from_coord)
        if block.piece is None:
            print(f"there's no piece at {from_coord}")
        elif block.piece.colour != self.turn():
            print(f"it's not {block.piece.colour}'s turn")
        else:
            move_set: Coord2DSet = generate_move(board=self.board, from_coord=from_coord)
            if to_coord in move_set:
                self.board.move_piece(from_coord, to_coord)
                self.moves_made.append((from_coord, to_coord))
                self.turn_number += 1

                # TODO: draw states
                # TODO: win states
                if is_in_check(self.board, self._enemy()):
                    current: Colour = self.turn()
                    self.status = GameStatus.WHITE_CHECKS_BLACK if current is Colour.WHITE \
                        else GameStatus.BLACK_CHECKS_WHITE
                    # if not generate_move(board=self.board, from_coord=self.board.get_king_location(self._enemy())):
                    #     self.status = GameStatus.WHITE_WIN if current is Colour.WHITE else GameStatus.BLACK_WIN
                else:
                    self.status = GameStatus.NORMAL

                self._is_white_turn = not self._is_white_turn

