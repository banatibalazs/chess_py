import unittest
from unittest.mock import Mock
import numpy as np

from src.controller.GuiController import GuiController


class TestViewController(unittest.TestCase):

    def setUp(self):
        self.view_controller = GuiController()
        self.mock_board = Mock()

    def test_update_board_view(self):
        # Create a mock 8x8 numpy array
        mock_piece_positions_board = np.zeros((8, 8), dtype=int)
        mock_coloring_board = np.array((8, 8), dtype=str)

        # Call the method with the mock data
        self.view_controller.update_board_view(mock_piece_positions_board, mock_coloring_board)

        # Assert that the method behaves as expected
        # This will depend on the specific implementation of your method
        # For example, you might check that the board's state has been updated correctly

    # Add more test methods as needed


if __name__ == '__main__':
    unittest.main()
