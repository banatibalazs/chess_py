from typing import List

from src.controller.CustomTypesForTypeHinting import ByteArray8x8, CharArray8x8
import numpy as np
from src.model.pieces.Piece import Piece


class Board:

    NORMAL_MOVE_SYMBOL = 'n'
    SELECTED_PIECE_SYMBOL = 'x'
    EMPTY_SYMBOL = 'o'

    def __init__(self) -> None:
        self._piece_board: ByteArray8x8 = np.zeros((8, 8), dtype=np.byte)
        self._coloring_board: CharArray8x8 = np.zeros((8, 8), dtype=np.str_)

    def update(self, current_player, opponent) -> None:
        self.update_piece_board(current_player, opponent)
        self.update_coloring_board(current_player.selected_piece)

    def update_coloring_board(self, selected_piece: Piece) -> None:
        self._coloring_board.fill(self.EMPTY_SYMBOL)
        if selected_piece is not None:
            self._coloring_board[selected_piece.row, selected_piece.col] = self.SELECTED_PIECE_SYMBOL

            possible_moves = selected_piece.possible_fields
            if possible_moves is not None:
                for move in possible_moves:
                    self._coloring_board[move[0], move[1]] = self.NORMAL_MOVE_SYMBOL

    def update_piece_board(self, current_player_pieces: List[Piece], opponent_pieces: List[Piece]) -> None:
        self._piece_board.fill(0)
        # Update the board with the current piece positions
        for piece in current_player_pieces:
            self._piece_board[piece.row][piece.col] = piece.type.value * piece.color.value

        for piece in opponent_pieces:
            self._piece_board[piece.row][piece.col] = piece.type.value * piece.color.value

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

