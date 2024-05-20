import unittest

from src.model.players.player import Player
from src.model.enums.color import Color
from src.model.board import Board

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.king = None
        self.white_player = Player("White", Color.WHITE, self.board)
        self.black_player = Player("Black", Color.BLACK, self.board)

    def set_king_position_and_update(self, row, col):
        self.white_player.init_pieces()
        self.black_player.init_pieces()

        if self.white_player.has_piece_at(row, col):
            self.white_player.get_piece_at(row, col).coordinates = self.white_player.king().coordinates

        self.white_player.king().coordinates = (row, col)
        self.white_player.update_pieces_attacked_fields(self.black_player)
        self.black_player.update_pieces_attacked_fields(self.white_player)


    def test_king_possible_moves_on_50(self):
        self.set_king_position_and_update(5, 0)
        expected_result = {(4, 0), (4, 1), (5, 1)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_51(self):
        self.set_king_position_and_update(5, 1)
        expected_result = {(4, 0), (4, 1), (4, 2), (5, 0), (5, 2)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_52(self):
        self.set_king_position_and_update(5, 2)
        expected_result = {(4, 1), (4, 2), (5, 1), (5, 3), (4, 3)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_53(self):
        self.set_king_position_and_update(5, 3)
        expected_result = {(4, 2), (4, 3), (5, 2), (5, 4), (4, 4)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_54(self):
        self.set_king_position_and_update(5, 4)
        expected_result = {(4, 3), (4, 4), (5, 3), (5, 5), (4, 5)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_55(self):
        self.set_king_position_and_update(5, 5)
        expected_result = {(4, 4), (4, 5), (5, 4), (5, 6), (4, 6)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_56(self):
        self.set_king_position_and_update(5, 6)
        expected_result = {(4, 5), (4, 6), (5, 5), (5, 7), (4, 7)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_57(self):
        self.set_king_position_and_update(5, 7)
        expected_result = {(4, 6), (5, 6), (4, 7)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_60(self):
        self.set_king_position_and_update(6, 0)
        expected_result = {(5, 0), (5, 1)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_61(self):
        self.set_king_position_and_update(6, 1)
        expected_result = {(5, 0), (5, 1), (5, 2)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_62(self):
        self.set_king_position_and_update(6, 2)
        expected_result = {(5, 1), (5, 2), (5, 3)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_63(self):
        self.set_king_position_and_update(6, 3)
        expected_result = {(5, 2), (5, 3), (5, 4)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_64(self):
        self.set_king_position_and_update(6, 4)
        expected_result = {(5, 3), (5, 4), (5, 5)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_65(self):
        self.set_king_position_and_update(6, 5)
        expected_result = {(5, 4), (5, 5), (5, 6)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_66(self):
        self.set_king_position_and_update(6, 6)
        expected_result = {(5, 5), (5, 6), (5, 7)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_67(self):
        self.set_king_position_and_update(6, 7)
        expected_result = {(5, 6), (5, 7)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_70(self):
        self.set_king_position_and_update(7, 0)
        expected_result = set()
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_71(self):
        self.set_king_position_and_update(7, 1)
        expected_result = set()
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_72(self):
        self.set_king_position_and_update(7, 2)
        expected_result = set()
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_73(self):
        self.set_king_position_and_update(7, 3)
        expected_result = set()
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_74(self):
        self.set_king_position_and_update(7, 4)
        expected_result = set()
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_75(self):
        self.set_king_position_and_update(7, 5)
        expected_result = set()
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_76(self):
        self.set_king_position_and_update(7, 6)
        expected_result = set()
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_77(self):
        self.set_king_position_and_update(7, 7)
        expected_result = set()
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_40(self):
        self.set_king_position_and_update(4, 0)
        expected_result = {(3, 0), (3, 1), (4, 1), (5, 0), (5, 1)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_41(self):
        self.set_king_position_and_update(4, 1)
        expected_result = {(3, 0), (3, 1), (3, 2), (4, 0), (4, 2), (5, 0), (5, 1), (5, 2)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_42(self):
        self.set_king_position_and_update(4, 2)
        expected_result = {(3, 1), (3, 2), (3, 3), (4, 1), (4, 3), (5, 1), (5, 2), (5, 3)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_43(self):
        self.set_king_position_and_update(4, 3)
        expected_result = {(3, 2), (3, 3), (3, 4), (4, 2), (4, 4), (5, 2), (5, 3), (5, 4)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_44(self):
        self.set_king_position_and_update(4, 4)
        expected_result = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_45(self):
        self.set_king_position_and_update(4, 5)
        expected_result = {(3, 4), (3, 5), (3, 6), (4, 4), (4, 6), (5, 4), (5, 5), (5, 6)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_46(self):
        self.set_king_position_and_update(4, 6)
        expected_result = {(3, 5), (3, 6), (3, 7), (4, 5), (4, 7), (5, 5), (5, 6), (5, 7)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_47(self):
        self.set_king_position_and_update(4, 7)
        expected_result = {(3, 6), (3, 7), (4, 6), (5, 6), (5, 7)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

######################################################################################################################

    def test_king_possible_moves_on_30(self):
        self.set_king_position_and_update(3, 0)
        expected_result = {(3, 1), (4, 0), (4, 1)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_31(self):
        self.set_king_position_and_update(3, 1)
        expected_result = {(3, 0), (3, 2), (4, 0), (4, 1), (4, 2)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_32(self):
        self.set_king_position_and_update(3, 2)
        expected_result = {(3, 1), (3, 3), (4, 1), (4, 2), (4, 3)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_33(self):
        self.set_king_position_and_update(3, 3)
        expected_result = {(3, 2), (3, 4), (4, 2), (4, 3), (4, 4)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_34(self):
        self.set_king_position_and_update(3, 4)
        expected_result = {(3, 3), (3, 5), (4, 3), (4, 4), (4, 5)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_35(self):
        self.set_king_position_and_update(3, 5)
        expected_result = {(3, 4), (3, 6), (4, 4), (4, 5), (4, 6)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_36(self):
        self.set_king_position_and_update(3, 6)
        expected_result = {(3, 5), (3, 7), (4, 5), (4, 6), (4, 7)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

    def test_king_possible_moves_on_37(self):
        self.set_king_position_and_update(3, 7)
        expected_result = {(3, 6), (4, 6), (4, 7)}
        self.assertEqual(self.white_player.king()._possible_fields, expected_result)

######################################################################################################################
    # def test_king_possible_moves_on_20(self):
    #     self.set_king_position_and_update(2, 0)
        expected_result = {(3, 0), (3, 1)}
    #     self.assertEqual(self.white_player.get_king()._possible_fields, expected_result)
    #
    # def test_king_possible_moves_on_21(self):
    #     self.set_king_position_and_update(2, 1)
    #     expected_result = {(3, 0), (3, 1), (3, 2)}
    #     self.assertEqual(self.white_player.get_king()._possible_fields, expected_result)
    #
    # def test_king_possible_moves_on_22(self):
    #     self.set_king_position_and_update(2, 2)
    #     expected_result = {(3, 1), (3, 2), (3, 3)}
    #     self.assertEqual(self.white_player.get_king()._possible_fields, expected_result)
    #
    # def test_king_possible_moves_on_23(self):
    #     self.set_king_position_and_update(2, 3)
    #     expected_result = {(3, 2), (3, 3), (3, 4)}
    #     self.assertEqual(self.white_player.get_king()._possible_fields, expected_result)








if __name__ == '__main__':
    unittest.main()