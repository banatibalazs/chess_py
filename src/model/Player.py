from typing import Optional, List

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
        self._king_is_checked = False
        self._pieces: List[Piece] = []
        self._possible_moves = []
        self._special_moves = []
        self._attacked_squares = []  # TODO

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

    def get_pieces(self):
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

    def move_piece(self, to_x, to_y) -> None:
        # Set en passant field if the pawn moves two squares
        self.reset_en_passant()
        if isinstance(self.selected_piece, Pawn):
            if abs(self.selected_piece.y - to_y) == 2:
                self.selected_piece.is_en_passant = True

            if to_y == 0 or to_y == 7:
                self.promote_pawn(to_x, to_y, PieceTypeEnum.QUEEN)
                return

        self.selected_piece.set_coordinates(to_x, to_y)
        self.selected_piece.set_moved()

    def reset_en_passant(self) -> None:
        for piece in self._pieces:
            if isinstance(piece, Pawn):
                piece.is_en_passant = False

    def promote_pawn(self, to_x: int, to_y: int, piece_type: PieceTypeEnum) -> None:
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



