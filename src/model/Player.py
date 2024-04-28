from typing import Optional, List, Tuple
import src.model.Board as Board
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

        '''
                         The board 

                [00][01][02][03][04][05][06][07]                [A8][B8][C8][D8][E8][F8][G8][H8]
                [10][11][12][13][14][15][16][17]                [A7][B7][C7][D7][E7][F7][G7][H7]
                [20][21][22][23][24][25][26][27]                [A6][B6][C6][D6][E6][F6][G6][H6]
                [30][31][32][33][34][35][36][37]        ->      [A5][B5][C5][D5][E5][F5][G5][H5]
                [40][41][42][43][44][45][46][47]                [A4][B4][C4][D4][E4][F4][G4][H4]
                [50][51][52][53][54][55][56][57]                [A3][B3][C3][D3][E3][F3][G3][H3]
                [60][61][62][63][64][65][66][67]                [A2][B2][C2][D2][E2][F2][G2][H2]
                [70][71][72][73][74][75][76][77]                [A1][B1][C1][D1][E1][F1][G1][H1]
        '''

        # Append pawns
        for i in range(8):
            self._pieces.append(Pawn(color, i, 6 if color == ColorEnum.WHITE else 1))

        self._pieces.append(Rook(color,0, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Knight(color, 1, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Bishop(color, 2, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Queen(color, 3, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(King(color, 4, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Bishop(color, 5, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Knight(color, 6, 7 if color == ColorEnum.WHITE else 0))
        self._pieces.append(Rook(color, 7, 7 if color == ColorEnum.WHITE else 0))


    def is_computer(self):
        return self._is_computer

    def get_name(self):
        return self._name

    def get_color(self):
        return self._color

    @property
    def pieces(self):
        return self._pieces

    def get_piece_at(self, x, y):
        for piece in self._pieces:
            if piece.coordinates == (x, y):
                return piece
        return None

    def has_piece_at(self, x, y):
        for piece in self._pieces:
            if piece.coordinates == (x, y):
                return True
        return False

    def __str__(self):
        return f"{self._name} ({self._color})"

    def update_player(self, board: Board):
        self._update_possible_moves_of_selected_piece(board)
        self._update_attacked_locations(board)
        self._update_special_moves(board)
        self._update_protected_fields(board)

    def _update_possible_moves_of_selected_piece(self, board: Board):
        if self._selected_piece is not None:
            self._possible_moves, _ = self._selected_piece.get_possible_moves(board)

    @property
    def possible_moves_of_selected_piece(self) -> List[Tuple[int, int]]:
        # self._update_possible_moves_of_selected_piece(board)
        return self._possible_moves

    def _update_protected_fields(self, board: Board) -> None:
        self._protected_fields = [field for piece in self._pieces for field in piece.get_possible_moves(board)[1]]

    @property
    def protected_fields(self) -> List[Tuple[int, int]]:
        return self._protected_fields

    def _update_attacked_locations(self, board: Board) -> None:
        self._attacked_squares = []
        for piece in self._pieces:
            if isinstance(piece, Pawn):
                attacked_locations = piece.get_attacked_locations(board)
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

    def _update_special_moves(self, board: Board) -> None:
        self._special_moves = []
        # Promotion

        # En passant
        if self.selected_piece is not None and isinstance(self.selected_piece, Pawn):
            self.update_en_passant(board)
        # Castling
        if self.selected_piece is not None and isinstance(self.selected_piece, King):
            self.update_castling(board)

    def get_last_moved_piece(self):
        return self._last_moved_piece

    def update_en_passant(self, board: Board) -> None:
        print("Updating en passant")
        op_last_moved_piece = board.get_opponent_player_last_moved_piece()
        if op_last_moved_piece is not None and \
            isinstance(op_last_moved_piece, Pawn) and \
            op_last_moved_piece.is_en_passant and \
            self.selected_piece is not None and \
            isinstance(self.selected_piece, Pawn) and \
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
                    not rook.is_moved() and
                    not king.is_moved() and
                    board.is_empty_at(1, 0) and
                    board.is_empty_at(2, 0) and
                    board.is_empty_at(3, 0) and
                    not board.square_is_attacked_by_black(4, 0) and
                    not board.square_is_attacked_by_white(4, 0) and
                    not board.square_is_attacked_by_white(3, 0) and
                    not board.square_is_attacked_by_white(2, 0)):
                self._special_moves.append((0, 2))

            rook = self.get_piece_at(7, 0)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved() and
                    not king.is_moved() and
                    board.is_empty_at(5, 0) and
                    board.is_empty_at(6, 0) and
                    not board.square_is_attacked_by_black(4, 0) and
                    not board.square_is_attacked_by_white(4, 0) and
                    not board.square_is_attacked_by_white(5, 0) and
                    not board.square_is_attacked_by_white(6, 0)):
                self._special_moves.append((0, 6))

        else:
            king = self.get_piece_at(4, 7)
            rook = self.get_piece_at(0, 7)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved() and
                    not king.is_moved() and
                    board.is_empty_at(1, 7) and
                    board.is_empty_at(2, 7) and
                    board.is_empty_at(3, 7) and
                    not board.square_is_attacked_by_white(4, 7) and  # type: ignore
                    not board.square_is_attacked_by_black(4, 7) and
                    not board.square_is_attacked_by_black(3, 7) and
                    not board.square_is_attacked_by_black(2, 7)):
                self._special_moves.append((7, 2))

            rook = self.get_piece_at(7, 7)
            if (isinstance(rook, Rook) and
                    isinstance(king, King) and
                    not rook.is_moved() and
                    not king.is_moved() and
                    board.is_empty_at(5, 7) and
                    board.is_empty_at(6, 7) and
                    not board.square_is_attacked_by_white(4, 7) and
                    not board.square_is_attacked_by_black(4, 7) and
                    not board.square_is_attacked_by_black(5, 7) and
                    not board.square_is_attacked_by_black(6, 7)):
                self._special_moves.append((7, 6))

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

    def attacks_position(self, x: int, y: int, board):
        for piece in self._pieces:
            if (x, y) in piece.get_possible_moves(board):
                return True
        return False

    def get_piece_number(self):
        return len(self._pieces)

    def make_normal_move(self, to_x, to_y) -> None:
        print("Normal move.")
        # Set en passant field if the pawn moves two squares
        self.reset_en_passant()
        if isinstance(self.selected_piece, Pawn):
            if abs(self.selected_piece.y - to_y) == 2:
                print("En passant variable is set.")
                self.selected_piece.is_en_passant = True

            if to_y == 0 or to_y == 7:
                self.promote_pawn(to_x, to_y, PieceTypeEnum.QUEEN)
                return

        self.selected_piece.set_coordinates(to_x, to_y)
        self.selected_piece.set_moved()
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
                rook.set_moved()
        elif x == 6:
            rook = self.get_piece_at(7, y)
            if rook is not None:
                rook.set_coordinates(5, y)
                rook.set_moved()

        king = self.get_king()
        if king is not None:
            king.set_coordinates(x, y)
            king.set_moved()
        self._last_moved_piece = king
        self.reset_en_passant()

    def en_passant(self, to_x, to_y):
        self.selected_piece.set_coordinates(to_x, to_y)
        self.reset_en_passant()






