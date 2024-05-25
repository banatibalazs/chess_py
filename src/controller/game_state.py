from typing import Optional, Tuple, Set

import numpy as np

from src.controller.custom_types_for_type_hinting import ByteArray8x8


class GameState:
    def __init__(self):
        self.board: ByteArray8x8 = np.array([
            [-2, -3, -4, -5, -6, -4, -3, -2],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [2, 3, 4, 5, 6, 4, 3, 2]], dtype=np.byte)

        self.step_from: Optional[Tuple[int, int]] = None
        self.step_to: Optional[Tuple[int, int]] = None

        self._possible_fields: Set[Tuple[int, int]] = set()

        self._last_move = None
        self._last_moved_piece = None

        # black king
        self._king_04_is_moved = False
        # white king
        self._king_74_is_moved = False
        # black rooks
        self._rook_00_is_moved = False
        self._rook_07_is_moved = False
        # white rooks
        self._rook_70_is_moved = False
        self._rook_77_is_moved = False

        self._is_en_passant = False

        self.is_white_turn: bool = True
        self.is_game_over: bool = False

    @property
    def last_move(self):
        return self._last_move

    @last_move.setter
    def last_move(self, value):
        self._last_move = value

    @property
    def last_moved_piece(self):
        return self._last_moved_piece

    @last_moved_piece.setter
    def last_moved_piece(self, value):
        self._last_moved_piece = value

    @property
    def possible_fields(self):
        return self._possible_fields

    @possible_fields.setter
    def possible_fields(self, value):
        self._possible_fields = value

    @property
    def king_04_is_moved(self):
        return self._king_04_is_moved

    @king_04_is_moved.setter
    def king_04_is_moved(self, value):
        self._king_04_is_moved = value

    @property
    def king_74_is_moved(self):
        return self._king_74_is_moved

    @king_74_is_moved.setter
    def king_74_is_moved(self, value):
        self._king_74_is_moved = value

    @property
    def rook_00_is_moved(self):
        return self._rook_00_is_moved

    @rook_00_is_moved.setter
    def rook_00_is_moved(self, value):
        self._rook_00_is_moved = value

    @property
    def rook_07_is_moved(self):
        return self._rook_07_is_moved

    @rook_07_is_moved.setter
    def rook_07_is_moved(self, value):
        self._rook_07_is_moved = value

    @property
    def rook_70_is_moved(self):
        return self._rook_70_is_moved

    @rook_70_is_moved.setter
    def rook_70_is_moved(self, value):
        self._rook_70_is_moved = value

    @property
    def rook_77_is_moved(self):
        return self._rook_77_is_moved

    @rook_77_is_moved.setter
    def rook_77_is_moved(self, value):
        self._rook_77_is_moved = value

    @property
    def is_en_passant(self):
        return self._is_en_passant

    @is_en_passant.setter
    def is_en_passant(self, value):
        self._is_en_passant = value

    @property
    def is_white_turn(self):
        return self._is_white_turn

    @is_white_turn.setter
    def is_white_turn(self, value):
        self._is_white_turn = value

    @property
    def is_game_over(self):
        return self._is_game_over

    @is_game_over.setter
    def is_game_over(self, value):
        self._is_game_over = value


