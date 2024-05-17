from typing import List, Dict

from src.controller.Memento import Memento
from src.model.pieces.Bishop import Bishop
from src.model.pieces.King import King
from src.model.pieces.Knight import Knight
from src.model.pieces.Pawn import Pawn
from src.model.enums.PieceType import PieceType
from src.model.players.Player import Player
from src.model.pieces.Queen import Queen
from src.model.pieces.Rook import Rook


class GameSaver:
    def __init__(self) -> None:
        self._memento_list: List[Memento] = []
        self._memento_index = 0
        self._hashed_states: Dict[str, int] = dict()
        self.is_threefold_repetition = False

    def is_current_state(self) -> bool:
        return self._memento_index == len(self._memento_list) - 1

    def current_state_index(self) -> int:
        return self._memento_index

    def total_states(self) -> int:
        return len(self._memento_list) - 1

    def save_game(self, current_player, opponent) -> None:
        memento = Memento(current_player, opponent)

        hashed_state = memento.get_hashed_state()
        if hashed_state not in self._hashed_states:
            self._hashed_states[hashed_state] = 1
        else:
            self._hashed_states[hashed_state] += 1
            if self._hashed_states[hashed_state] == 3:
                self.is_threefold_repetition = True

        self._memento_list.append(memento)
        self._memento_index = len(self._memento_list) - 1

    def load_previous_state(self, current_player: Player, opponent: Player):
        if self._memento_index > 0:
            self._memento_index -= 1
            self._load_state(current_player, opponent, self._memento_list[self._memento_index])

    def load_next_state(self, current_player: Player, opponent: Player):
        if self._memento_index < len(self._memento_list) - 1:
            self._memento_index += 1
            self._load_state(current_player, opponent, self._memento_list[self._memento_index])

    def _load_state(self, current_player: Player, opponent: Player, memento: Memento):
        current_player.pieces.clear()
        current_player.color = memento.current_player_color
        opponent.color = memento.opponent_color
        opponent.pieces.clear()

        for piece in memento.current_player_pieces:
            row, col = piece["coordinates"]
            color = piece["color"]
            _type = piece["type"]
            is_en_passant = piece.get("is_en_passant", False)
            new_piece = self.create_piece(_type, color, row, col, is_en_passant)
            new_piece.is_moved = piece["is_moved"]
            current_player.add_piece(new_piece)

        for piece in memento.opponent_pieces:
            row, col = piece["coordinates"]
            color = piece["color"]
            _type = piece["type"]
            is_en_passant = piece.get("is_en_passant", False)
            new_piece = self.create_piece(_type, color, row, col, is_en_passant)
            new_piece.is_moved = piece["is_moved"]
            opponent.add_piece(new_piece)

        opponent.last_move = memento.opponent_last_move

    def create_piece(self, piece_type, color, row, col, is_en_passant=False):
        if piece_type == PieceType.PAWN:
            new_piece = Pawn(color, row, col)
            new_piece.is_en_passant = is_en_passant
        elif piece_type == PieceType.KNIGHT:
            new_piece = Knight(color, row, col)
        elif piece_type == PieceType.BISHOP:
            new_piece = Bishop(color, row, col)
        elif piece_type == PieceType.ROOK:
            new_piece = Rook(color, row, col)
        elif piece_type == PieceType.QUEEN:
            new_piece = Queen(color, row, col)
        elif piece_type == PieceType.KING:
            new_piece = King(color, row, col)
        else:
            raise ValueError("Invalid piece type.")
        return new_piece