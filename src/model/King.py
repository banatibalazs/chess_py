from typing import override, Tuple, List
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(PieceTypeEnum.KING, color, x, y)

    @override
    def update_piece(self, board: Board):
        self._possible_fields.clear()
        self._protected_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        piece_board = board.get_piece_board()
        white_attacked_fields = board.get_white_attack_board()
        black_attacked_fields = board.get_black_attack_board()
        white_protected_fields = board.get_white_protection_board()
        black_protected_fields = board.get_black_protection_board()

        move_pattern_list = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y),
                             (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]

        for move in move_pattern_list:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                field = piece_board[move[1], move[0]]
                if color == ColorEnum.WHITE:
                    if field <= 0 and not black_protected_fields[move[1], move[0]] and \
                            not black_attacked_fields[move[1], move[0]]:
                        self._possible_fields.add(move)
                    elif field > 0:
                        self._protected_fields.add(move)
                else:
                    if field >= 0 and not white_protected_fields[ move[1], move[0]] and \
                            not white_attacked_fields[ move[1], move[0]]:
                        self._possible_fields.add(move)
                    elif field < 0:
                        self._protected_fields.add(move)


