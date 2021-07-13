from chess.model.board import Board
from chess.model.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Game:

    def __init__(self, board: Board = None) -> None:
        if not board:
            self.board = Board()
        self._setup()

    def _setup(self):
        for i in range(8):
            self.board[1][i].piece = Pawn("BLACK")
            self.board[6][i].piece = Pawn("WHITE")

        self.board[0][0].piece = Rook("BLACK")
        self.board[0][7].piece = Rook("BLACK")
        self.board[7][0].piece = Rook("WHITE")
        self.board[7][7].piece = Rook("WHITE")

        self.board[0][1].piece = Knight("BLACK")
        self.board[0][6].piece = Knight("BLACK")
        self.board[7][1].piece = Knight("WHITE")
        self.board[7][6].piece = Knight("WHITE")

        self.board[0][2].piece = Bishop("BLACK")
        self.board[0][5].piece = Bishop("BLACK")
        self.board[7][2].piece = Bishop("BLACK")
        self.board[7][5].piece = Bishop("BLACK")

        self.board[0][3].piece = Queen("BLACK")
        self.board[7][3].piece = Queen("WHITE")

        self.board[0][4].piece = King("BLACK")
        self.board[7][4].piece = King("WHITE")