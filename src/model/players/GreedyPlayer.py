from typing import List

from src.model.pieces.Piece import Piece
from src.model.players.Player import Player


class GreedyPlayer(Player):
    def __init__(self, name: str, color, board, time: int):
        super().__init__(name, color, board, time)

    def choose_move(self):
        max_value = -1000
        best_move = None
        for piece in self._pieces:
            if piece.is_movable():
                for field in piece.possible_fields:
                    if field.value > max_value:
                        max_value = field.value
                        best_move = (piece.row, piece.col, field.row, field.col)
        return best_move

    def select_piece(self):
        max_value = -1000
        best_piece = None
        for piece in self.get_movable_pieces():
            for field in piece.possible_fields:

                if field.value > max_value:
                    max_value = field.value
                    best_piece = piece
        self.selected_piece = best_piece
        return best_piece

    def get_movable_pieces(self) -> List[Piece]:
        movable_pieces = []
        for piece in self._pieces:
            if piece.is_movable():
                movable_pieces.append(piece)
        return movable_pieces