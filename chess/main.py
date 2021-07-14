from chess.game import Game
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
game.board.show()
board = game.board
mv = game.move_validator
board[2][0] = Block(2, 0, piece=Pawn("BLACK"))
board.show()
print(mv.generate_move(board[1][0]))
print(mv.move_is_valid(board[1][0], board[2][0]))
print(mv.move_is_valid(board[1][0], board[3][0]))
