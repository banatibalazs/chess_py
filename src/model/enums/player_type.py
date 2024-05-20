from enum import Enum


class PlayerType(Enum):
    HUMAN = 1
    RANDOM = 2
    GREEDY = 3
    MINIMAX = 4
    MINIMAX_WITH_ALPHABETA = 5