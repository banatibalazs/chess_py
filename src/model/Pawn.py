from typing import Tuple, override, Set
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Pawn(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.PAWN, color, x, y)
        self._is_en_passant = False

    @override
    def update_attacked_fields(self, current_player, opponent):
        self._attacked_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        if color == ColorEnum.WHITE:
            if x - 1 >= 0 and y - 1 >= 0:
                if x - 1 >= 0 and y - 1 >= 0:
                    self._attacked_fields.add((x - 1, y - 1))
            if x + 1 <= 7 and y - 1 >= 0:
                if x + 1 <= 7 and y - 1 >= 0:
                    self._attacked_fields.add((x + 1, y - 1))
        else:
            if x - 1 >= 0 and y + 1 <= 7:
                if x - 1 >= 0 and y + 1 <= 7:
                    self._attacked_fields.add((x - 1, y + 1))
            if x + 1 <= 7 and y + 1 <= 7:
                if x + 1 <= 7 and y + 1 <= 7:
                    self._attacked_fields.add((x + 1, y + 1))




    @override
    def update_possible_fields(self, current_player, opponent) -> None:
        self._possible_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        piece_board = current_player._board.get_piece_board()

        # Move forward
        if color == ColorEnum.WHITE:
            if y - 1 >= 0:
                if piece_board[y - 1, x] == 0:
                    self._possible_fields.add((x, y - 1))
        else:
            if y + 1 <= 7:
                if piece_board[y + 1, x] == 0:
                    self._possible_fields.add((x, y + 1))

        # Move two squares forward
        if color == ColorEnum.WHITE and y == 6:
            if piece_board[y - 1, x] == 0 and piece_board[y - 2, x] == 0:
                self._possible_fields.add((x, y - 2))
        elif color == ColorEnum.BLACK and y == 1:
            if piece_board[y + 1, x] == 0 and piece_board[y + 2, x] == 0:
                self._possible_fields.add((x, y + 2))

        # Diagonal capture
        if color == ColorEnum.WHITE:
            if x - 1 >= 0 and y - 1 >= 0:
                if piece_board[y - 1, x - 1] < 0:
                    self._possible_fields.add((x - 1, y - 1))
            if x + 1 <= 7 and y - 1 >= 0:
                if piece_board[y - 1, x + 1] < 0:
                    self._possible_fields.add((x + 1, y - 1))
        else:
            if x - 1 >= 0 and y + 1 <= 7:
                if piece_board[y + 1, x - 1] > 0:
                    self._possible_fields.add((x - 1, y + 1))

            if x + 1 <= 7 and y + 1 <= 7:
                if piece_board[y + 1, x + 1] > 0:
                    self._possible_fields.add((x + 1, y + 1))

        # Attacked fields are possible fields only when enemy is there and the king will not be attacked after the move

        # filtered = set()
        # for field in self._possible_fields:
        #     if self.check_if_king_is_attacked_after_move(field, current_player, opponent):
        #         filtered.add(field)
        # self._possible_fields = self._possible_fields - filtered

    def update_protected_fields(self, current_player):
        self._protected_fields.clear()
        for field in self._attacked_fields:
            if current_player.has_piece_at(field[0], field[1]):
                self._protected_fields.add(field)




    @property
    def is_en_passant(self) -> bool:
        return self._is_en_passant

    @is_en_passant.setter
    def is_en_passant(self, value: bool) -> None:
        self._is_en_passant = value

    @override
    @property
    def attacked_fields(self) -> Set[Tuple[int, int]]:
        return self._attacked_fields

