from typing import override

from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.QUEEN, color, x, y)

    @override
    def get_possible_moves(self, board):
        possible_moves = []

        x = self.x
        y = self.y
        color = self.color

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

        # Move diagonally
        for i in range(1, 8):
            if x + i > 7 or y + i > 7:
                break
            if board.is_empty(x + i, y + i):
                possible_moves.append((x + i, y + i))
            elif board.is_enemy(x + i, y + i, color):
                possible_moves.append((x + i, y + i))
                break
            else:
                break

        for i in range(1, 8):
            if x - i < 0 or y + i > 7:
                break
            if board.is_empty(x - i, y + i):
                possible_moves.append((x - i, y + i))
            elif board.is_enemy(x - i, y + i, color):
                possible_moves.append((x - i, y + i))
                break
            else:
                break

        for i in range(1, 8):
            if x + i > 7 or y - i < 0:
                break
            if board.is_empty(x + i, y - i):
                possible_moves.append((x + i, y - i))
            elif board.is_enemy(x + i, y - i, color):
                possible_moves.append((x + i, y - i))
                break
            else:
                break

        for i in range(1, 8):
            if x - i < 0 or y - i < 0:
                break
            if board.is_empty(x - i, y - i):
                possible_moves.append((x - i, y - i))
            elif board.is_enemy(x - i, y - i, color):
                possible_moves.append((x - i, y - i))
                break
            else:
                break

        # Move horizontally
        for i in range(1, 8):
            if x + i > 7:
                break
            if board.is_empty(x + i, y):
                possible_moves.append((x + i, y))
            elif board.is_enemy(x + i, y, color):
                possible_moves.append((x + i, y))
                break
            else:
                break

        for i in range(1, 8):
            if x - i < 0:
                break
            if board.is_empty(x - i, y):
                possible_moves.append((x - i, y))
            elif board.is_enemy(x - i, y, color):
                possible_moves.append((x - i, y))
                break
            else:
                break

        # Move vertically
        for i in range(1, 8):
            if y + i > 7:
                break
            if board.is_empty(x, y + i):
                possible_moves.append((x, y + i))
            elif board.is_enemy(x, y + i, color):
                possible_moves.append((x, y + i))
                break
            else:
                break

        for i in range(1, 8):
            if y - i < 0:
                break
            if board.is_empty(x, y - i):
                possible_moves.append((x, y - i))
            elif board.is_enemy(x, y - i, color):
                possible_moves.append((x, y - i))
                break
            else:
                break

        return possible_moves