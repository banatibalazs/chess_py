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
    def __init__(self, name: str, color: ColorEnum, board: Board, opponent_player: Optional["Player"] = None):
        self._name: str = name
        self._color: ColorEnum = color
        self._opponent_player: Optional["Player"] = opponent_player
        self._board: Board = board
        self._is_computer: bool = False
        self._selected_piece: Optional[Piece] = None
        self._last_moved_piece: Optional[Piece] = None
        self._king_is_checked: bool = False

        self._pieces: List[Piece] = []
        self._possible_moves_of_selected_piece: List[Tuple[int, int]] = []
        self._all_possible_move: List[Tuple[int, int]] = []
        self._protected_fields: List[Tuple[int, int]] = []
        self._special_moves: List[Tuple[int, int]] = []
        self._attacked_fields: List[Tuple[int, int]] = []
        self._piece_coordinates: Set[Tuple[int, int]] = set((piece.x, piece.y) for piece in self._pieces)

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

        self._piece_coordinates = set((piece.x, piece.y) for piece in self._pieces)


    def set_pieces(self, pieces: List[Piece]) -> None:
        self._pieces = pieces

    def set_opponent(self, opponent_player: "Player") -> None:
        self._opponent_player = opponent_player

    def update_normal_moves(self):
        board = self._board.get_piece_board()
        self._possible_moves_of_selected_piece = self.get_possible_moves_of_piece(self._selected_piece)
        self._update_attacked_locations(board)
        self._update_protected_fields(board)
        self._piece_coordinates = set((piece.x, piece.y) for piece in self._pieces)

    def update_data(self) -> None:
        self.update_players()
        self.update_boards()

    def update_players(self):
        # Set normal moves
        self.update_normal_moves()
        self._opponent_player.update_normal_moves()

        # Set special moves
        self.reset_special_moves()
        if isinstance(self.selected_piece, Pawn):
            self.add_en_passant_moves(self._opponent_player.get_last_moved_piece())
        if isinstance(self.selected_piece, King):
            self.add_castling_moves(self._board)

    def update_boards(self) -> None:
        self._board.reset_piece_board()
        self._board.reset_coloring_board()
        self._board.reset_attack_boards()
        self._board.reset_protection_boards()

        if self._color == ColorEnum.WHITE:
            self._board.update_piece_board(self.pieces, self._opponent_player.pieces)
            self._board.update_attack_boards(self.attacked_fields, self._opponent_player.attacked_fields)
            self._board.update_protection_boards(self.protected_fields, self._opponent_player.protected_fields)
        else:
            self._board.update_piece_board(self._opponent_player.pieces, self.pieces)
            self._board.update_attack_boards(self._opponent_player.attacked_fields, self.attacked_fields)
            self._board.update_protection_boards(self._opponent_player.protected_fields, self.protected_fields)

        self._board.update_coloring_board(self.selected_piece,
                                          self.possible_moves_of_selected_piece,
                                          self.special_moves)

    def _update_protected_fields(self, board: ByteArray8x8) -> None:
        self._protected_fields = [field for piece in self._pieces for field in self.get_possible_moves_of_piece(piece)]

    def get_possible_moves_of_piece(self, piece: Piece) -> Optional[List[Tuple[int, int]]]:
        if piece is None:
            return None
        if isinstance(piece, King):
            unfiltered_moves = piece.get_possible_moves(self._board.get_piece_board(),
                                                        self._piece_coordinates,
                                                        self._opponent_player._piece_coordinates)[0]
            filtered_moves = []
            for move in unfiltered_moves:
                if move not in self._opponent_player._attacked_fields and \
                        move not in self._opponent_player._protected_fields:
                    filtered_moves.append(move)
            return filtered_moves

        return piece.get_possible_moves(self._board.get_piece_board(),
                                        self._piece_coordinates,
                                        self._opponent_player._piece_coordinates)[0]

    def _update_attacked_locations(self, board: ByteArray8x8) -> None:
        self._attacked_fields = []
        for piece in self._pieces:
            if isinstance(piece, Pawn):
                attacked_locations = piece.get_attacked_locations()
            else:
                attacked_locations = self.get_possible_moves_of_piece(piece)
            for location in attacked_locations:
                self._attacked_fields.append((location[1], location[0]))

    def add_en_passant_moves(self, op_last_moved_piece) -> None:
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

    def add_castling_moves(self, board: Board) -> None:
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

    @property
    def possible_moves_of_selected_piece(self) -> List[Tuple[int, int]]:
        return self.get_possible_moves_of_piece(self._selected_piece)

    @property
    def special_moves(self) -> List[Tuple[int, int]]:
        return self._special_moves

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
        if self.selected_piece is None:
            return False
        return (x, y) in self._possible_moves_of_selected_piece

    def is_possible_special_move(self, x, y):
        return (x, y) in self.special_moves

    def is_possible_move(self, x, y):
        return self.is_possible_normal_move(x, y) or self.is_possible_special_move(x, y)

    def __str__(self):
        return f"{self._name} ({self._color})"

    @property
    def protected_fields(self) -> List[Tuple[int, int]]:
        return self._protected_fields

    @property
    def attacked_fields(self) -> List[Tuple[int, int]]:
        return self._attacked_fields

    def get_last_moved_piece(self):
        return self._last_moved_piece

    def reset_special_moves(self) -> None:
        self._special_moves = []

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

    def make_move(self, to_x, to_y) -> None:
        print("Player steps.")
        if self.selected_piece is None:
            raise ValueError("No piece is selected.")
        # Set en passant field if the pawn moves two squares
        self.reset_en_passant()
        self.set_en_passant(to_y)
        if self.is_promotion(to_x, to_y):
            self.promote_pawn(to_x, to_y, PieceTypeEnum.QUEEN)
        elif self.is_possible_special_move(to_x, to_y):
            if isinstance(self.selected_piece, King):
                self.castling(to_x, to_y)
            if isinstance(self.selected_piece, Pawn):
                self.en_passant(to_x, to_y)

        if self._opponent_player is not None and self._opponent_player.has_piece_at(to_x, to_y):
            self._opponent_player.remove_piece_at(to_x, to_y)
        self.selected_piece.set_coordinates(to_x, to_y)
        self.selected_piece.is_moved = True
        self._last_moved_piece = self.selected_piece
        self.reset_selected_piece()

    def is_promotion(self, to_x, to_y):
        return ((to_y == 0) or (to_y == 7)) and isinstance(self.selected_piece, Pawn)

    def reset_en_passant(self) -> None:
        if self._last_moved_piece is not None:
            self._last_moved_piece.is_en_passant = False

    def set_en_passant(self, to_y):
        # If the selected piece is a pawn and it moves two squares forward, set the en passant variable
        self.reset_en_passant()
        if isinstance(self.selected_piece, Pawn):
            if abs(self.selected_piece.y - to_y) == 2:
                print("En passant variable is set.")
                self.selected_piece.is_en_passant = True

    def promote_pawn(self, to_x: int, to_y: int, piece_type: PieceTypeEnum) -> None:
        print("Promoting pawn")
        from_x = self.selected_piece.x
        from_y = self.selected_piece.y
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

    def en_passant(self, to_x, to_y):
        if self._color == ColorEnum.WHITE:
            self._opponent_player.remove_piece_at(to_x, to_y + 1)
        else:
            self._opponent_player.remove_piece_at(to_x, to_y - 1)
        self.selected_piece.set_coordinates(to_x, to_y)
        self.reset_en_passant()

    def get_score(self) -> int:
        score = 0
        for piece in self._pieces:
            score += piece.value
        return score
