from typing import List, Tuple, override, Set
from src.model.Board import Board
from src.model.ColorEnum import ColorEnum
from src.model.Piece import Piece
from src.model.PieceTypeEnum import PieceTypeEnum


class Pawn(Piece):
    def __init__(self, color: ColorEnum, x: int, y: int):
        super().__init__(PieceTypeEnum.PAWN, color, x, y)
        self._is_en_passant = False

    @override
    def update_attacked_fields(self, board: Board):
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
    def update_possible_fields(self, board: Board) -> None:
        self._possible_fields.clear()
        x = self.x
        y = self.y
        color = self.color

        piece_board = board.get_piece_board()

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


    def update_protected_fields(self, board: Board):
        self._protected_fields.clear()
        for field in self._attacked_fields:
            if self._color == ColorEnum.WHITE:
                if board.get_piece(field[0], field[1]) > 0:
                    self._protected_fields.add(field)
            else:
                if board.get_piece(field[0], field[1]) < 0:
                    self._protected_fields.add(field)

    def check_if_king_is_attacked_after_move(self, board: Board, move: Tuple[int, int],
                                             opponent_pieces: List["Piece"]) -> bool:
        # Copy the board
        copy_piece_board = copy.deepcopy(board.get_piece_board())

        # Get the king position
        if self.color == ColorEnum.WHITE:
            own_king_y, own_king_x = np.where(copy_piece_board == 6)
        else:
            own_king_y, own_king_x = np.where(copy_piece_board == -6)

        # Moving piece data
        from_x, from_y = self.x, self.y
        to_x, to_y = move
        value = self._type.value
        color = self.color

        # Move the piece
        copy_piece_board[from_y, from_x] = 0
        copy_piece_board[to_y, to_x] = value if color == ColorEnum.WHITE else -value

        # Update update opponents attack fields
        for piece in opponent_pieces:
            piece.update_attacked_fields(copy_piece_board)

        return False

    def update_possible_fields(self, board: Board):
        self._possible_fields = self._attacked_fields - self._protected_fields