import random
from typing import Optional, List, Tuple, Set

from src.controller.CustomTypesForTypeHinting import ByteArray8x8
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
        self._king_is_checked: bool = False

        self._pieces: List[Piece] = []
        self._all_possible_move: set[Tuple[int, int]] = set()
        self._protected_fields: set[Tuple[int, int]] = set()
        self._special_moves: set[Tuple[int, int]] = set()
        self._attacked_fields: set[Tuple[int, int]] = set()
        self._piece_coordinates: Set[Tuple[int, int]] = set()

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

        self._piece_coordinates.update((piece.x, piece.y) for piece in self._pieces)

    def set_pieces(self, pieces: List[Piece]) -> None:
        self._pieces = pieces

    def update_piece_coordinates(self):
        self._piece_coordinates.clear()
        self._piece_coordinates.update((piece.x, piece.y) for piece in self._pieces)

    def update_pieces_data(self):
        for piece in self._pieces:
            piece.update_piece(self._board)
        self.update_piece_coordinates()

    def update_possible_moves_of_selected_piece(self, board: Board):
        # 1. Update possible moves of selected piece
        if self._selected_piece is not None:
            # If the selected piece is a king, the possible moves need to be filtered
            # so that the king does not move into an attacked field
            # This is handled in the get_possible_moves_of_piece method
            self._selected_piece.update_piece(board)

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

        # return piece.get_possible_moves(self._board)
    # def choose_step(self) -> Optional[Tuple[int, int]]:
    #
    #     # Check if there are any possible moves
    #     if not self._possible_moves_of_selected_piece:
    #         return None
    #     # Select a random move
    #     chosen_move = random.choice(list(self._selected_piece.possible_fields))
    #     print(f"Chosen move: {chosen_move}")
    #     return chosen_move
    #
    # def choose_movable_piece(self):
    #     movable_pieces = self.get_movable_pieces()
    #     if len(movable_pieces) == 0:
    #         return None
    #     self._selected_piece = random.choice(movable_pieces)
    #     return self._selected_piece
    #
    # def get_movable_pieces(self):
    #     movable_pieces = []
    #     for piece in self._pieces:
    #         moves = piece.update_piece(self._board)[0]
    #         if moves != [] and moves is not None:
    #             movable_pieces.append(piece)
    #     return movable_pieces

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

    def add_castling_moves_to_special_moves(self) -> None:
        if self._color == ColorEnum.BLACK:
            # Then king is at (4, 0) and rooks are at (0, 0) and (7, 0)
            king = self.get_piece_at(4, 0)
            rook = self.get_piece_at(0, 0)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved and
                    not king.is_moved and
                    self._board.is_empty_at(1, 0) and
                    self._board.is_empty_at(2, 0) and
                    self._board.is_empty_at(3, 0) and
                    not self._board.square_is_attacked_by_black(4, 0) and
                    not self._board.square_is_attacked_by_white(4, 0) and
                    not self._board.square_is_attacked_by_white(3, 0) and
                    not self._board.square_is_attacked_by_white(2, 0)):
                self._special_moves.add((2, 0))

            rook = self.get_piece_at(7, 0)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved and
                    not king.is_moved and
                    self._board.is_empty_at(5, 0) and
                    self._board.is_empty_at(6, 0) and
                    not self._board.square_is_attacked_by_black(4, 0) and
                    not self._board.square_is_attacked_by_white(4, 0) and
                    not self._board.square_is_attacked_by_white(5, 0) and
                    not self._board.square_is_attacked_by_white(6, 0)):
                self._special_moves.add((6, 0))

        else:
            king = self.get_piece_at(4, 7)
            rook = self.get_piece_at(0, 7)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved and
                    not king.is_moved and
                    self._board.is_empty_at(1, 7) and
                    self._board.is_empty_at(2, 7) and
                    self._board.is_empty_at(3, 7) and
                    not self._board.square_is_attacked_by_white(4, 7) and
                    not self._board.square_is_attacked_by_black(4, 7) and
                    not self._board.square_is_attacked_by_black(3, 7) and
                    not self._board.square_is_attacked_by_black(2, 7)):
                self._special_moves.add((2, 7))

            rook = self.get_piece_at(7, 7)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved and
                    not king.is_moved and
                    self._board.is_empty_at(5, 7) and
                    self._board.is_empty_at(6, 7) and
                    not self._board.square_is_attacked_by_white(4, 7) and
                    not self._board.square_is_attacked_by_black(4, 7) and
                    not self._board.square_is_attacked_by_black(5, 7) and
                    not self._board.square_is_attacked_by_black(6, 7)):
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
        self._selected_piece.set_coordinates(to_x, to_y)
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

    def en_passant(self, to_x, to_y, opponent):
        if self._color == ColorEnum.WHITE:
            opponent.remove_piece_at(to_x, to_y + 1)
        else:
            opponent.remove_piece_at(to_x, to_y - 1)
        self._selected_piece.set_coordinates(to_x, to_y)
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
        return (x, y) in self._piece_coordinates

    def is_selected_piece_at(self, x, y):
        if self._selected_piece is not None:
            return self._selected_piece.coordinates == (x, y)

    def is_possible_move(self, x, y):
        if self._selected_piece is None:
            return False
        print(f"Possible moves: {self._selected_piece.possible_fields}")
        return (x, y) in self._special_moves or (x, y) in self._selected_piece.possible_fields

    def __str__(self):
        return f"{self._name} ({self._color})"

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
            print(f"Possible moves: {self._selected_piece.possible_fields}")

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



