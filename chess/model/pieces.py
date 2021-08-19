from ..custom_typehints import Colour


class Piece:
    def __init__(self, colour: Colour, has_moved: bool = False) -> None:
        self.colour: Colour = colour
        self.has_moved = has_moved

    def __repr__(self) -> str:
        return f"Piece(colour={self.colour})"

    def __str__(self) -> str:
        return f"{to_piece_notation(self)}"


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


piece_notation = {
    King: "K",
    Queen: "Q",
    Bishop: "B",
    Knight: "N",
    Rook: "R",
    Pawn: "P",
    Piece: ""
}

def to_piece_notation(piece: Piece) -> str:
    notation: str = piece_notation[type(piece)]
    return notation if piece.colour is Colour.WHITE else notation.lower()











