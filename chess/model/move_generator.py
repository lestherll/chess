from itertools import chain
from typing import List, Tuple, Literal, Optional, Union, Set, Dict, Callable, Type, Iterable

from chess.custom_typehints import Coord2DSet, Coord2D, Colour
from chess.model.board import Block, Board
from chess.model.pieces import Piece, Pawn, Rook, Bishop, Queen, King, Knight

from chess.constants import *


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


def _generate_coord_moveset(board: Board,
                            from_coord: Coord2D,
                            directions: Coord2DSet,
                            move_range: int
                            ) -> Coord2DSet:
    """
    Helper method for generating move coordinates based on a direction set and move_range given
    :param board: board to generate moveset from (contains the bounds for the coordinates that can be taken)
    :param from_coord: location to generate moveset from
    :param directions: directions the piece can take
    :param move_range: depicts how many times the directions can be taken
    :return: possible movements(normal) from the direction and range
    """
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


def _generate_pawn_moves(board: Board, from_coord: Coord2D, last_move: Tuple[Coord2D, Coord2D] = tuple()) -> Coord2DSet:
    x, y = from_coord
    piece_to_move: Piece = board[y][x].piece
    move_range: int = 1 if piece_to_move.has_moved else 2

    side: Literal[1, -1] = -1
    directions: Coord2DSet = WHITE_PAWN_DIRECTIONS
    if piece_to_move.colour == Colour.BLACK:
        directions = BLACK_PAWN_DIRECTIONS
        side *= -1

    move_set: Coord2DSet = set()
    for i in (-1, 1):
        curr_coord: Coord2D = (x + i, y + 1 * side)
        if not out_of_bounds(curr_coord, len(board)):
            curr_block: Block = board[curr_coord[1]][curr_coord[0]]
            if curr_block.piece and curr_block.piece.colour != piece_to_move.colour:
                move_set.add(curr_coord)

    if len(last_move) == 2 and all([len(coord) == 2 for coord in last_move]):
        move_set.add(_en_passant_move(board, from_coord, last_move))

    return move_set.union(_generate_coord_moveset(board=board,
                                                  from_coord=from_coord,
                                                  directions=directions,
                                                  move_range=move_range))


def _en_passant_move(board: Board,
                     from_coord: Coord2D,
                     last_move: Tuple[Coord2D, Coord2D]
                     ) -> Union[Coord2D, Tuple[()]]:
    """
    Generate move for an en passant move for a pawn piece if valid
    """
    x, y = from_coord
    piece_to_move: Piece = board[y][x].piece

    # en passant is only possible on this row based on colour
    row_to_move: int = 4 if piece_to_move.colour is Colour.BLACK else 3
    column_diff: int = abs(x - last_move[0][0])
    jumped_two: bool = True if abs(last_move[0][1]-last_move[1][1]) == 2 else False

    # if the difference in y of the last move is 2 then en passant is possible
    # only if the pawn piece to move is 1 column away from the last moved piece
    # from either side and is in the correct row(4 for black, 3 for white in terms)
    # of list index
    last_move_x, last_move_y = last_move[1]
    if (y != row_to_move or column_diff != 1 or not jumped_two) or\
            board[last_move_y][last_move_x].colour() is piece_to_move.colour or\
            not isinstance(board[last_move_y][last_move_x].piece, Pawn) or\
            not isinstance(board[y][x].piece, Pawn):
        return tuple()
    else:
        y_dir: int = 1 if piece_to_move.colour is Colour.BLACK else -1
        return last_move[0][0], y + y_dir


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
    x, y = from_coord
    enemy_colour: Colour = Colour.WHITE if board[y][x].colour() == Colour.BLACK else Colour.BLACK

    castle_move: Coord2DSet = set()
    if len(board) == 8 and not board[y][x].piece.has_moved:
        # enforce castling only for standard board size
        # check if:
        # 1. king has not moved
        # 2. if there is a rook
        # 3. if rook is of same colour with king
        # 4. if the gap between king and rook is empty
        if all([not board[j][i].piece for i, j in [(x - 1, y), (x - 2, y), (x - 3, y)]]) and \
                isinstance(board[y][x - 4].piece, Rook) and \
                board[y][x - 4].colour() is board[y][x].colour():
            castle_move.add((x - 2, y))
        if all([not board[j][i].piece for i, j in [(x + 1, y), (x + 2, y)]]) and \
                isinstance(board[y][x + 3].piece, Rook) and \
                board[y][x + 3].colour() is board[y][x].colour():
            castle_move.add((x + 2, y))

    generated_normal_moves: Coord2DSet = _generate_coord_moveset(board=board,
                                                                 from_coord=from_coord,
                                                                 directions=KING_DIRECTIONS,
                                                                 move_range=1)
    # generate normal enemy moves
    normal_enemy_moves: Coord2DSet = get_attack_coords(board=board, colour=enemy_colour, exclude_type=King)
    # generate enemy pawn diagonal pseudo-moves
    enemy_pawn_diag_moves: Coord2DSet = _get_pawn_diag_attack(board=board, colour=enemy_colour)
    # verify that king can't move into places they can get checked
    return (generated_normal_moves | castle_move) - normal_enemy_moves - enemy_pawn_diag_moves


# map piece type to correct generation method
piece_type_moves: Dict[Type[Piece], Callable[[Board, Coord2D], Coord2DSet]] = {
    Pawn: _generate_pawn_moves,
    Rook: _generate_rook_moves,
    Knight: _generate_knight_moves,
    Bishop: _generate_bishop_moves,
    Queen: _generate_queen_moves,
    King: _generate_king_moves
}


def generate_move(board: Board, from_coord: Coord2D, last_move: Tuple[Coord2D, Coord2D] = tuple()) -> Coord2DSet:
    """Generate moveset(of Coord2DSet annotation) for a piece on the board"""
    x, y = from_coord
    piece_to_move: Optional[Piece] = board[y][x].piece

    if piece_to_move is None:
        return set()

    piece_type: Type[Piece] = type(piece_to_move)
    if piece_type is not Pawn:
        move_set: Coord2DSet = piece_type_moves[piece_type](board, from_coord)
    else:
        move_set: Coord2DSet = piece_type_moves[piece_type](board, from_coord, last_move=last_move)

    return move_set


def get_attack_coords(board: Board, colour: Colour,
                      exclude_type: Union[Iterable[Piece], Type[Piece]] = None
                      ) -> Coord2DSet:
    """Generate all valid attack coordinates of a given colour from a board"""
    if exclude_type is None:
        exclude_type = []

    if not isinstance(exclude_type, Iterable):
        exclude_type = [exclude_type]

    move_set: List[Coord2DSet] = []
    for i, j in board.get_pieces_by_colour(colour, exclude_type=exclude_type):
        move_set.append(generate_move(board=board, from_coord=(i, j)))

    return set(chain(*move_set))


def _get_pawn_diag_attack(board: Board, colour: Colour) -> Coord2DSet:
    """
    Helper function for generating diagonal pawn pseudo-moves of the passed
    colour, which are moves that can only be taken on a special case. A pawn
    diagonal move is only valid if there is an enemy piece on the destination block.
    :param board: board state to generate pawn diagonal movements from
    :param colour: colour of the pawns
    :return: coordinate diagonal to all possible diagonal destinations of all pawns for a colour
    """
    pawn_dir: Coord2DSet = BLACK_PAWN_ATTACK_DIRECTIONS if colour == Colour.BLACK else WHITE_PAWN_ATTACK_DIRECTIONS

    move_set: List[Coord2DSet] = []
    for i, j in board.get_pieces_by_colour(colour, exclude_type=[Rook, Knight, Bishop, Queen, King]):
        move_set.append(_generate_coord_moveset(board=board,
                                                from_coord=(i, j),
                                                directions=pawn_dir,
                                                move_range=1))
    return set(chain(*move_set))
