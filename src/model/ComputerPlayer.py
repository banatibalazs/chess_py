import random
from typing import Tuple, Optional, List
from src.model.Piece import Piece
from src.model.Player import Player


class ComputerPlayer(Player):
    def __init__(self, name, color):
        super().__init__(name, color)

    def choose_move(self) -> Tuple[int, int]:
        return  random.choice(list(self.selected_piece.possible_fields))

    def select_piece(self) -> Optional[Piece]:
        movable_pieces = self.get_movable_pieces()
        if len(movable_pieces) == 0:
            return None
        self.selected_piece = random.choice(movable_pieces)

    def get_movable_pieces(self) -> List[Piece]:
        movable_pieces = []
        for piece in self._pieces:
            if piece.is_movable():
                movable_pieces.append(piece)
        return movable_pieces