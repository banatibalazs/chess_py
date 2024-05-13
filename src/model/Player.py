from typing import Optional, List, Tuple, Set
from src.model.Bishop import Bishop
from src.model.Board import Board
from src.model.King import King
from src.model.Knight import Knight
from src.model.Pawn import Pawn
from src.model.Color import Color
from src.model.Piece import Piece
from src.model.PieceType import PieceType
from src.model.Queen import Queen
from src.model.Rook import Rook


class Player:

    def __init__(self, name: str, color: Color, board: Board) -> None:
        self._name: str = name
        self._color: Color = color
        self._board: Board = board
        self._is_computer: bool = False
        self._selected_piece: Optional[Piece] = None
        self._last_moved_piece: Optional[Piece] = None
        self._king: Optional[King] = None
        self._king_is_checked: bool = False
        self._last_move: Optional[Tuple[int, int, int, int]] = None

        self._pieces: List[Piece] = []
        self._attacked_fields: Set[Tuple[int, int]] = set()
        self._possible_fields: Set[Tuple[int, int]] = set()

    def init_pieces(self) -> None:
        color = self._color

        for i in range(8):
            self._pieces.append(Pawn(color, 6 if color == Color.WHITE else 1, i))

        self._pieces.append(Rook(color, 7 if color == Color.WHITE else 0, 0))
        self._pieces.append(Knight(color, 7 if color == Color.WHITE else 0, 1))
        self._pieces.append(Bishop(color, 7 if color == Color.WHITE else 0, 2))
        self._pieces.append(Queen(color, 7 if color == Color.WHITE else 0, 3))

        self._king = King(color, 7 if color == Color.WHITE else 0, 4)
        self._pieces.append(self._king)

        self._pieces.append(Bishop(color, 7 if color == Color.WHITE else 0, 5))
        self._pieces.append(Knight(color, 7 if color == Color.WHITE else 0, 6))
        self._pieces.append(Rook(color, 7 if color == Color.WHITE else 0, 7))

    def update_pieces_attacked_fields(self, opponent: 'Player') -> None:
        self._attacked_fields.clear()
        for piece in self._pieces:
            if piece.type == PieceType.KING:
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

    def get_piece_at(self, row: int, col: int) -> Optional[Piece]:
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

    def has_piece_at(self, row: int, col: int) -> bool:
        for piece in self._pieces:
            if piece.coordinates == (row, col):
                return True
        return False

    def is_selected_piece_at(self, row: int, col: int) -> bool:
        if self._selected_piece is not None:
            return self._selected_piece.coordinates == (row, col)
        return False

    def is_possible_move(self, row: int, col: int) -> bool:
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
    def selected_piece(self, piece: Optional[Piece]) -> None:
        self._selected_piece = piece

    @property
    def king(self) -> Optional[Piece]:
        return self._king

    @property
    def color(self) -> Color:
        return self._color

    def add_piece(self, piece: Piece) -> None:
        self._pieces.append(piece)

    @property
    def last_move(self) -> Tuple[int, int, int, int]:
        return self._last_move

    @last_move.setter
    def last_move(self, move: Tuple[int, int, int, int]) -> None:
        self._last_move = move

    def move_piece(self, to_row: int, to_col: int) -> None:
        from_row, from_col = self.selected_piece.coordinates
        self.last_move = (from_row, from_col, to_row, to_col)
        self.selected_piece.coordinates = (to_row, to_col)
        self.selected_piece.is_moved = True
        self._last_moved_piece = self.selected_piece
        # self.selected_piece.update_attacked_fields(self, self._opponent_player)
