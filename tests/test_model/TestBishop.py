import unittest
from src.model.pieces.Bishop import Bishop
from src.model.Board import Board
from src.model.enums.Color import Color
from src.model.pieces.Pawn import Pawn
from src.model.players.Player import Player

"""
                            Black player's side
            -----------------------------------------------------------------------------

            Grid layout                       Piece codes                         Chess notation

[00][01][02][03][04][05][06][07]   [-2][-3][-4][-5][-6][-4][-3][-2]   [A8][B8][C8][D8][E8][F8][G8][H8]
[10][11][12][13][14][15][16][17]   [-1][-1][-1][-1][-1][-1][-1][-1]   [A7][B7][C7][D7][E7][F7][G7][H7]
[20][21][22][23][24][25][26][27]   [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]   [A6][B6][C6][D6][E6][F6][G6][H6]
[30][31][32][33][34][35][36][37]   [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]   [A5][B5][C5][D5][E5][F5][G5][H5]
[40][41][42][43][44][45][46][47]   [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]   [A4][B4][C4][D4][E4][F4][G4][H4]
[50][51][52][53][54][55][56][57]   [ 0][ 0][ 0][ 0][ 0][ 0][ 0][ 0]   [A3][B3][C3][D3][E3][F3][G3][H3]
[60][61][62][63][64][65][66][67]   [ 1][ 1][ 1][ 1][ 1][ 1][ 1][ 1]   [A2][B2][C2][D2][E2][F2][G2][H2]
[70][71][72][73][74][75][76][77]   [ 2][ 3][ 4][ 5][ 6][ 4][ 3][ 2]   [A1][B1][C1][D1][E1][F1][G1][H1]

            -----------------------------------------------------------------------------
                                             White player's side
"""

class TestBishop(unittest.TestCase):
    def setUp(self):
        self.bishop = Bishop(Color.WHITE, 0, 0)
        self.board = Board()
        self.white_player = Player("White", Color.WHITE, self.board)
        self.black_player = Player("Black", Color.BLACK, self.board)
        # self.current_player.add_piece(King(ColorEnum.WHITE, 4, 7))
        # self.opponent.add_piece(King(ColorEnum.BLACK, 4, 0))

    def test_update_attacked_fields_bishop_on_44_empty_board(self):
        self.bishop.coordinates = (4, 4)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7), (5, 3),
                           (6, 2), (7, 1), (3, 5), (2, 6), (1, 7)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_white_bishop_attacked_fields_empty_board(self):
        for row in range(8):
            for col in range(8):
                self.bishop = Bishop(Color.WHITE, row, col)
                self.bishop.update_attacked_fields(self.white_player, self.black_player)
                expected_result = set()
                for i in range(1, 8):
                    if row + i < 8 and col + i < 8:
                        expected_result.add((row + i, col + i))
                    if row + i < 8 and col - i >= 0:
                        expected_result.add((row + i, col - i))
                    if row - i >= 0 and col + i < 8:
                        expected_result.add((row - i, col + i))
                    if row - i >= 0 and col - i >= 0:
                        expected_result.add((row - i, col - i))
                self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_black_bishop_attacked_fields_empty_board(self):
        for row in range(8):
            for col in range(8):
                self.bishop = Bishop(Color.BLACK, row, col)
                self.bishop.update_attacked_fields(self.black_player, self.white_player)
                expected_result = set()
                for i in range(1, 8):
                    if row + i < 8 and col + i < 8:
                        expected_result.add((row + i, col + i))
                    if row + i < 8 and col - i >= 0:
                        expected_result.add((row + i, col - i))
                    if row - i >= 0 and col + i < 8:
                        expected_result.add((row - i, col + i))
                    if row - i >= 0 and col - i >= 0:
                        expected_result.add((row - i, col - i))
                self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_white_bishop_attacked_fields_full_enemy_board(self):
        for row in range(8):
            for col in range(8):
                self.black_player.add_piece(Pawn(Color.BLACK, row, col))

        for row in range(8):
            for col in range(8):
                self.bishop = Bishop(Color.WHITE, row, col)
                self.bishop.update_attacked_fields(self.white_player, self.black_player)
                expected_result = set()
                if row + 1 < 8 and col + 1 < 8:
                    expected_result.add((row + 1, col + 1))
                if row + 1 < 8 and col - 1 >= 0:
                    expected_result.add((row + 1, col - 1))
                if row - 1 >= 0 and col + 1 < 8:
                    expected_result.add((row - 1, col + 1))
                if row - 1 >= 0 and col - 1 >= 0:
                    expected_result.add((row - 1, col - 1))
                self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_black_bishop_attacked_fields_full_enemy_board(self):
        for row in range(8):
            for col in range(8):
                self.white_player.add_piece(Pawn(Color.WHITE, row, col))

        for row in range(8):
            for col in range(8):
                self.bishop = Bishop(Color.BLACK, row, col)
                self.bishop.update_attacked_fields(self.black_player, self.white_player)
                expected_result = set()
                if row + 1 < 8 and col + 1 < 8:
                    expected_result.add((row + 1, col + 1))
                if row + 1 < 8 and col - 1 >= 0:
                    expected_result.add((row + 1, col - 1))
                if row - 1 >= 0 and col + 1 < 8:
                    expected_result.add((row - 1, col + 1))
                if row - 1 >= 0 and col - 1 >= 0:
                    expected_result.add((row - 1, col - 1))
                self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_white_bishop_attacked_fields_full_friendly_board(self):
        for row in range(8):
            for col in range(8):
                self.white_player.add_piece(Pawn(Color.WHITE, row, col))

        for row in range(8):
            for col in range(8):
                self.bishop = Bishop(Color.WHITE, row, col)
                self.bishop.update_attacked_fields(self.white_player, self.black_player)
                expected_result = set()
                self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_black_bishop_attacked_fields_full_friendly_board(self):
        for row in range(8):
            for col in range(8):
                self.black_player.add_piece(Pawn(Color.BLACK, row, col))

        for row in range(8):
            for col in range(8):
                self.bishop = Bishop(Color.BLACK, row, col)
                self.bishop.update_attacked_fields(self.black_player, self.white_player)
                expected_result = set()
                self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_72_with_starting_board(self):
        """
        Bishop on (7, 2) with starting board. As if bishop was white.
        """
        self.white_player.init_pieces()
        self.black_player.init_pieces()

        self.white_player.remove_piece_at(7, 2)
        self.bishop.coordinates = (7, 2)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = set()
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_75_with_starting_board(self):
        """
        Bishop on (7, 5) with starting board, as if bishop was white.
        """

        self.white_player.init_pieces()
        self.black_player.init_pieces()

        self.white_player.remove_piece_at(7, 5)
        self.bishop.coordinates = (7, 5)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = set()
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_02_with_starting_board(self):
        """
        Bishop on (0, 2) with starting board, as if bishop was black.
        """
        self.white_player.init_pieces()
        self.black_player.init_pieces()

        self.white_player.remove_piece_at(0, 2)
        self.bishop.coordinates = (0, 2)
        self.bishop.update_attacked_fields(self.black_player, self.white_player)
        expected_result = set()
        self.assertEqual(self.bishop._attacked_fields, expected_result)


    def test_update_attacked_fields_bishop_on_05_with_starting_board(self):
        """
        Bishop on (0, 5) with starting board, as if bishop was black.
        """
        self.white_player.init_pieces()
        self.black_player.init_pieces()

        self.white_player.remove_piece_at(0, 5)
        self.bishop.coordinates = (0, 5)
        self.bishop.update_attacked_fields(self.black_player, self.white_player)
        expected_result = set()
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_44_surrounded_by_own_pieces(self):
        """
        Bishop on (4, 4) surrounded by own pieces.
        """
        self.white_player.add_piece(Pawn(Color.WHITE, 3, 3))
        self.white_player.add_piece(Pawn(Color.WHITE, 3, 5))
        self.white_player.add_piece(Pawn(Color.WHITE, 5, 3))
        self.white_player.add_piece(Pawn(Color.WHITE, 5, 5))

        self.bishop.coordinates = (4, 4)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = set()
        self.assertEqual(self.bishop._attacked_fields, expected_result)

    def test_update_attacked_fields_bishop_on_44_surrounded_by_opponent_pieces(self):
        """
        Bishop on (4, 4) surrounded by opponent pieces.
        """
        self.black_player.add_piece(Pawn(Color.BLACK, 3, 3))
        self.black_player.add_piece(Pawn(Color.BLACK, 3, 5))
        self.black_player.add_piece(Pawn(Color.BLACK, 5, 3))
        self.black_player.add_piece(Pawn(Color.BLACK, 5, 5))

        self.bishop.coordinates = (4, 4)
        self.bishop.update_attacked_fields(self.white_player, self.black_player)
        expected_result = {(3, 3), (3, 5), (5, 3), (5, 5)}
        self.assertEqual(self.bishop._attacked_fields, expected_result)


if __name__ == '__main__':
    unittest.main(verbosity=1)