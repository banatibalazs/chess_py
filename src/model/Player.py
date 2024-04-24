from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum
from src.model.ColorEnum import ColorEnum


class Player:
    def __init__(self, name, color):
        self._name = name
        self._color = color
        self._pieces = []

        # Append pawns
        for i in range(8):
            self._pieces.append(Piece(PieceTypeEnum.PAWN, color, 6 if color == ColorEnum.WHITE else 1, i))

        # Append other pieces
        piece_types = [PieceTypeEnum.ROOK, PieceTypeEnum.KNIGHT, PieceTypeEnum.BISHOP, PieceTypeEnum.QUEEN,
                       PieceTypeEnum.KING, PieceTypeEnum.BISHOP, PieceTypeEnum.KNIGHT, PieceTypeEnum.ROOK]

        for i, piece_type in enumerate(piece_types):
            self._pieces.append(Piece(piece_type, color, 7 if color == ColorEnum.WHITE else 0, i))

    def get_name(self):
        return self._name

    def get_color(self):
        return self._color

    def get_pieces(self):
        return self._pieces


    def __str__(self):
        return f"{self._name} ({self._color})"