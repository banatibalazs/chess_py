from typing import Tuple, List, override

# from src.model.Board import Board
from src.model import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum



class Knight(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.KNIGHT, color, x, y)

    @override
    def get_possible_moves(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        possible_moves = []
        protected_fields = []
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
        if board.is_empty(x - 1, y - 2) or board.is_enemy(x - 1, y - 2, color):
            possible_moves.append((x - 1, y - 2))
        if board.is_empty(x + 1, y - 2) or board.is_enemy(x + 1, y - 2, color):
            possible_moves.append((x + 1, y - 2))
        if board.is_empty(x - 2, y - 1) or board.is_enemy(x - 2, y - 1, color):
            possible_moves.append((x - 2, y - 1))
        if board.is_empty(x + 2, y - 1) or board.is_enemy(x + 2, y - 1, color):
            possible_moves.append((x + 2, y - 1))
        if board.is_empty(x - 2, y + 1) or board.is_enemy(x - 2, y + 1, color):
            possible_moves.append((x - 2, y + 1))
        if board.is_empty(x + 2, y + 1) or board.is_enemy(x + 2, y + 1, color):
            possible_moves.append((x + 2, y + 1))
        if board.is_empty(x - 1, y + 2) or board.is_enemy(x - 1, y + 2, color):
            possible_moves.append((x - 1, y + 2))
        if board.is_empty(x + 1, y + 2) or board.is_enemy(x + 1, y + 2, color):
            possible_moves.append((x + 1, y + 2))

        if board.is_friend(x - 1, y - 2, color):
            protected_fields.append((x - 1, y - 2))
        if board.is_friend(x + 1, y - 2, color):
            protected_fields.append((x + 1, y - 2))
        if board.is_friend(x - 2, y - 1, color):
            protected_fields.append((x - 2, y - 1))
        if board.is_friend(x + 2, y - 1, color):
            protected_fields.append((x + 2, y - 1))
        if board.is_friend(x - 2, y + 1, color):
            protected_fields.append((x - 2, y + 1))
        if board.is_friend(x + 2, y + 1, color):
            protected_fields.append((x + 2, y + 1))
        if board.is_friend(x - 1, y + 2, color):
            protected_fields.append((x - 1, y + 2))
        if board.is_friend(x + 1, y + 2, color):
            protected_fields.append((x + 1, y + 2))

        return possible_moves, protected_fields


