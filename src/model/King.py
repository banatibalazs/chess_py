from typing import override

from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.KING, color, x, y)

    @override
    def get_possible_moves(self, board) -> object:
        possible_moves = []
        x = self.x
        y = self.y
        color = self.color

        if board.is_empty(x, y - 1) or board.is_enemy(x, y - 1, color):
            possible_moves.append((x, y - 1))
        if board.is_empty(x, y + 1) or board.is_enemy(x, y + 1, color):
            possible_moves.append((x, y + 1))
        if board.is_empty(x - 1, y) or board.is_enemy(x - 1, y, color):
            possible_moves.append((x - 1, y))
        if board.is_empty(x + 1, y) or board.is_enemy(x + 1, y, color):
            possible_moves.append((x + 1, y))
        if board.is_empty(x - 1, y - 1) or board.is_enemy(x - 1, y - 1, color):
            possible_moves.append((x - 1, y - 1))
        if board.is_empty(x + 1, y - 1) or board.is_enemy(x + 1, y - 1, color):
            possible_moves.append((x + 1, y - 1))
        if board.is_empty(x - 1, y + 1) or board.is_enemy(x - 1, y + 1, color):
            possible_moves.append((x - 1, y + 1))
        if board.is_empty(x + 1, y + 1) or board.is_enemy(x + 1, y + 1, color):
            possible_moves.append((x + 1, y + 1))


        for move in possible_moves:
            if color == ColorEnum.WHITE:
                if board.square_is_attacked_by_black(move[0], move[1]):
                    possible_moves.remove(move)
            else:
                if board.square_is_attacked_by_white(move[0], move[1]):
                    possible_moves.remove(move)


        return possible_moves

    # def get_special_move(self, board):
    #
    #     x = self.x
    #     y = self.y
    #     color = self.color
    #
    #     coloring_board = board.coloring_board
    #     piece_board = board.piece_board
    #
    #     special_moves = []
    #     if color == ColorEnum.BLACK:
    #         # Then king is at (4, 0) and rooks are at (0, 0) and (7, 0)
    #         king = self._current_player.get_piece_at(4, 0)
    #         rook = self._current_player.get_piece_at(0, 0)
    #         if (isinstance(rook, Rook) and
    #             isinstance(king, King) and
    #             not rook.is_moved() and
    #             not king.is_moved() and
    #             self.is_empty_at(1, 0) and
    #             self.is_empty_at(2, 0) and
    #             self.is_empty_at(3, 0) and
    #             not self.square_is_attacked_by_black(4, 0) and
    #             not self.square_is_attacked_by_white(4, 0) and
    #             not self.square_is_attacked_by_white(3, 0) and
    #             not self.square_is_attacked_by_white(2, 0)):
    #             special_moves.append((0, 2))
    #
    #         rook = self._current_player.get_piece_at(7, 0)
    #         if (isinstance(rook, Rook) and
    #             isinstance(king, King) and
    #             not rook.is_moved() and
    #             not king.is_moved() and
    #             self.is_empty_at(5, 0) and
    #             self.is_empty_at(6, 0) and
    #             not self.square_is_attacked_by_black(4, 0) and
    #             not self.square_is_attacked_by_white(4, 0) and
    #             not self.square_is_attacked_by_white(5, 0) and
    #             not self.square_is_attacked_by_white(6, 0)):
    #             self._coloring_board[0, 6] = self.SPECIAL_MOVE_SYMBOL
    #
    #     else:
    #         king = self._current_player.get_piece_at(4, 7)
    #         rook = self._current_player.get_piece_at(0, 7)
    #         if (isinstance(rook, Rook) and
    #             isinstance(king, King) and
    #             not rook.is_moved() and
    #             not king.is_moved() and
    #             self.is_empty_at(1, 7) and
    #             self.is_empty_at(2, 7) and
    #             self.is_empty_at(3, 7) and
    #             not self.square_is_attacked_by_white(4, 7) and
    #             not self.square_is_attacked_by_black(4, 7) and
    #             not self.square_is_attacked_by_black(3, 7) and
    #             not self.square_is_attacked_by_black(2, 7)):
    #             self._coloring_board[7, 2] = self.SPECIAL_MOVE_SYMBOL
    #
    #         rook = self._current_player.get_piece_at(7, 7)
    #         if (isinstance(rook, Rook) and
    #             isinstance(king, King) and
    #             not rook.is_moved() and
    #             not king.is_moved() and
    #             self.is_empty_at(5, 7) and
    #             self.is_empty_at(6, 7) and
    #             not self.square_is_attacked_by_white(4, 7) and
    #             not self.square_is_attacked_by_black(4, 7) and
    #             not self.square_is_attacked_by_black(5, 7) and
    #             not self.square_is_attacked_by_black(6, 7)):
    #             self._coloring_board[7, 6] = self.SPECIAL_MOVE_SYMBOL