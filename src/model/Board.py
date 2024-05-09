from typing import List

from src.controller.CustomTypesForTypeHinting import ByteArray8x8, CharArray8x8, BoolArray8x8
import numpy as np

from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece


class Board:

    NORMAL_MOVE_SYMBOL = 'n'
    SPECIAL_MOVE_SYMBOL = 's'
    SELECTED_PIECE_SYMBOL = 'x'
    EMPTY_SYMBOL = 'o'

    def __init__(self):
        self._piece_board: ByteArray8x8 = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board: CharArray8x8 = np.zeros((8, 8), dtype=np.str_)
        self._white_attack_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)
        self._black_attack_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)
        self._white_protection_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)
        self._black_protection_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)

    # def reset_coloring_board(self):
    #     self._coloring_board.fill(self.EMPTY_SYMBOL)

    def update_coloring_board(self, selected_piece: Piece):
        self._coloring_board.fill(self.EMPTY_SYMBOL)
        if selected_piece is not None:
            self._coloring_board[selected_piece.row, selected_piece.col] = self.SELECTED_PIECE_SYMBOL

            possible_moves = selected_piece.possible_fields
            if possible_moves is not None:
                for move in possible_moves:
                    self._coloring_board[move[0], move[1]] = self.NORMAL_MOVE_SYMBOL

            # if special_moves is not None:
            #     # print("Special moves: ", special_moves)
            #     for move in special_moves:
            #         self._coloring_board[move[0], move[1]] = self.SPECIAL_MOVE_SYMBOL

    # def reset_piece_board(self):
    #     self._piece_board.fill(0)

    def update_piece_board(self, white_player_pieces: List[Piece], black_player_pieces: List[Piece]) -> None:
        # Update the board with the current piece positions
        self._piece_board.fill(0)
        for piece in white_player_pieces:
            self._piece_board[piece.row][piece.col] = piece.type.value * piece.color.value

        for piece in black_player_pieces:
            self._piece_board[piece.row][piece.col] = piece.type.value * piece.color.value

    # def reset_attack_boards(self):
    #     self._white_attack_board.fill(False)
    #     self._black_attack_board.fill(False)

    def update_attack_boards(self, current_player, opponent) -> None:

        self._white_attack_board.fill(False)
        self._black_attack_board.fill(False)

        if current_player.color == ColorEnum.WHITE:
            white_selected_piece = current_player.selected_piece
            black_selected_piece = opponent.selected_piece
        else:
            white_selected_piece = opponent.selected_piece
            black_selected_piece = current_player.selected_piece

        if white_selected_piece is not None:
            if white_selected_piece._attacked_fields is not None:
                for field in white_selected_piece._attacked_fields:
                    self._white_attack_board[field[0], field[1]] = True

        if black_selected_piece is not None:
            if black_selected_piece._attacked_fields is not None:
                for field in black_selected_piece._attacked_fields:
                    self._black_attack_board[field[0], field[1]] = True


    def update_protection_boards(self, current_player, opponent) -> None:

        self._white_protection_board.fill(False)
        self._black_protection_board.fill(False)

        if current_player.color == ColorEnum.WHITE:
            white_selected_piece = current_player.selected_piece
            black_selected_piece = opponent.selected_piece
        else:
            white_selected_piece = opponent.selected_piece
            black_selected_piece = current_player.selected_piece


        if white_selected_piece is not None:
            if white_selected_piece.possible_fields is not None:
                for field in white_selected_piece.possible_fields:
                    self._white_protection_board[field[0], field[1]] = True

        if black_selected_piece is not None:
            if black_selected_piece.possible_fields is not None:
                for field in black_selected_piece.possible_fields:
                    self._black_protection_board[field[0], field[1]] = True

    def is_normal_move_at(self, row, col):
        return self._coloring_board[row, col] == self.NORMAL_MOVE_SYMBOL

    def is_special_move_at(self, row, col):
        return self._coloring_board[row, col] == self.SPECIAL_MOVE_SYMBOL

    def is_empty_at(self, row: int, col: int) -> bool:
        return self._piece_board[row][col] == 0

    def square_is_attacked_by_white(self, row, col) -> bool:
        return bool(self._white_attack_board[row, col])

    def square_is_attacked_by_black(self, row, col) -> bool:
        return bool(self._black_attack_board[row, col])

    def get_coloring_board(self) -> CharArray8x8:
        return self._coloring_board

    def get_piece_board(self) -> ByteArray8x8:
        return self._piece_board

    def is_selected_piece_at(self, row: int, col: int) -> bool:
        return self._coloring_board[row, col] == self.SELECTED_PIECE_SYMBOL

    def get_black_attack_board(self):
        return self._black_attack_board

    def get_white_attack_board(self):
        return self._white_attack_board

    def get_black_protection_board(self):
        return self._black_protection_board

    def get_white_protection_board(self):
        return self._white_protection_board

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
