from typing import Optional, List, Tuple, Set
from src.model.Bishop import Bishop
from src.model.Board import Board
from src.model.King import King
from src.model.Knight import Knight
from src.model.Pawn import Pawn
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum
from src.model.Queen import Queen
from src.model.Rook import Rook


class Player:

    def __init__(self, name: str, color: ColorEnum, board: Board):
        self._name: str = name
        self._color: ColorEnum = color
        self._board: Board = board
        self._is_computer: bool = False
        self._selected_piece: Optional[Piece] = None
        self._last_moved_piece: Optional[Piece] = None
        self._king = None
        self._king_is_checked: bool = False

        self._pieces: List[Piece] = []
        self._attacked_fields: Set[Tuple[int, int]] = set()
        self._possible_fields: Set[Tuple[int, int]] = set()

    def init_pieces(self):
        color = self._color
        # Append pawns
        for i in range(8):
            self._pieces.append(Pawn(color, 6 if color == ColorEnum.WHITE else 1, i))

        self._pieces.append(Rook(color, 7 if color == ColorEnum.WHITE else 0, 0))
        self._pieces.append(Knight(color, 7 if color == ColorEnum.WHITE else 0, 1))
        self._pieces.append(Bishop(color, 7 if color == ColorEnum.WHITE else 0, 2))
        self._pieces.append(Queen(color, 7 if color == ColorEnum.WHITE else 0, 3))

        self._king = King(color, 7 if color == ColorEnum.WHITE else 0, 4)
        self._pieces.append(self._king)

        self._pieces.append(Bishop(color, 7 if color == ColorEnum.WHITE else 0, 5))
        self._pieces.append(Knight(color, 7 if color == ColorEnum.WHITE else 0, 6))
        self._pieces.append(Rook(color, 7 if color == ColorEnum.WHITE else 0, 7))

    def update_pieces_attacked_fields(self, opponent):
        # print("Attacked fields are updated.")
        self._attacked_fields.clear()
        for piece in self._pieces:
            if piece.type == PieceTypeEnum.KING:
                pass
            piece.update_attacked_fields(self, opponent)
            for field in piece.attacked_fields:
                self._attacked_fields.add(field)

    def reset_en_passant(self) -> None:
        if self._last_moved_piece is not None:
            self._last_moved_piece.is_en_passant = False

    def remove_piece_at(self, row: int, col: int) -> None:
        for piece in self._pieces:
            if piece.coordinates == (row, col):
                self._pieces.remove(piece)
                break

    def get_piece_at(self, row, col) -> Optional[Piece]:
        for piece in self._pieces:
            if piece.coordinates == (row, col):
                return piece
        return None

    def get_score(self) -> int:
        score = 0
        for piece in self._pieces:
            score += piece.value
        return score

    @property
    def pieces(self) -> List[Piece]:
        return self._pieces

    @property
    def last_moved_piece(self) -> Piece:
        return self._last_moved_piece

    @last_moved_piece.setter
    def last_moved_piece(self, piece: Piece) -> None:
        self._last_moved_piece = piece

    def has_piece_at(self, row, col) -> bool:
        for piece in self._pieces:
            if piece.coordinates == (row, col):
                return True

    def is_selected_piece_at(self, row, col) -> bool:
        if self._selected_piece is not None:
            return self._selected_piece.coordinates == (row, col)

    def is_possible_move(self, row, col) -> bool:
        if self._selected_piece is None:
            return False
        return (row, col) in self._selected_piece.possible_fields

    def set_selected_piece(self, row: int, col: int) -> None:
        if self.has_piece_at(row, col):
            self._selected_piece = self.get_piece_at(row, col)

    @property
    def selected_piece(self) -> Piece:
        return self._selected_piece

    @selected_piece.setter
    def selected_piece(self, piece: Piece) -> None:
        self._selected_piece = piece

    @property
    def king(self) -> Optional[Piece]:
        return self._king

    @property
    def color(self) -> ColorEnum:
        return self._color

    def add_piece(self, piece: Piece) -> None:
        self._pieces.append(piece)

