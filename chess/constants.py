from chess.custom_typehints import Coord2DSet


BLACK_PAWN_DIRECTIONS: Coord2DSet = {(0, 1)}
BLACK_PAWN_ATTACK_DIRECTIONS: Coord2DSet = {(-1, 1), (1, 1)}
WHITE_PAWN_DIRECTIONS: Coord2DSet = {(0, -1)}
WHITE_PAWN_ATTACK_DIRECTIONS: Coord2DSet = {(-1, -1), (1, -1)}

KNIGHT_DIRECTIONS: Coord2DSet = {(-2, -1), (-1, -2), (1, -2), (2, -1),
                                 (2, 1), (1, 2), (-1, 2), (-2, 1)}
ROOK_DIRECTIONS: Coord2DSet = {(0, 1), (1, 0), (0, -1), (-1, 0)}
BISHOP_DIRECTIONS: Coord2DSet = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
QUEEN_DIRECTIONS: Coord2DSet = ROOK_DIRECTIONS.union(BISHOP_DIRECTIONS)
KING_DIRECTIONS: Coord2DSet = QUEEN_DIRECTIONS
