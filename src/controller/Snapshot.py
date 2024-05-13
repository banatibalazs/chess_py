from src.model.Bishop import Bishop
from src.model.King import King
from src.model.Knight import Knight
from src.model.Pawn import Pawn
from src.model.PieceType import PieceType
from src.model.Player import Player
from src.model.Queen import Queen
from src.model.Rook import Rook


class Snapshot:
    def __init__(self, current_player: Player, opponent: Player):
        self.current_player_pieces = self._get_pieces_info(current_player)
        self.opponent_pieces = self._get_pieces_info(opponent)
        self.current_player_color = current_player.color
        self.opponent_color = opponent.color
        self.opponent_last_move = opponent.last_move

    def _get_pieces_info(self, player):
        pieces_info = []
        for piece in player.pieces:
            piece_info = {
                'coordinates': piece.coordinates,
                'type': piece.type,
                'color': piece._color,
                'is_moved': piece.is_moved
            }
            if isinstance(piece, Pawn):
                piece_info['is_en_passant'] = piece.is_en_passant
            pieces_info.append(piece_info)
        return pieces_info

    def load_players(self, current_player: Player, opponent: Player):
        current_player.pieces.clear()
        opponent.pieces.clear()

        for piece in self.current_player_pieces:
            row, col = piece["coordinates"]
            color = piece["color"]
            _type = piece["type"]
            is_en_passant = piece.get("is_en_passant", False)
            new_piece = self.create_piece(_type, color, row, col, is_en_passant)
            new_piece.is_moved = piece["is_moved"]
            current_player.add_piece(new_piece)

        for piece in self.opponent_pieces:
            row, col = piece["coordinates"]
            color = piece["color"]
            _type = piece["type"]
            is_en_passant = piece.get("is_en_passant", False)
            new_piece = self.create_piece(_type, color, row, col, is_en_passant)
            new_piece.is_moved = piece["is_moved"]
            opponent.add_piece(new_piece)

        opponent.last_move = self.opponent_last_move

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
