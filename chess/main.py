from chess.model.game import Game
from chess.model.move_generator import generate_move, get_attack_coords, _get_pawn_diag_attack
from chess.model.pieces import Piece, Pawn
from model.board import Board, Block

# board = Board()
# # for row in board.blocks:
# #     print(row)
# board.show()
#
# board.put_piece(Block(1, 1), Piece("BLACK"))
# board.show()
#
# board.move_piece(Block(1, 1), Block(2, 3))
# board.show()
#
# print(board[Block(1,1)])
# print(board[Block(2,3)])
# board.remove_piece(Block(2,3))
# board.show()

# -------
game = Game()
board = game.board
print(board)
board[2][0] = Block(2, 0, piece=Pawn("BLACK"))
print(board)
print(generate_move(board=board, from_coord=(0, 1)))

print(get_attack_coords(board=board, colour="BLACK"))

board.clear()
board.put_piece((2, 5), piece=Pawn("WHITE"))
print(_get_pawn_diag_attack(board=board, colour="WHITE"))