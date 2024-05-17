import random
from typing import Tuple, Optional, List

from src.model.enums.Color import Color
from src.model.pieces.Piece import Piece
from src.model.players.Player import Player


class RandomPlayer(Player):
    def __init__(self, name: str, color: Color, board, time: int):
        super().__init__(name, color, board, time)

    def choose_move(self, opponent) -> Optional[Piece]:
        movable_pieces = self.get_movable_pieces()
        if len(movable_pieces) == 0:
            return None
        self.selected_piece = random.choice(movable_pieces)
        return random.choice(list(self.selected_piece.possible_fields))

    def get_movable_pieces(self) -> List[Piece]:
        return [piece for piece in self._pieces if piece.is_movable()]