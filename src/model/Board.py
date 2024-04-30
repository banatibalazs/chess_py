from typing import List, Tuple

from src.controller.CustomTypesForTypeHinting import ByteArray8x8, CharArray8x8, BoolArray8x8
import numpy as np

from src.model.Piece import Piece


class Board:

    NORMAL_MOVE_SYMBOL = b'n'
    SPECIAL_MOVE_SYMBOL = b's'
    SELECTED_PIECE_SYMBOL = b'x'
    EMPTY_SYMBOL = b'o'

    def __init__(self):
        self._piece_board: ByteArray8x8 = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board: CharArray8x8 = np.zeros((8, 8), dtype=np.character)
        self._white_attack_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)
        self._black_attack_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)
        self._white_protection_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)
        self._black_protection_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)

    def reset_coloring_board(self):
        self._coloring_board.fill(self.EMPTY_SYMBOL)

    def update_coloring_board(self, selected_piece: Piece, possible_moves_of_selected_piece: List[Tuple[int,int]],
                              special_moves: List[Tuple[int,int]]):

        if selected_piece is not None:
            self._coloring_board[selected_piece.y, selected_piece.x] = self.SELECTED_PIECE_SYMBOL

            possible_moves = possible_moves_of_selected_piece
            if possible_moves is not None:
                for move in possible_moves:
                    self._coloring_board[move[1], move[0]] = self.NORMAL_MOVE_SYMBOL

        if special_moves is not None:
            for move in special_moves:
                self._coloring_board[move[1], move[0]] = self.SPECIAL_MOVE_SYMBOL

    def reset_piece_board(self):
        self._piece_board.fill(0)

    def update_piece_board(self, white_player_pieces: List[Piece], black_player_pieces: List[Piece]) -> None:
        # Update the board with the current piece positions
        for piece in white_player_pieces:
            self._piece_board[piece.y][piece.x] = piece.type.value * piece.color.value

        for piece in black_player_pieces:
            self._piece_board[piece.y][piece.x] = piece.type.value * piece.color.value

    def reset_attack_boards(self):
        self._white_attack_board.fill(False)
        self._black_attack_board.fill(False)

    def update_attack_boards(self, attacked_by_white: List[Tuple[int, int]],
                             attacked_by_black: List[Tuple[int, int]]) -> None:
        for location in attacked_by_white:
            self._white_attack_board[location[0], location[1]] = True

        for location in attacked_by_black:
            self._black_attack_board[location[0], location[1]] = True

    def reset_protection_boards(self):
        self._white_protection_board.fill(False)
        self._black_protection_board.fill(False)

    def update_protection_boards(self, protected_by_white: List[Tuple[int, int]],
                                 protected_by_black: List[Tuple[int, int]]) -> None:

        for location in protected_by_white:
            self._white_protection_board[location[1], location[0]] = True

        for location in protected_by_black:
            self._black_protection_board[location[1], location[0]] = True

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

    def get_opponent_attack_board(self, color):
        if color == 1:
            return self._black_attack_board
        else:
            return self._white_attack_board

    def get_opponent_protection_board(self, color):
        if color == 1:
            return self._black_protection_board
        else:
            return self._white_protection_board

    def get_black_protection_board(self):
        return self._black_protection_board

    def get_white_protection_board(self):
        return self._white_protection_board



