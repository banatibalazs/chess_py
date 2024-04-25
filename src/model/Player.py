from src.model.Bishop import Bishop
from src.model.King import King
from src.model.Knight import Knight
from src.model.Pawn import Pawn
from src.model.ColorEnum import ColorEnum
from src.model.Queen import Queen
from src.model.Rook import Rook


class Player:
    def __init__(self, name, color):
        self._name = name
        self._color = color
        self._is_computer = False
        self._pieces = []
        self._selected_piece = None

        '''
                         The board 

                [00][01][02][03][04][05][06][07]
                [10][11][12][13][14][15][16][17]
                [20][21][22][23][24][25][26][27]
                [30][31][32][33][34][35][36][37]
                [40][41][42][43][44][45][46][47]
                [50][51][52][53][54][55][56][57]
                [60][61][62][63][64][65][66][67]
                [70][71][72][73][74][75][76][77]
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
            if piece.get_coordinates() == (x, y):
                return piece
        return None

    def has_piece_at(self, x, y):
        for piece in self._pieces:
            if piece.get_coordinates() == (x, y):
                return True
        return False

    def __str__(self):
        return f"{self._name} ({self._color})"

    def reset_selected_piece(self):
        self._selected_piece = None
    def set_selected_piece(self, x, y):
        if self.has_piece_at(x, y):
            self._selected_piece = self.get_piece_at(x, y)

    def get_selected_piece(self):
        return self._selected_piece

    def has_selected_piece(self):
        return self._selected_piece is not None

    def remove_piece_at(self, x, y):
        for piece in self._pieces:
            if piece.get_coordinates() == (x, y):
                self._pieces.remove(piece)
                break