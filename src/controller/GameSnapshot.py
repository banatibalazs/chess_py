from src.model.Pawn import Pawn
from src.model.Player import Player


class GameSnapshot:
    def __init__(self, current_player, opponent):
        self.current_player_pieces = self._get_pieces_info(current_player)
        self.opponent_pieces = self._get_pieces_info(opponent)
        self.current_player_name = current_player.name
        self.opponent_name = opponent.name
        self.current_player_color = current_player.color
        self.opponent_color = opponent.color

    def _get_pieces_info(self, player):
        pieces_info = []
        for piece in player.pieces:
            piece_info = {
                'coordinates': piece.coordinates,
                'type': piece.type,
                'color': piece.color,
                'is_moved': piece.is_moved
            }
            if isinstance(piece, Pawn):
                piece_info['is_en_passant'] = piece.is_en_passant
            pieces_info.append(piece_info)
        return pieces_info

    def get_player(self):
        return Player()