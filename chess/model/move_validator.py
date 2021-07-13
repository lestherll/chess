from typing import List, Tuple, Literal

from chess.model.board import Block
from chess.model.pieces import Piece, Pawn, Rook, Bishop, Queen, King, Knight


class MoveValidator:

    def move_is_valid(self, from_block: Block, to_block: Block) -> bool:
        piece_to_move: Piece = from_block.piece

        if not piece_to_move:
            return False

    def generate_move(self, from_block: Block) -> List[Tuple[int, int]]:
        piece_to_move: Piece = from_block.piece

        if not piece_to_move:
            return []

        move_set: List[Tuple[int, int]] = []

        if isinstance(piece_to_move, Pawn):
            side: Literal[1, -1] = 1
            if piece_to_move.colour != "WHITE":
                side *= -1

            if not piece_to_move.has_moved:
                move_set.append((from_block.y + 1 * side, from_block.x + 1 * side))
                move_set.append((from_block.y + 2 * side, from_block.x + 2 * side))
            else:
                move_set.append((from_block.y + 1 * side, from_block.x + 1 * side))

        elif isinstance(piece_to_move, Knight):
            for i in [-2, 2]:
                for j in [1, -1]:
                    move_set.append((from_block.y + i, from_block.x + j))
                    move_set.append((from_block.y + j, from_block.x + i))

            # move_set.append((from_block.y + 2, from_block.x + 1))
            # move_set.append((from_block.y + 2, from_block.x - 1))
            # move_set.append((from_block.y - 2, from_block.x + 1))
            # move_set.append((from_block.y - 2, from_block.x - 1))
            # move_set.append((from_block.y + 1, from_block.x + 2))
            # move_set.append((from_block.y - 1, from_block.x + 2))
            # move_set.append((from_block.y + 1, from_block.x - 2))
            # move_set.append((from_block.y - 1, from_block.x - 2))
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


