from typing import List, Tuple, override

from src.model import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Pawn(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.PAWN, color, x, y)
        self._is_en_passant = False

    @override
    def get_possible_moves(self, board: Board) -> List[Tuple[int, int]]:
        possible_moves = []
        x = self.x
        y = self.y
        color = self.color

        '''
        The board [yx] coordinates
        
        [00][01][02][03][04][05][06][07]
        [10][11][12][13][14][15][16][17]
        [20][21][22][23][24][25][26][27]
        [30][31][32][33][34][35][36][37]
        [40][41][42][43][44][45][46][47]
        [50][51][52][53][54][55][56][57]
        [60][61][62][63][64][65][66][67]
        [70][71][72][73][74][75][76][77]
        '''

        # Move forward
        if color == ColorEnum.WHITE:
            if board.is_empty(x, y - 1):
                possible_moves.append((x, y - 1))
        else:
            if board.is_empty(x, y + 1):
                possible_moves.append((x, y + 1))

        # Move two squares forward
        if not self.is_moved():
            if color == ColorEnum.WHITE:
                if board.is_empty(x, y - 1) and board.is_empty(x, y - 2):
                    possible_moves.append((x, y - 2))
            else:
                if board.is_empty(x, y + 1) and board.is_empty(x, y + 2):
                    possible_moves.append((x, y + 2))

        # Capture diagonally
        if color == ColorEnum.WHITE:
            if board.is_enemy(x - 1, y - 1, color):
                possible_moves.append((x - 1, y - 1))
            if board.is_enemy(x + 1, y - 1, color):
                possible_moves.append((x + 1, y - 1))
        else:
            if board.is_enemy(x - 1, y + 1, color):
                possible_moves.append((x - 1, y + 1))
            if board.is_enemy(x + 1, y + 1, color):
                possible_moves.append((x + 1, y + 1))

        # Remove moves that are out of bounds
        for move in possible_moves:
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                possible_moves.remove(move)

        return possible_moves

    def get_attacked_locations(self, board: Board) -> List[Tuple[int, int]]:

        attacked_locations = []
        x = self.x
        y = self.y
        color = self.color

        if color == ColorEnum.WHITE:
            if x - 1 >= 0 and y - 1 >= 0:
                if x - 1 >= 0 and y - 1 >= 0:
                    attacked_locations.append((x - 1, y - 1))
            if x + 1 <= 7 and y - 1 >= 0:
                if x + 1 <= 7 and y - 1 >= 0:
                    attacked_locations.append((x + 1, y - 1))
        else:
            if x - 1 >= 0 and y + 1 <= 7:
                if x - 1 >= 0 and y + 1 <= 7:
                    attacked_locations.append((x - 1, y + 1))
            if x + 1 <= 7 and y + 1 <= 7:
                if x + 1 <= 7 and y + 1 <= 7:
                    attacked_locations.append((x + 1, y + 1))

        return attacked_locations

    def en_passant_move(self, board: Board) -> None:
        possible_moves = []
        if self.color == ColorEnum.WHITE:
            if board.is_empty(self.x - 1, self.y - 1) and board.is_enemy(self.x - 1, self.y, self.color)\
                    and board.is_en_passant(self.x - 1, self.y - 1):
                possible_moves.append((self.x - 1, self.y - 1))
            if board.is_empty(self.x + 1, self.y - 1) and board.is_enemy(self.x + 1, self.y, self.color):
                possible_moves.append((self.x + 1, self.y - 1))
        else:
            if board.is_empty(self.x - 1, self.y + 1) and board.is_enemy(self.x - 1, self.y, self.color):
                possible_moves.append((self.x - 1, self.y + 1))
            if board.is_empty(self.x + 1, self.y + 1) and board.is_enemy(self.x + 1, self.y, self.color):
                possible_moves.append((self.x + 1, self.y + 1))

    @property
    def is_en_passant(self) -> bool:
        return self._is_en_passant

    @is_en_passant.setter
    def is_en_passant(self, value: bool) -> None:
        self._is_en_passant = value

