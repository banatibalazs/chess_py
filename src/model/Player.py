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
    """
    Important methods:

        1. init_pieces (called in the constructor)
        ----------------
        3. update_pieces_data
        4. update_possible_moves_of_selected_piece
        ----------------
        5. get_special_moves
        7. add_en_passant_moves_to_special_moves
        8. is_castling_possible
        9. add_castling_moves_to_special_moves
        ----------------
        10. make_move
        11. is_promotion
        12. promote_pawn
        13. castling
        14. en_passant

    """

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
        self._special_moves: Set[Tuple[int, int]] = set()
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
        self._pieces.append(King(color, 7 if color == ColorEnum.WHITE else 0, 4))
        self._pieces.append(Bishop(color, 7 if color == ColorEnum.WHITE else 0, 5))
        self._pieces.append(Knight(color, 7 if color == ColorEnum.WHITE else 0, 6))
        self._pieces.append(Rook(color, 7 if color == ColorEnum.WHITE else 0, 7))

        self._king = self.get_king()

    def update_pieces_attacked_fields(self, opponent):
        # print("Attacked fields are updated.")
        self._attacked_fields.clear()
        for piece in self._pieces:
            if piece.type == PieceTypeEnum.KING:
                pass
            piece.update_attacked_fields(self, opponent)
            for field in piece.attacked_fields:
                self._attacked_fields.add(field)

    def update_pieces_possible_fields(self, opponent):
        self._possible_fields.clear()
        # self._possible_fields = self._attacked_fields.copy()

    def attacks_field(self, row, col) -> bool:
        return (row, col) in self._attacked_fields

    def update_special_moves(self, opponent_player_last_moved_piece):
        # Reset special moves before adding new ones
        self._special_moves.clear()
        # Add special moves
        if isinstance(self._selected_piece, Pawn):
            self.add_en_passant_moves_to_special_moves(opponent_player_last_moved_piece)
        if isinstance(self._selected_piece, King):
            self.add_castling_moves_to_special_moves()

    def add_en_passant_moves_to_special_moves(self, op_last_moved_piece) -> None:
        if op_last_moved_piece is not None and \
                isinstance(op_last_moved_piece, Pawn) and \
                op_last_moved_piece.is_en_passant and \
                self._selected_piece is not None and \
                self._selected_piece.row == op_last_moved_piece.row and \
                abs(self._selected_piece.col - op_last_moved_piece.col) == 1:
            if self._color == ColorEnum.WHITE:
                print("En passant move is added.")
                self._special_moves.add((op_last_moved_piece.row - 1, op_last_moved_piece.col))
            else:
                self._special_moves.add((op_last_moved_piece.row + 1, op_last_moved_piece.col))

    def add_castling_moves_to_special_moves(self) -> None:
        # Rooks coordinates are (0, 0), (7, 0), (0, 7), (7, 7) for white and black respectively
        if self._color == ColorEnum.BLACK:
            if self.is_castling_possible(self.get_piece_at(0, 0), range(1, 4)):
                self._special_moves.add((0, 2))
            if self.is_castling_possible(self.get_piece_at(0, 7), range(5, 7)):
                self._special_moves.add((0, 6))
        else:
            if self.is_castling_possible(self.get_piece_at(7, 0), range(1, 4)):
                self._special_moves.add((7, 2))
            if self.is_castling_possible(self.get_piece_at(7, 7), range(5, 7)):
                self._special_moves.add((7, 6))

    def is_castling_possible(self, rook, cols):
        return (isinstance(rook, Rook) and
                not rook.is_moved and
                not self._king.is_moved and
                all(self._board.is_empty_at(self._king.row, col) for col in cols) and
                not any(self._board.get_opponent_attack_board(self._color)[self._king.row, col] for col in cols))

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
    def special_moves(self) -> Set[Tuple[int, int]]:
        return self._special_moves

    @property
    def pieces(self) -> List[Piece]:
        return self._pieces

    @property
    def last_moved_piece(self):
        return self._last_moved_piece

    @last_moved_piece.setter
    def last_moved_piece(self, piece: Piece) -> None:
        self._last_moved_piece = piece

    def has_piece_at(self, row, col) -> bool:
        for piece in self._pieces:
            if piece.coordinates == (row, col):
                return True

    def is_selected_piece_at(self, row, col):
        if self._selected_piece is not None:
            return self._selected_piece.coordinates == (row, col)

    def is_possible_move(self, row, col):
        if self._selected_piece is None:
            return False
        # print(f"Possible moves: {self._selected_piece.possible_fields}")
        return (row, col) in self._special_moves or (row, col) in self._selected_piece.possible_fields


    def set_selected_piece(self, row: int, col: int) -> None:
        if self.has_piece_at(row, col):
            self._selected_piece = self.get_piece_at(row, col)

    @property
    def selected_piece(self):
        return self._selected_piece

    @selected_piece.setter
    def selected_piece(self, piece: Piece) -> None:
        self._selected_piece = piece

    def get_king(self):
        for piece in self._pieces:
            if piece.type == PieceTypeEnum.KING:
                return piece
        return None

    @property
    def color(self):
        return self._color

    def add_piece(self, piece: Piece) -> None:
        self._pieces.append(piece)
