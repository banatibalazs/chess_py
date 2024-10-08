from typing import List

from src.model.enums.color import Color
from src.model.pieces.pawn import Pawn
from src.model.pieces.piece import Piece
from src.model.players.player import Player


class GreedyPlayer(Player):
    def __init__(self, name: str, color, board, time: int):
        super().__init__(name, color, board, time)
        self.selected_piece = None
        self.chosen_move = None

    def choose_move(self, opponent):
        max_value = -1000
        best_move = None
        for piece in self.get_movable_pieces():
            for move in piece.possible_fields:
                score = self.simulate_move(move, piece, opponent)
                if score > max_value:
                    max_value = score
                    self.selected_piece = piece
                    best_move = move
        return best_move

    def simulate_move(self, move, piece, opponent) -> int:
        score = 0
        color = self.color
        from_row, from_col = piece.coordinates
        to_row, to_col = move

        piece.coordinates = move

        captured_piece = None
        if opponent.has_piece_at(*move):
            captured_piece = opponent.get_piece_at(*move)
            opponent.remove_piece_at(*move)

        self.update_pieces_attacked_fields(opponent.piece_coordinates)

        # Attacking the opponent's king is rewarded
        if opponent.king.coordinates in self._attacked_fields:
            score += 3

        # Capture opponent's pieces is rewarded
        score += self.get_score() - opponent.get_score()

        # Getting closer to the enemy's side is beneficial
        if isinstance(piece, Pawn) and (
                (color == Color.WHITE and from_row > to_row) or (color != Color.WHITE and from_row < to_row)):
            score += 4

        score += int(3.5 - abs(3.5 - to_col))

        if captured_piece is not None:
            opponent.add_piece(captured_piece)

        piece.coordinates = (from_row, from_col)

        return score
