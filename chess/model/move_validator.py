from typing import List, Tuple, Literal, Optional, Union, Set, Dict, Callable, Type

from chess.custom_typehints import MoveSet, Coord2D
from chess.model.board import Block, Board
from chess.model.pieces import Piece, Pawn, Rook, Bishop, Queen, King, Knight

ROOK_DIRECTIONS: MoveSet = {(0, 1), (1, 0), (0, -1), (-1, 0)}
BISHOP_DIRECTIONS: MoveSet = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
QUEEN_DIRECTIONS: MoveSet = ROOK_DIRECTIONS.union(BISHOP_DIRECTIONS)


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


def _generate_coord_moveset(board: Board, from_coord: Coord2D, directions: MoveSet, move_range: int) -> MoveSet:
    x, y = from_coord
    piece_to_move: Optional[Piece] = board[y][x].piece
    move_set: MoveSet = set()

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


def _generate_pawn_moves(board: Board, from_coord: Coord2D) -> MoveSet:
    x, y = from_coord
    piece_to_move: Optional[Piece] = board[y][x].piece
    move_set: MoveSet = set()

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


def _generate_rook_moves(board: Board, from_coord: Coord2D) -> MoveSet:
    return _generate_coord_moveset(board=board,
                                   from_coord=from_coord,
                                   directions=ROOK_DIRECTIONS,
                                   move_range=len(board))


def _generate_bishop_moves(board: Board, from_coord: Coord2D) -> MoveSet:
    return _generate_coord_moveset(board=board,
                                   from_coord=from_coord,
                                   directions=BISHOP_DIRECTIONS,
                                   move_range=len(board))


def _generate_queen_moves(board: Board, from_coord: Coord2D) -> MoveSet:
    return _generate_coord_moveset(board=board,
                                   from_coord=from_coord,
                                   directions=QUEEN_DIRECTIONS,
                                   move_range=len(board))


piece_type_moves: Dict[Type[Piece], Callable[[Board, Coord2D], MoveSet]] = {
    Pawn: _generate_pawn_moves,
    Rook: _generate_rook_moves,
    Bishop: _generate_bishop_moves,
    Queen: _generate_queen_moves
}


def generate_move(board: Board, from_coord: Coord2D) -> Union[MoveSet, NotImplementedError]:
    x, y = from_coord
    piece_to_move: Optional[Piece] = board[y][x].piece

    if piece_to_move is None:
        return set()

    move_set: MoveSet = piece_type_moves[piece_to_move.__class__](board, from_coord)

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

class MoveValidator:

    def move_is_valid(self, from_block: Block, to_block: Block) -> bool:
        piece_to_move: Piece = from_block.piece

        if not piece_to_move:
            return False

        generated_moves: List[Tuple[int, int]] = self.generate_move(from_block)
        if (to_block.y, to_block.x) not in generated_moves:
            return False
        elif to_block.piece:
            if from_block.piece.colour == to_block.piece.colour:
                return False

        return True

    def generate_move(self, from_block: Block) -> List[Tuple[int, int]]:
        piece_to_move: Piece = from_block.piece

        if not piece_to_move:
            return []

        move_set: List[Tuple[int, int]] = []

        if isinstance(piece_to_move, Pawn):
            side: Literal[1, -1] = 1
            if piece_to_move.colour != "BLACK":
                side *= -1

            if not piece_to_move.has_moved:
                move_set.append((from_block.y + 1 * side, from_block.x))
                move_set.append((from_block.y + 2 * side, from_block.x))
            else:
                move_set.append((from_block.y + 1 * side, from_block.x))

        elif isinstance(piece_to_move, Knight):
            for i in [-2, 2]:
                for j in [1, -1]:
                    move_set.append((from_block.y + i, from_block.x + j))
                    move_set.append((from_block.y + j, from_block.x + i))
        elif isinstance(piece_to_move, Rook):
            for i in range(1, 9):
                move_set.append((from_block.y + i, from_block.x))
                move_set.append((from_block.y - i, from_block.x))
                move_set.append((from_block.y, from_block.x + i))
                move_set.append((from_block.y, from_block.x - i))
        elif isinstance(piece_to_move, Bishop):
            for i in range(1, 9):
                move_set.append((from_block.y + i, from_block.x + i))
                move_set.append((from_block.y + i, from_block.x - i))
                move_set.append((from_block.y - i, from_block.x + i))
                move_set.append((from_block.y - i, from_block.x - i))
        elif isinstance(piece_to_move, Queen):
            for i in range(1, 9):
                move_set.append((from_block.y + i, from_block.x))
                move_set.append((from_block.y - i, from_block.x))
                move_set.append((from_block.y, from_block.x + i))
                move_set.append((from_block.y, from_block.x - i))
                move_set.append((from_block.y + i, from_block.x + i))
                move_set.append((from_block.y + i, from_block.x - i))
                move_set.append((from_block.y - i, from_block.x + i))
                move_set.append((from_block.y - i, from_block.x - i))
        elif isinstance(piece_to_move, King):
            move_set.append((from_block.y + 1, from_block.x))
            move_set.append((from_block.y - 1, from_block.x))
            move_set.append((from_block.y, from_block.x + 1))
            move_set.append((from_block.y, from_block.x - 1))
            move_set.append((from_block.y + 1, from_block.x + 1))
            move_set.append((from_block.y + 1, from_block.x - 1))
            move_set.append((from_block.y - 1, from_block.x + 1))
            move_set.append((from_block.y - 1, from_block.x - 1))

        return move_set
