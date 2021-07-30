from typing import List, Tuple, Literal, Optional, Union, Set

from chess.model.board import Block, Board
from chess.model.pieces import Piece, Pawn, Rook, Bishop, Queen, King, Knight


def generate_move(board: Board, coord: Tuple[int, int]) -> Union[Set[Tuple[int, int]], NotImplementedError]:
    x, y = coord
    piece_to_move: Optional[Piece] = board[y][x].piece

    if piece_to_move is None:
        return set()

    move_set: Set[Tuple[int, int]] = set()

    if isinstance(piece_to_move, Pawn):
        side: Literal[1, -1] = 1
        if piece_to_move.colour != "BLACK":
            side *= -1

        move_range: int = 1
        if not piece_to_move.has_moved:
            move_range = 2

        for i in range(move_range):
            curr_y: int = y+(i+1)*side
            if curr_y >= len(board)-1 or board[curr_y][x].piece is not None:
                break
            else:
                move_set.add((x, curr_y))

        take_range: Optional[Tuple[int, ...]] = None
        if x <= 0:
            take_range = (1, )
        elif x >= 7:
            take_range = (-1, )
        else:
            take_range = (-1, 1)

        for take_side in take_range:
            possible_block = board[y + 1 * side][x + take_side]
            if possible_block.piece is not None \
                    and possible_block.piece.colour != piece_to_move.colour:
                move_set.add((x+take_side, y+1*side))


    elif isinstance(piece_to_move, Piece):
        raise NotImplementedError(f"Moves for {piece_to_move.__class__.__name__} has not been implemented")

    return move_set

def _generate_pawn_moves(board: Board, coord: Tuple[int, int]) -> Set[Tuple[int, int]]:
    ...




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
                move_set.append((from_block.y+i, from_block.x))
                move_set.append((from_block.y-i, from_block.x))
                move_set.append((from_block.y, from_block.x+i))
                move_set.append((from_block.y, from_block.x-i))
        elif isinstance(piece_to_move, Bishop):
            for i in range(1, 9):
                move_set.append((from_block.y+i, from_block.x+i))
                move_set.append((from_block.y+i, from_block.x-i))
                move_set.append((from_block.y-i, from_block.x+i))
                move_set.append((from_block.y-i, from_block.x-i))
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


