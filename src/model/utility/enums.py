from enum import Enum


class Color(Enum):
    W = 1
    B = -1


class GameResult(Enum):
    WHITE_WON_BY_CHECKMATE = 1
    BLACK_WON_BY_CHECKMATE = -1
    WHITE_WON_BY_RESIGNATION = 2
    BLACK_WON_BY_RESIGNATION = -2
    WHITE_WON_BY_TIMEOUT = 3
    BLACK_WON_BY_TIMEOUT = -3
    DRAW_BY_STALEMATE = 4
    DRAW_BY_INSUFFICIENT_MATERIAL = 5
    DRAW_BY_THREEFOLD_REPETITION = 6


class SignedPieceType(Enum):
    WH_PAWN = 1
    WH_ROOK = 2
    WH_KNIGHT = 3
    WH_BISHOP = 4
    WH_QUEEN = 5
    WH_KING = 6
    BL_PAWN = -1
    BL_ROOK = -2
    BL_KNIGHT = -3
    BL_BISHOP = -4
    BL_QUEEN = -5
    BL_KING = -6
    NONE = 0


class UnsignedPieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6
    EMPTY = 0


class PlayerType(Enum):
    HUMAN = 1
    RANDOM = 2
    GREEDY = 3
    MINIMAX = 4
    MINIMAX_WITH_ALPHABETA = 5