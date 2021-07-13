from ..types import Colour


class Piece:
    def __init__(self, colour: Colour, has_moved: bool = False) -> None:
        self.colour: Colour = colour
        self.has_moved = has_moved

    def __repr__(self) -> str:
        return f"Piece(colour={self.colour})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__[:2]}{self.colour[0]}"


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