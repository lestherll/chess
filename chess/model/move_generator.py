from itertools import chain
from typing import List, Tuple, Literal, Optional, Union, Set, Dict, Callable, Type, Iterable

from chess.custom_typehints import Coord2DSet, Coord2D, Colour
from chess.model.board import Block, Board
from chess.model.pieces import Piece, Pawn, Rook, Bishop, Queen, King, Knight

BLACK_PAWN_DIRECTIONS: Coord2DSet = {(0, 1)}
BLACK_PAWN_ATTACK_DIRECTIONS: Coord2DSet = {(-1, 1), (1, 1)}
WHITE_PAWN_DIRECTIONS: Coord2DSet = {(0, -1)}
WHITE_PAWN_ATTACK_DIRECTIONS: Coord2DSet = {(-1, -1), (1, -1)}

KNIGHT_DIRECTIONS: Coord2DSet = {(-2, -1), (-1, -2), (1, -2), (2, -1),
                                 (2, 1), (1, 2), (-1, 2), (-2, 1)}
ROOK_DIRECTIONS: Coord2DSet = {(0, 1), (1, 0), (0, -1), (-1, 0)}
BISHOP_DIRECTIONS: Coord2DSet = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
QUEEN_DIRECTIONS: Coord2DSet = ROOK_DIRECTIONS.union(BISHOP_DIRECTIONS)
KING_DIRECTIONS: Coord2DSet = QUEEN_DIRECTIONS


def out_of_bounds(from_coord: Coord2D, bound_range: int) -> bool:
    """
    Checks if any of the components of *coord* is not in 0 to *bound_range*
    :param from_coord:
    :param bound_range:
    :return:
    """
    x, y = from_coord
    if x < 0 or x > bound_range - 1 or y < 0 or y > bound_range - 1:
        return True
    return False


def _generate_coord_moveset(board: Board, from_coord: Coord2D, directions: Coord2DSet, move_range: int) -> Coord2DSet:
    x, y = from_coord
    piece_to_move: Optional[Piece] = board[y][x].piece
    move_set: Coord2DSet = set()

    for direction in directions:
        for i in range(1, move_range + 1):
            advancement: Coord2D = (direction[0] * i, direction[1] * i)
            curr_coord: Coord2D = (x + advancement[0], y + advancement[1])

            if out_of_bounds(from_coord=curr_coord, bound_range=len(board)):
                break

            curr_block: Block = board[curr_coord[1]][curr_coord[0]]
            if curr_block.piece is None:
                move_set.add(curr_coord)
            else:
                # if piece at curr_block is different colour,
                # add current coordinate to move_set
                if curr_block.piece.colour != piece_to_move.colour and type(piece_to_move) != Pawn:
                    move_set.add(curr_coord)
                break
    return move_set


def _generate_pawn_moves(board: Board, from_coord: Coord2D) -> Coord2DSet:
    x, y = from_coord
    piece_to_move: Piece = board[y][x].piece
    move_range: int = 1 if piece_to_move.has_moved else 2

    side: Literal[1, -1] = -1
    directions: Coord2DSet = WHITE_PAWN_DIRECTIONS
    if piece_to_move.colour == "BLACK":
        directions = BLACK_PAWN_DIRECTIONS
        side *= -1

    move_set: Coord2DSet = set()
    for i in (-1, 1):
        curr_coord: Coord2D = (x + i, y + 1 * side)
        if not out_of_bounds(curr_coord, len(board)):
            curr_block: Block = board[curr_coord[1]][curr_coord[0]]
            if curr_block.piece and curr_block.piece.colour != piece_to_move.colour:
                move_set.add(curr_coord)

    return move_set.union(_generate_coord_moveset(board=board,
                                                  from_coord=from_coord,
                                                  directions=directions,
                                                  move_range=move_range))


def _generate_rook_moves(board: Board, from_coord: Coord2D) -> Coord2DSet:
    return _generate_coord_moveset(board=board,
                                   from_coord=from_coord,
                                   directions=ROOK_DIRECTIONS,
                                   move_range=len(board))


def _generate_knight_moves(board: Board, from_coord: Coord2D) -> Coord2DSet:
    return _generate_coord_moveset(board=board,
                                   from_coord=from_coord,
                                   directions=KNIGHT_DIRECTIONS,
                                   move_range=1)


def _generate_bishop_moves(board: Board, from_coord: Coord2D) -> Coord2DSet:
    return _generate_coord_moveset(board=board,
                                   from_coord=from_coord,
                                   directions=BISHOP_DIRECTIONS,
                                   move_range=len(board))


def _generate_queen_moves(board: Board, from_coord: Coord2D) -> Coord2DSet:
    return _generate_coord_moveset(board=board,
                                   from_coord=from_coord,
                                   directions=QUEEN_DIRECTIONS,
                                   move_range=len(board))


def _generate_king_moves(board: Board, from_coord: Coord2D) -> Coord2DSet:
    enemy_colour: Colour = "WHITE" if board[from_coord[1]][from_coord[0]].colour() == "BLACK" else "BLACK"
    return _generate_coord_moveset(board=board,
                                   from_coord=from_coord,
                                   directions=KING_DIRECTIONS,
                                   move_range=1)\
        .difference(get_attack_coords(board=board, colour=enemy_colour, exclude_type=[King]))\
        .difference(_get_pawn_diag_attack(board=board, colour=enemy_colour))


piece_type_moves: Dict[Type[Piece], Callable[[Board, Coord2D], Coord2DSet]] = {
    Pawn: _generate_pawn_moves,
    Rook: _generate_rook_moves,
    Knight: _generate_knight_moves,
    Bishop: _generate_bishop_moves,
    Queen: _generate_queen_moves,
    King: _generate_king_moves
}


def generate_move(board: Board, from_coord: Coord2D) -> Union[Coord2DSet, NotImplementedError]:
    x, y = from_coord
    piece_to_move: Optional[Piece] = board[y][x].piece

    if piece_to_move is None:
        return set()

    move_set: Coord2DSet = piece_type_moves[piece_to_move.__class__](board, from_coord)

    return move_set


def get_attack_coords(board: Board, colour: Colour, exclude_type: Iterable = None) -> Coord2DSet:
    if exclude_type is None:
        exclude_type = []

    if not isinstance(exclude_type, Iterable):
        exclude_type = [exclude_type]

    move_set: List[Coord2DSet] = []
    for i, j in board.get_pieces_by_colour(colour, exclude_type=exclude_type):
        move_set.append(generate_move(board=board, from_coord=(i, j)))

    return set(chain(*move_set))


def _get_pawn_diag_attack(board: Board, colour: Colour) -> Coord2DSet:
    pawn_dir: Coord2DSet = BLACK_PAWN_ATTACK_DIRECTIONS if colour == "BLACK" else WHITE_PAWN_ATTACK_DIRECTIONS

    move_set: List[Coord2DSet] = []
    for i, j in board.get_pieces_by_colour(colour, exclude_type=[Rook, Knight, Bishop, Queen, King]):
        move_set.append(_generate_coord_moveset(board=board,
                                                from_coord=(i, j),
                                                directions=pawn_dir,
                                                move_range=1))
    return set(chain(*move_set))
