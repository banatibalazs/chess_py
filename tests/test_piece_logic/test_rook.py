import unittest

from src.controller.custom_types_for_type_hinting import ByteArray8x8
from src.model.pieces.piece_logics import PieceLogics
import numpy as np


class TestPieceLogics(unittest.TestCase):
    def setUp(self):
        self.piece_logic = PieceLogics()
        self.board: ByteArray8x8 = np.array([
            [-2, -3, -4, -5, -6, -4, -3, -2],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [0,  0,  0,  0,  0,  0,  0,  0],
            [1,  1,  1,  1,  1,  1,  1,  1],
            [2,  3,  4,  5,  6,  4,  3,  2]], dtype=np.byte)

        self._last_move = None
        self._last_moved_piece = None

        # black king
        self._king_04_is_moved = False
        # white king
        self._king_74_is_moved = False
        # black rooks
        self._rook_00_is_moved = False
        self._rook_07_is_moved = False
        # white rooks
        self._rook_70_is_moved = False
        self._rook_77_is_moved = False

        self._is_en_passant = False


    def test_legal_moves(self):
        moving_piece_position = (0, 0)

        # Test legal moves for the rook
        legal_moves = self.piece_logic.get_legal_moves_of_piece(self.board, moving_piece_position,
                                                                self._king_04_is_moved, self._king_74_is_moved,
                                                                self._rook_00_is_moved, self._rook_07_is_moved,
                                                                self._rook_70_is_moved, self._rook_77_is_moved,
                                                                self._is_en_passant, self._last_move)
        expected_moves = set()
        self.assertEqual(set(legal_moves), set(expected_moves))

if __name__ == "__main__":
    unittest.main()