from enum import Enum


class Color(Enum):
    W = 1
    B = -1
    N = 0


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


class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6


class PlayerType(Enum):
    HUMAN = 1
    RANDOM = 2
    GREEDY = 3
    MINIMAX = 4
    MINIMAX_WITH_ALPHABETA = 5