from src.controller.CustomTypesForTypeHinting import ByteArray8x8, CharArray8x8
import numpy as np


class Board:

    NORMAL_MOVE_SYMBOL = b'n'
    SPECIAL_MOVE_SYMBOL = b's'
    SELECTED_PIECE_SYMBOL = b'x'
    EMPTY_SYMBOL = b'o'

    def __init__(self):
        self._piece_board = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board = np.zeros((8, 8), dtype=np.character)
        self._white_attack_board = np.zeros((8, 8), dtype=np.bool_)
        self._black_attack_board = np.zeros((8, 8), dtype=np.bool_)
        self._white_protection_board = np.zeros((8, 8), dtype=np.bool_)
        self._black_protection_board = np.zeros((8, 8), dtype=np.bool_)

    def is_normal_move_at(self, x, y):
        return self._coloring_board[y, x] == self.NORMAL_MOVE_SYMBOL

    def is_special_move_at(self, x, y):
        return self._coloring_board[y, x] == self.SPECIAL_MOVE_SYMBOL

    def is_empty_at(self, x: int, y: int) -> bool:
        return self._piece_board[y][x] == 0

    def square_is_attacked_by_white(self, x, y) -> bool:
        return bool(self._white_attack_board[y, x])

    def square_is_attacked_by_black(self, x, y) -> bool:
        return bool(self._black_attack_board[y, x])

    def get_coloring_board(self) -> CharArray8x8:
        return self._coloring_board

    def get_piece_board(self) -> ByteArray8x8:
        return self._piece_board

    def is_selected_piece_at(self, x: int, y: int) -> bool:
        return self._coloring_board[y, x] == self.SELECTED_PIECE_SYMBOL

    def get_black_attack_board(self):
        return self._black_attack_board

    def get_white_attack_board(self):
        return self._white_attack_board

    def get_black_protection_board(self):
        return self._black_protection_board

    def get_white_protection_board(self):
        return self._white_protection_board



