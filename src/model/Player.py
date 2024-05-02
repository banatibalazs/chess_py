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
        6. update_protected_and_attacked_fields
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
        self._protected_fields: set[Tuple[int, int]] = set()
        self._special_moves: set[Tuple[int, int]] = set()
        self._attacked_fields: set[Tuple[int, int]] = set()

    def init_pieces(self):
        color = self._color
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

        self._king = self.get_king()


    def update_pieces_attacked_fields(self, opponent):
        for piece in self._pieces:
            piece.update_attacked_fields(self, opponent)

    def update_pieces_protected_fields(self):
        for piece in self._pieces:
            piece.update_protected_fields(self)

    def update_pieces_possible_fields(self, opponent):
        for piece in self._pieces:
            piece.update_possible_fields(self, opponent)

    def get_special_moves(self, opponent_player_last_moved_piece):
        # Reset special moves before adding new ones
        self._special_moves.clear()
        # Add special moves
        if isinstance(self._selected_piece, Pawn):
            self.add_en_passant_moves_to_special_moves(opponent_player_last_moved_piece)
        if isinstance(self._selected_piece, King):
            self.add_castling_moves_to_special_moves()

    def update_protected_and_attacked_fields(self) -> None:

        self._protected_fields.clear()
        self._attacked_fields.clear()

        for piece in self._pieces:
            self._protected_fields.update(piece.protected_fields)

            # The only exception is the pawn, as it moves forward but captures diagonally
            if isinstance(piece, Pawn):
                attacked_fields = piece.attacked_fields
                self._attacked_fields.update(attacked_fields)
            else:
                self._attacked_fields.update(piece.possible_fields)

    def add_en_passant_moves_to_special_moves(self, op_last_moved_piece) -> None:
        if op_last_moved_piece is not None and \
                isinstance(op_last_moved_piece, Pawn) and \
                op_last_moved_piece.is_en_passant and \
                self._selected_piece is not None and \
                self._selected_piece.y == op_last_moved_piece.y and \
                abs(self._selected_piece.x - op_last_moved_piece.x) == 1:
            if self._color == ColorEnum.WHITE:
                self._special_moves.add((op_last_moved_piece.x, op_last_moved_piece.y - 1))
            else:
                self._special_moves.add((op_last_moved_piece.x, op_last_moved_piece.y + 1))

    def is_castling_possible(self, rook, squares):
        return (isinstance(rook, Rook) and
                not rook.is_moved and
                not self._king.is_moved and
                all(self._board.is_empty_at(x, self._king.y) for x in squares) and
                not any(self._board.get_opponent_attack_board(self._color)[self._king.y, x] for x in squares))

    def add_castling_moves_to_special_moves(self) -> None:
        # Rooks coordinates are (0, 0), (7, 0), (0, 7), (7, 7) for white and black respectively
        if self._color == ColorEnum.BLACK:
            if self.is_castling_possible(self.get_piece_at(0, 0), range(1, 4)):
                self._special_moves.add((2, 0))
            if self.is_castling_possible(self.get_piece_at(7, 0), range(5, 7)):
                self._special_moves.add((6, 0))
        else:
            if self.is_castling_possible(self.get_piece_at(0, 7), range(1, 4)):
                self._special_moves.add((2, 7))
            if self.is_castling_possible(self.get_piece_at(7, 7), range(5, 7)):
                self._special_moves.add((6, 7))

    def make_move(self, to_x: int, to_y: int, opponent) -> None:
        if self._selected_piece is None:
            print("Eror: No piece is selected.")
        # Set en passant field if the pawn moves two squares
        self.reset_en_passant()
        self.set_en_passant(to_y)
        if self.is_promotion(to_x, to_y):
            self.promote_pawn(to_x, to_y, PieceTypeEnum.QUEEN)
        elif (to_x, to_y) in self._special_moves:
            if isinstance(self._selected_piece, King):
                self.castling(to_x, to_y)
            if isinstance(self._selected_piece, Pawn):
                self.en_passant(to_x, to_y, opponent)

        if opponent is not None and opponent.has_piece_at(to_x, to_y):
            opponent.remove_piece_at(to_x, to_y)
        self._selected_piece.coordinates = (to_x, to_y)
        self._selected_piece.is_moved = True
        self._last_moved_piece = self._selected_piece

    def is_promotion(self, to_x, to_y):
        return ((to_y == 0) or (to_y == 7)) and isinstance(self._selected_piece, Pawn)

    def reset_en_passant(self) -> None:
        if self._last_moved_piece is not None:
            self._last_moved_piece.is_en_passant = False

    def set_en_passant(self, to_y):
        # If the selected piece is a pawn and it moves two squares forward, set the en passant variable
        self.reset_en_passant()
        if isinstance(self._selected_piece, Pawn):
            if abs(self._selected_piece.y - to_y) == 2:
                print("En passant variable is set.")
                self._selected_piece.is_en_passant = True

    def promote_pawn(self, to_x: int, to_y: int, piece_type: PieceTypeEnum) -> None:
        print("Promoting pawn")
        from_x = self._selected_piece.x
        from_y = self._selected_piece.y
        new_piece = None
        self.remove_piece_at(from_x, from_y)
        if piece_type == PieceTypeEnum.QUEEN:
            new_piece = Queen(self._color, to_x, to_y)
        elif piece_type == PieceTypeEnum.ROOK:
            new_piece = Rook(self._color, to_x, to_y)
        elif piece_type == PieceTypeEnum.BISHOP:
            new_piece = Bishop(self._color, to_x, to_y)
        elif piece_type == PieceTypeEnum.KNIGHT:
            new_piece = Knight(self._color, to_x, to_y)
        else:
            raise ValueError("Invalid piece type.")
        self._pieces.append(new_piece)
        self._last_moved_piece = new_piece
        self.reset_en_passant()

    def castling(self, x: int, y: int):
        print("Castling")
        if x == 2:
            rook = self.get_piece_at(0, y)
            if rook is not None:
                rook.coordinates = (3, y)
                rook.set_moved = True
        elif x == 6:
            rook = self.get_piece_at(7, y)
            if rook is not None:
                rook.coordinates = (5, y)
                rook.set_moved = True

        king = self.get_king()
        if king is not None:
            king.coordinates = (x, y)
            king.set_moved = True
        self._last_moved_piece = king
        self.reset_en_passant()

    def en_passant(self, to_x, to_y, opponent):
        if self._color == ColorEnum.WHITE:
            opponent.remove_piece_at(to_x, to_y + 1)
        else:
            opponent.remove_piece_at(to_x, to_y - 1)
        self._selected_piece.coordinates = (to_x, to_y)
        self.reset_en_passant()

    def remove_piece_at(self, x: int, y: int) -> None:
        for piece in self._pieces:
            if piece.coordinates == (x, y):
                self._pieces.remove(piece)
                break

    def get_piece_at(self, x, y) -> Optional[Piece]:
        for piece in self._pieces:
            if piece.coordinates == (x, y):
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

    def has_piece_at(self, x, y) -> bool:
        for piece in self._pieces:
            if piece.x == x and piece.y == y:
                return True

    def is_selected_piece_at(self, x, y):
        if self._selected_piece is not None:
            return self._selected_piece.coordinates == (x, y)

    def is_possible_move(self, x, y):
        if self._selected_piece is None:
            return False
        # print(f"Possible moves: {self._selected_piece.possible_fields}")
        return (x, y) in self._special_moves or (x, y) in self._selected_piece.possible_fields


    @property
    def protected_fields(self) -> Set[Tuple[int, int]]:
        return self._protected_fields

    @property
    def attacked_fields(self) -> Set[Tuple[int, int]]:
        return self._attacked_fields

    @property
    def last_moved_piece(self):
        return self._last_moved_piece

    def set_selected_piece(self, x: int, y: int) -> None:
        if self.has_piece_at(x, y):
            self._selected_piece = self.get_piece_at(x, y)

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
