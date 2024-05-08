from abc import ABC, abstractmethod
from typing import Tuple, Set, List
from src.model.ColorEnum import ColorEnum
from src.model.PieceTypeEnum import PieceTypeEnum



class Piece(ABC):
    def __init__(self, piece_type: PieceTypeEnum, color: ColorEnum, row: int, col: int):
        self._type = piece_type
        self._color = color
        self._col = col
        self._row = row
        self._value = self._init_value()
        self._attacked_fields = set()
        self._possible_fields = set()


        self._is_moved = False
        self._is_captured = False
        self._is_castling = False
        self._is_promotion = False
        self._is_check = False
        self._is_checkmate = False
        self._is_stalemate = False

    def _init_value(self):
        if self._type == PieceTypeEnum.PAWN:
            return 1
        elif self._type == PieceTypeEnum.KNIGHT:
            return 3
        elif self._type == PieceTypeEnum.BISHOP:
            return 3
        elif self._type == PieceTypeEnum.ROOK:
            return 5
        elif self._type == PieceTypeEnum.QUEEN:
            return 9
        elif self._type == PieceTypeEnum.KING:
            return 100

    @property
    def possible_fields(self) -> Set[Tuple[int, int]]:
        return self._possible_fields

    @possible_fields.setter
    def possible_fields(self, value: Set[Tuple[int, int]]):
        self._possible_fields = value

    @property
    def attacked_fields(self) -> Set[Tuple[int, int]]:
        return self._possible_fields

    @abstractmethod
    def update_attacked_fields(self, current_player, opponent):
        pass

    def update_possible_fields(self, current_player, opponent):
        self._possible_fields.clear()

        opponent_attacked_fields = set()
        for piece in opponent._pieces:
            for field in piece._attacked_fields:
                opponent_attacked_fields.add(field)

        for move in self._attacked_fields:
            if not self.king_in_check_after_move(move, current_player, opponent):
                self._possible_fields.add(move)

    def king_in_check_after_move(self, move, current_player, opponent) -> bool:
        result = False

        from_row = self.row
        from_col = self.col

        self.row = move[0]
        self.col = move[1]

        captured_piece = None
        if opponent.has_piece_at(move[0], move[1]):
            captured_piece = opponent.get_piece_at(move[0], move[1])
            opponent.remove_piece_at(move[0], move[1])


        king_position = current_player.get_king().coordinates
        print("King position: ", king_position)
        opponent.update_pieces_attacked_fields(current_player)
        for piece in opponent._pieces:
            for field in piece._attacked_fields:
                if king_position == field:
                    result = True
                    break


        if captured_piece is not None:
            opponent.add_piece(captured_piece)

        self.row = from_row
        self.col = from_col

        for piece in opponent._pieces:
            piece.update_attacked_fields(current_player, opponent)

        return result


        # if (self.color == ColorEnum.WHITE and self.type == PieceTypeEnum.QUEEN) or \
        #         (self.type == PieceTypeEnum.KING and self.color == ColorEnum.BLACK):
        #     print(self.color.name, self.type.name, " at: ", self.coordinates, end=" ")
        #     print("Possible fields: ", possible_fields)
        #     print("Deleted fields: ", filtered)
        #     print("Filtered possible fields: ", self._possible_fields)


    @property
    def value(self) -> int:
        return self._value

    @property
    def is_moved(self):
        return self._is_moved

    @is_moved.setter
    def is_moved(self, value: bool):
        self._is_moved = value

    @property
    def type(self):
        return self._type

    @property
    def col(self) -> int:
        return self._col

    @col.setter
    def col(self, value: int):
        self._col = value

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, value: int):
        self._row = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: ColorEnum):
        self._color = value

    @property
    def coordinates(self):
        """
        :return: (y:row, x:column)
        """
        return self._row, self._col

    @coordinates.setter
    def coordinates(self, value):
        """
        :param value: (y:row, x:column)
        :return: None
        """
        self.row, self.col = value


