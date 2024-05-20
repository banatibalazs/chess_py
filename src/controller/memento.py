import hashlib
from typing import List, Dict, Any, Tuple

from src.model.enums.color import Color
from src.model.pieces.pawn import Pawn
from src.model.players.player import Player


class Memento:
    def __init__(self, current_player: Player, opponent: Player) -> None:
        self.current_player_pieces: List[Dict[str, Any]] = self._get_pieces_info(current_player)
        self.opponent_pieces: List[Dict[str, Any]] = self._get_pieces_info(opponent)
        self.current_player_color: Color = current_player.color
        self.opponent_color: Color = opponent.color
        self.opponent_last_move: Tuple[int, int, int, int] = opponent.last_move

    def _get_pieces_info(self, player) -> List[Dict[str, Any]]:
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

    def get_hashed_state(self) -> str:
        game_state = ''

        # Add information about each piece to the game state string
        for player_pieces in [self.current_player_pieces, self.opponent_pieces]:
            for piece in player_pieces:
                game_state += str(piece['coordinates'])
                game_state += str(piece['type'])
                game_state += str(piece['color'])
                game_state += str(piece['is_moved'])
                if 'is_en_passant' in piece:
                    game_state += str(piece['is_en_passant'])

        # Add information about the current player's color to the game state string
        game_state += str(self.current_player_color)

        # Add information about the opponent's last move to the game state string
        game_state += str(self.opponent_last_move)

        # Generate a hash of the game state string
        game_state_hash = hashlib.sha256(game_state.encode()).hexdigest()

        return game_state_hash
