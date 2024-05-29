from typing import Optional, Tuple, Set
import hashlib
import numpy as np

from src.controller.custom_types_for_type_hinting import ByteArray8x8


class GameState:
    def __init__(self) -> None:
        self.board: ByteArray8x8 = np.array([
            [-2, -3, -4, -5, -6, -4, -3, -2],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [2, 3, 4, 5, 6, 4, 3, 2]], dtype=np.byte)

        self.step_from: Optional[Tuple[int, int]] = None
        self.step_to: Optional[Tuple[int, int]] = None
        self._possible_fields: Set[Tuple[int, int]] = set()
        self._last_move = None
        # black king
        self._king_04_is_moved: bool = False
        # white king
        self._king_74_is_moved: bool = False
        # black rooks
        self._rook_00_is_moved: bool = False
        self._rook_07_is_moved: bool = False
        # white rooks
        self._rook_70_is_moved: bool = False
        self._rook_77_is_moved: bool = False
        self._is_en_passant: bool = False
        self._is_white_turn: bool = True
        self._is_game_over: bool = False
        self._state_count: int = 0

    def hash_state(self):
        """Generate a hash for the current game state."""
        # Convert the game state attributes to a string
        state_str = str(self.board) + str(self.step_from) + str(self.step_to) + str(self._possible_fields) + \
                    str(self._last_move) + str(self._king_04_is_moved) + str(self._king_74_is_moved) + \
                    str(self._rook_00_is_moved) + str(self._rook_07_is_moved) + str(self._rook_70_is_moved) + \
                    str(self._rook_77_is_moved) + str(self._is_en_passant) + str(self._is_white_turn) + \
                    str(self._is_game_over) + str(self._state_count)

        # Generate a hash from the string
        state_hash = hashlib.sha256(state_str.encode()).hexdigest()

        return state_hash

    def copy(self):
        """Create a copy of the current game state."""
        new_state = GameState()
        new_state.board = self.board.copy()
        new_state.step_from = self.step_from
        new_state.step_to = self.step_to
        new_state._possible_fields = self._possible_fields.copy()
        new_state._last_move = self._last_move
        new_state._king_04_is_moved = self._king_04_is_moved
        new_state._king_74_is_moved = self._king_74_is_moved
        new_state._rook_00_is_moved = self._rook_00_is_moved
        new_state._rook_07_is_moved = self._rook_07_is_moved
        new_state._rook_70_is_moved = self._rook_70_is_moved
        new_state._rook_77_is_moved = self._rook_77_is_moved
        new_state._is_en_passant = self._is_en_passant
        new_state._is_white_turn = self._is_white_turn
        new_state._is_game_over = self._is_game_over
        new_state._state_count = self._state_count
        return new_state

    @property
    def state_count(self):
        return self._state_count

    @state_count.setter
    def state_count(self, value):
        self._state_count = value

    @property
    def last_move(self):
        return self._last_move

    @last_move.setter
    def last_move(self, value):
        self._last_move = value

    @property
    def last_moved_piece(self):
        return self._last_moved_piece

    @last_moved_piece.setter
    def last_moved_piece(self, value):
        self._last_moved_piece = value

    @property
    def possible_fields(self):
        return self._possible_fields

    @possible_fields.setter
    def possible_fields(self, value):
        self._possible_fields = value

    @property
    def king_04_is_moved(self):
        return self._king_04_is_moved

    @king_04_is_moved.setter
    def king_04_is_moved(self, value):
        self._king_04_is_moved = value

    @property
    def king_74_is_moved(self):
        return self._king_74_is_moved

    @king_74_is_moved.setter
    def king_74_is_moved(self, value):
        self._king_74_is_moved = value

    @property
    def rook_00_is_moved(self):
        return self._rook_00_is_moved

    @rook_00_is_moved.setter
    def rook_00_is_moved(self, value):
        self._rook_00_is_moved = value

    @property
    def rook_07_is_moved(self):
        return self._rook_07_is_moved

    @rook_07_is_moved.setter
    def rook_07_is_moved(self, value):
        self._rook_07_is_moved = value

    @property
    def rook_70_is_moved(self):
        return self._rook_70_is_moved

    @rook_70_is_moved.setter
    def rook_70_is_moved(self, value):
        self._rook_70_is_moved = value

    @property
    def rook_77_is_moved(self):
        return self._rook_77_is_moved

    @rook_77_is_moved.setter
    def rook_77_is_moved(self, value):
        self._rook_77_is_moved = value

    @property
    def is_en_passant(self):
        return self._is_en_passant

    @is_en_passant.setter
    def is_en_passant(self, value):
        self._is_en_passant = value

    @property
    def is_white_turn(self):
        return self._is_white_turn

    @is_white_turn.setter
    def is_white_turn(self, value):
        self._is_white_turn = value

    @property
    def is_game_over(self):
        return self._is_game_over

    @is_game_over.setter
    def is_game_over(self, value):
        self._is_game_over = value



