from typing import List

from src.controller.CustomTypesForTypeHinting import ByteArray8x8, CharArray8x8, BoolArray8x8
import numpy as np
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece


class Board:

    NORMAL_MOVE_SYMBOL = 'n'
    SELECTED_PIECE_SYMBOL = 'x'
    EMPTY_SYMBOL = 'o'

    def __init__(self):
        self._piece_board: ByteArray8x8 = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board: CharArray8x8 = np.zeros((8, 8), dtype=np.str_)
        self._white_attack_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)
        self._black_attack_board: BoolArray8x8 = np.zeros((8, 8), dtype=np.bool_)

    def update(self, current_player, opponent):
        self.update_piece_board( current_player, opponent)
        self.update_coloring_board(current_player.selected_piece)
        self.update_attack_boards(current_player, opponent)

    def update_coloring_board(self, selected_piece: Piece) -> None:
        self._coloring_board.fill(self.EMPTY_SYMBOL)
        if selected_piece is not None:
            self._coloring_board[selected_piece.row, selected_piece.col] = self.SELECTED_PIECE_SYMBOL

            possible_moves = selected_piece.possible_fields
            if possible_moves is not None:
                for move in possible_moves:
                    self._coloring_board[move[0], move[1]] = self.NORMAL_MOVE_SYMBOL

    def update_piece_board(self, current_player, opponent) -> None:
        self._piece_board.fill(0)

        white_player_pieces = current_player.pieces if current_player.color == ColorEnum.WHITE else opponent.pieces
        black_player_pieces = opponent.pieces if current_player.color == ColorEnum.WHITE else current_player.pieces

        # Update the board with the current piece positions
        for piece in white_player_pieces:
            self._piece_board[piece.row][piece.col] = piece.type.value * piece.color.value

        for piece in black_player_pieces:
            self._piece_board[piece.row][piece.col] = piece.type.value * piece.color.value

    def update_attack_boards(self, current_player, opponent) -> None:

        self._white_attack_board.fill(False)
        self._black_attack_board.fill(False)

        white_selected_piece = current_player.selected_piece if current_player.color == ColorEnum.WHITE else opponent.selected_piece
        black_selected_piece = opponent.selected_piece if current_player.color == ColorEnum.WHITE else current_player.selected_piece

        for piece, board in [(white_selected_piece, self._white_attack_board),
                             (black_selected_piece, self._black_attack_board)]:
            if piece and piece._attacked_fields:
                for field in piece._attacked_fields:
                    board[field[0], field[1]] = True

    def is_normal_move_at(self, row: int, col: int) -> bool:
        return self._coloring_board[row, col] == self.NORMAL_MOVE_SYMBOL

    def is_empty_at(self, row: int, col: int) -> bool:
        return self._piece_board[row][col] == 0

    def get_coloring_board(self) -> CharArray8x8:
        return self._coloring_board

    def get_piece_board(self) -> ByteArray8x8:
        return self._piece_board

    def is_selected_piece_at(self, row: int, col: int) -> bool:
        return self._coloring_board[row, col] == self.SELECTED_PIECE_SYMBOL

    def get_black_attack_board(self) -> BoolArray8x8:
        return self._black_attack_board

    def get_white_attack_board(self) -> BoolArray8x8:
        return self._white_attack_board

    def get_opponent_attack_board(self, color: ColorEnum) -> BoolArray8x8:
        if color == 1:
            return self._black_attack_board
        else:
            return self._white_attack_board

