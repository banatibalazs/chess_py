import random
from typing import Optional, List, Tuple, Set
from src.model.Bishop import Bishop
from src.model.Board import Board
from src.model.King import King
from src.model.Knight import Knight
from src.model.Pawn import Pawn
from src.model.Color import Color
from src.model.Piece import Piece
from src.model.Queen import Queen
from src.model.Rook import Rook


class Player:

    def __init__(self, name: str, color: Color, board: Board, time: Optional[int]) -> None:
        self._name: str = name
        self._color: Color = color
        self._time: Optional[int] = time
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
            piece.update_attacked_fields(self, opponent)
            for field in piece.attacked_fields:
                self._attacked_fields.add(field)

    def update_pieces_possible_fields(self, opponent: 'Player') -> None:
        self._possible_fields.clear()
        for piece in self._pieces:
            piece.update_possible_fields(self, opponent)

    def reset_en_passant(self) -> None:
        if self._last_moved_piece is not None:
            if isinstance(self._last_moved_piece, Pawn):
                self._last_moved_piece.is_en_passant = False
                print("En passant reset.")

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

    def can_move(self) -> bool:
        for piece in self._pieces:
            if piece.is_movable():
                return True
        return False

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
    def time(self) -> int:
        return self._time

    @time.setter
    def time(self, time: int) -> None:
        self._time = time

    @property
    def name(self) -> str:
        return self._name

    @property
    def king(self) -> Optional[King]:
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
        self.selected_piece.coordinates = (to_row, to_col)
        self.selected_piece.is_moved = True
        self._last_moved_piece = self.selected_piece

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
