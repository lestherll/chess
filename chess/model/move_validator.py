from typing import List, Tuple, Literal, Optional, Union, Set, Dict, Callable, Type

from chess.custom_typehints import Coord2DSet, Coord2D
from chess.model.board import Block, Board
from chess.model.pieces import Piece, Pawn, Rook, Bishop, Queen, King, Knight

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
                if curr_block.piece.colour != piece_to_move.colour:
                    move_set.add(curr_coord)
                break
    return move_set


def _generate_pawn_moves(board: Board, from_coord: Coord2D) -> Coord2DSet:
    x, y = from_coord
    piece_to_move: Optional[Piece] = board[y][x].piece
    move_set: Coord2DSet = set()

    side: Literal[1, -1] = 1
    if piece_to_move.colour != "BLACK":
        side *= -1

    move_range: int = 1
    if not piece_to_move.has_moved:
        move_range = 2

    for i in range(move_range):
        curr_y: int = y + (i + 1) * side
        if curr_y > len(board) - 1 or curr_y < 0 \
                or board[curr_y][x].piece is not None:
            break
        else:
            move_set.add((x, curr_y))

    take_range: Optional[Tuple[int, ...]] = None
    if x <= 0:
        take_range = (1,)
    elif x >= 7:
        take_range = (-1,)
    else:
        take_range = (-1, 1)

    for take_side in take_range:
        possible_block = board[y + 1 * side][x + take_side]
        if possible_block.piece is not None \
                and possible_block.piece.colour != piece_to_move.colour:
            move_set.add((x + take_side, y + 1 * side))

    return move_set


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
    return _generate_coord_moveset(board=board,
                                   from_coord=from_coord,
                                   directions=KING_DIRECTIONS,
                                   move_range=1)


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

    # if isinstance(piece_to_move, Pawn):
    #     move_set = _generate_pawn_moves(board=board, from_coord=from_coord)
    #
    # elif isinstance(piece_to_move, Rook):
    #     move_set = _generate_rook_moves(board=board, from_coord=from_coord)
    #
    # elif isinstance(piece_to_move, Bishop):
    #     move_set = _generate_bishop_moves(board=board, from_coord=from_coord)
    #
    # elif isinstance(piece_to_move, Queen):
    #     move_set = _generate_queen_moves(board=board, from_coord=from_coord)
    #
    # elif isinstance(piece_to_move, Piece):
    #     raise NotImplementedError(f"Moves for {piece_to_move.__class__.__name__} has not been implemented")

    return move_set


class MoveValidator: ...
