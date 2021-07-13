from ..types import Colour


class Piece:
    def __init__(self, colour: Colour) -> None:
        self.colour = colour

    def __repr__(self) -> str:
        return f"Piece(colour={self.colour})"


class Pawn(Piece):
    pass


class Rook(Piece):
    pass


class Knight(Piece):
    pass


class Bishop(Piece):
    pass


class Queen(Piece):
    pass


class King(Piece):
    pass
