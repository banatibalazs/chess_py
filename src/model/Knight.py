import copy
from typing import override, Tuple, List

import numpy as np

from src.controller.CustomTypesForTypeHinting import ByteArray8x8
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Knight(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.KNIGHT, color, x, y)

    @override
    def update_attacked_fields(self, current_player, opponent):
        self._attacked_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        move_pattern_list = [(x - 1, y - 2), (x + 1, y - 2), (x - 2, y - 1), (x + 2, y - 1),
                             (x - 2, y + 1), (x + 2, y + 1), (x - 1, y + 2), (x + 1, y + 2)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                self._attacked_fields.add(move)

        self.update_protected_fields(current_player)
