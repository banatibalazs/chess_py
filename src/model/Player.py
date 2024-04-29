from typing import Optional, List, Tuple, Set
import src.model.Board as Board
from src.controller.CustomTypesForTypeHinting import ByteArray8x8
from src.model.Bishop import Bishop
from src.model.King import King
from src.model.Knight import Knight
from src.model.Pawn import Pawn
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum
from src.model.Queen import Queen
from src.model.Rook import Rook


class Player:
    def __init__(self, name: str, color: ColorEnum):
        self._name: str = name
        self._color: ColorEnum = color
        self._is_computer: bool = False
        self._selected_piece: Optional[Piece] = None
        self._last_moved_piece: Optional[Piece] = None
        self._king_is_checked: bool = False

        self._pieces: List[Piece] = []
        self._possible_moves: List[Tuple[int, int]] = []
        self._protected_fields: List[Tuple[int, int]] = []
        self._special_moves: List[Tuple[int, int]] = []
        self._attacked_squares: List[Tuple[int, int]] = []

        # Append pawns
        for i in range(8):
            self._pieces.append(Pawn(color, i, 6 if color == ColorEnum.WHITE else 1))

        self._pieces.append(Rook(color, 0, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Knight(color, 1, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Bishop(color, 2, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Queen(color, 3, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(King(color, 4, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Bishop(color, 5, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Knight(color, 6, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Rook(color, 7, 7 if color == ColorEnum.WHITE else 0))

        self._piece_coordinates: Set[Tuple[int, int]] = set((piece.x, piece.y) for piece in self._pieces)


    def is_computer(self) -> bool:
        return self._is_computer

    def get_name(self) -> str:
        return self._name

    def get_color(self) -> ColorEnum:
        return self._color

    @property
    def pieces(self) -> List[Piece]:
        return self._pieces

    def get_piece_at(self, x, y) -> Optional[Piece]:
        for piece in self._pieces:
            if piece.coordinates == (x, y):
                return piece
        return None

    def has_piece_at(self, x, y) -> bool:
        return (x, y) in self._piece_coordinates

    def is_selected_piece_at(self, x, y):
        if self.selected_piece is not None:
            return self.selected_piece.coordinates == (x, y)

    def is_possible_normal_move(self, x, y):
        return (x, y) in self._possible_moves

    def is_possible_special_move(self, x, y):
        return (x, y) in self.special_moves

    def __str__(self):
        return f"{self._name} ({self._color})"

    def update_normal_moves(self, board: ByteArray8x8):
        self._update_possible_moves_of_selected_piece(board)
        self._update_attacked_locations(board)
        self._update_protected_fields(board)
        self._piece_coordinates = set((piece.x, piece.y) for piece in self._pieces)

    def _update_possible_moves_of_selected_piece(self, board: ByteArray8x8):
        if self._selected_piece is not None:
            self._possible_moves, _ = self._selected_piece.get_possible_moves(board)

    @property
    def possible_moves_of_selected_piece(self) -> List[Tuple[int, int]]:
        # self._update_possible_moves_of_selected_piece(board)
        return self._possible_moves

    def _update_protected_fields(self, board: ByteArray8x8) -> None:
        self._protected_fields = [field for piece in self._pieces for field in piece.get_possible_moves(board)[1]]

    @property
    def protected_fields(self) -> List[Tuple[int, int]]:
        return self._protected_fields

    def _update_attacked_locations(self, board: ByteArray8x8) -> None:
        self._attacked_squares = []
        for piece in self._pieces:
            if isinstance(piece, Pawn):
                attacked_locations = piece.get_attacked_locations()
            else:
                attacked_locations, _ = piece.get_possible_moves(board)
            for location in attacked_locations:
                self._attacked_squares.append((location[1], location[0]))

    @property
    def attacked_fields(self) -> List[Tuple[int, int]]:
        return self._attacked_squares

    @property
    def special_moves(self) -> List[Tuple[int, int]]:
        return self._special_moves

    def reset_special_moves(self) -> None:
        self._special_moves = []

    def get_last_moved_piece(self):
        return self._last_moved_piece

    def update_en_passant(self, op_last_moved_piece) -> None:
        if op_last_moved_piece is not None and \
                isinstance(op_last_moved_piece, Pawn) and \
                op_last_moved_piece.is_en_passant and \
                self.selected_piece is not None and \
                self.selected_piece.y == op_last_moved_piece.y and \
                abs(self.selected_piece.x - op_last_moved_piece.x) == 1:
            if self._color == ColorEnum.WHITE:
                self._special_moves.append((op_last_moved_piece.x, op_last_moved_piece.y - 1))
            else:
                self._special_moves.append((op_last_moved_piece.x, op_last_moved_piece.y + 1))

    def update_castling(self, board: Board) -> None:
        if self._color == ColorEnum.BLACK:
            # Then king is at (4, 0) and rooks are at (0, 0) and (7, 0)
            king = self.get_piece_at(4, 0)
            rook = self.get_piece_at(0, 0)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved and
                    not king.is_moved and
                    board.is_empty_at(1, 0) and
                    board.is_empty_at(2, 0) and
                    board.is_empty_at(3, 0) and
                    not board.square_is_attacked_by_black(4, 0) and
                    not board.square_is_attacked_by_white(4, 0) and
                    not board.square_is_attacked_by_white(3, 0) and
                    not board.square_is_attacked_by_white(2, 0)):
                self._special_moves.append((2, 0))

            rook = self.get_piece_at(7, 0)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved and
                    not king.is_moved and
                    board.is_empty_at(5, 0) and
                    board.is_empty_at(6, 0) and
                    not board.square_is_attacked_by_black(4, 0) and
                    not board.square_is_attacked_by_white(4, 0) and
                    not board.square_is_attacked_by_white(5, 0) and
                    not board.square_is_attacked_by_white(6, 0)):
                self._special_moves.append((6, 0))

        else:
            king = self.get_piece_at(4, 7)
            rook = self.get_piece_at(0, 7)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved and
                    not king.is_moved and
                    board.is_empty_at(1, 7) and
                    board.is_empty_at(2, 7) and
                    board.is_empty_at(3, 7) and
                    not board.square_is_attacked_by_white(4, 7) and
                    not board.square_is_attacked_by_black(4, 7) and
                    not board.square_is_attacked_by_black(3, 7) and
                    not board.square_is_attacked_by_black(2, 7)):
                self._special_moves.append((2, 7))

            rook = self.get_piece_at(7, 7)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved and
                    not king.is_moved and
                    board.is_empty_at(5, 7) and
                    board.is_empty_at(6, 7) and
                    not board.square_is_attacked_by_white(4, 7) and
                    not board.square_is_attacked_by_black(4, 7) and
                    not board.square_is_attacked_by_black(5, 7) and
                    not board.square_is_attacked_by_black(6, 7)):
                self._special_moves.append((6, 7))

    def reset_selected_piece(self):
        self._selected_piece = None

    def set_selected_piece(self, x: int, y: int) -> None:
        if self.has_piece_at(x, y):
            self._selected_piece = self.get_piece_at(x, y)

    @property
    def selected_piece(self):
        return self._selected_piece

    def has_selected_piece(self) -> bool:
        return self._selected_piece is not None

    def remove_piece_at(self, x: int, y: int) -> None:
        for piece in self._pieces:
            if piece.coordinates == (x, y):
                self._pieces.remove(piece)
                break

    def get_king(self):
        for piece in self._pieces:
            if piece.type == PieceTypeEnum.KING:
                return piece
        return None

    def get_king_is_checked(self):
        return self._king_is_checked

    def set_king_is_checked(self, value):
        self._king_is_checked = value

    def attacks_position(self, x: int, y: int, board: ByteArray8x8):
        for piece in self._pieces:
            if (x, y) in piece.get_possible_moves(board):
                return True
        return False

    def get_piece_number(self):
        return len(self._pieces)

    def make_normal_move(self, to_x, to_y) -> None:
        print("Normal move.")
        # Set en passant field if the pawn moves two squares

        self.selected_piece.set_coordinates(to_x, to_y)
        self.selected_piece.is_moved = True
        self._last_moved_piece = self.selected_piece

    def reset_en_passant(self) -> None:
        for piece in self._pieces:
            if isinstance(piece, Pawn):
                piece.is_en_passant = False

    def promote_pawn(self, to_x: int, to_y: int, piece_type: PieceTypeEnum) -> None:
        print("Promoting pawn")
        from_x = self.selected_piece.x
        from_y = self.selected_piece.y

        self.remove_piece_at(from_x, from_y)
        if piece_type == PieceTypeEnum.QUEEN:
            self._pieces.append(Queen(self._color, to_x, to_y))
        elif piece_type == PieceTypeEnum.ROOK:
            self._pieces.append(Rook(self._color, to_x, to_y))
        elif piece_type == PieceTypeEnum.BISHOP:
            self._pieces.append(Bishop(self._color, to_x, to_y))
        elif piece_type == PieceTypeEnum.KNIGHT:
            self._pieces.append(Knight(self._color, to_x, to_y))
        else:
            raise ValueError("Invalid piece type.")
        self._last_moved_piece = None
        self.reset_en_passant()

    def castling(self, x: int, y: int):
        print("Castling")
        if x == 2:
            rook = self.get_piece_at(0, y)
            if rook is not None:
                rook.set_coordinates(3, y)
                rook.set_moved = True
        elif x == 6:
            rook = self.get_piece_at(7, y)
            if rook is not None:
                rook.set_coordinates(5, y)
                rook.set_moved = True

        king = self.get_king()
        if king is not None:
            king.set_coordinates(x, y)
            king.set_moved = True
        self._last_moved_piece = king
        self.reset_en_passant()

    def en_passant(self, to_x, to_y):
        self.selected_piece.set_coordinates(to_x, to_y)
        self.reset_en_passant()

    def get_score(self) -> int:
        score = 0
        for piece in self._pieces:
            score += piece.value
        return score
