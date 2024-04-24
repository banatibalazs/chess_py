from enum import Enum

class PieceType(Enum):
    WH_PAWN = 1,
    WH_ROOK = 2,
    WH_KNIGHT = 3,
    WH_BISHOP = 4,
    WH_QUEEN = 5,
    WH_KING = 6,
    BL_PAWN = -1,
    BL_ROOK = -2,
    BL_KNIGHT = -3,
    BL_BISHOP = -4,
    BL_QUEEN = -5,
    BL_KING = -6