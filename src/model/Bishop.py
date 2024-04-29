from typing import override, Tuple, List

from src.controller.CustomTypesForTypeHinting import ByteArray8x8
import src.model.Board as Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.BISHOP, color, x, y)

    @override
    def get_possible_moves(self, board: Board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        possible_fields = []
        protected_fields = []
        x = self.x
        y = self.y
        color = self.color

        board: ByteArray8x8 = board.get_piece_board()

        vectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        directions = []
        for vector in vectors:
            direction = []
            for i in range(1, 8):
                if x + vector[0] * i > 7 or x + vector[0] * i < 0 or y + vector[1] * i > 7 or y + vector[1] * i < 0:
                    break
                direction.append((x + vector[0] * i, y + vector[1] * i))
            directions.append(direction)

        for direction in directions:
            for field in direction:
                if color == ColorEnum.WHITE:
                    if board[field[1], field[0]] == 0:
                        possible_fields.append(field)
                    elif board[field[1], field[0]] > 0:
                        protected_fields.append(field)
                        break
                    elif board[field[1], field[0]] < 0:
                        possible_fields.append(field)
                        break
                else:
                    if board[field[1], field[0]] == 0:
                        possible_fields.append(field)
                    elif board[field[1], field[0]] < 0:
                        protected_fields.append(field)
                        break
                    elif board[field[1], field[0]] > 0:
                        possible_fields.append(field)
                        break

        return possible_fields, protected_fields

    # @override
    # def get_possible_moves(self, board) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    #     possible_moves = []
    #     protected_fields = []
    #     x = self.x
    #     y = self.y
    #     color = self.color
    #
    #     for i in range(1, 8):
    #         if board.is_empty(x + i, y + i):
    #             possible_moves.append((x + i, y + i))
    #         elif board.is_enemy(x + i, y + i, color):
    #             possible_moves.append((x + i, y + i))
    #             break
    #         elif board.is_friend(x + i, y + i, color):
    #             protected_fields.append((x + i, y + i))
    #             break
    #         else:
    #             break
    #
    #     for i in range(1, 8):
    #         if board.is_empty(x - i, y + i):
    #             possible_moves.append((x - i, y + i))
    #         elif board.is_enemy(x - i, y + i, color):
    #             possible_moves.append((x - i, y + i))
    #             break
    #         elif board.is_friend(x - i, y + i, color):
    #             protected_fields.append((x - i, y + i))
    #             break
    #         else:
    #             break
    #
    #     for i in range(1, 8):
    #         if board.is_empty(x + i, y - i):
    #             possible_moves.append((x + i, y - i))
    #         elif board.is_enemy(x + i, y - i, color):
    #             possible_moves.append((x + i, y - i))
    #             break
    #         elif board.is_friend(x + i, y - i, color):
    #             protected_fields.append((x + i, y - i))
    #             break
    #         else:
    #             break
    #
    #     for i in range(1, 8):
    #         if board.is_empty(x - i, y - i):
    #             possible_moves.append((x - i, y - i))
    #         elif board.is_enemy(x - i, y - i, color):
    #             possible_moves.append((x - i, y - i))
    #             break
    #         elif board.is_friend(x - i, y - i, color):
    #             protected_fields.append((x - i, y - i))
    #             break
    #         else:
    #             break
    #
    #     return possible_moves, protected_fields
