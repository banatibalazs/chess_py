import random

from src.model.Player import Player


class ComputerPlayer(Player):
    def __init__(self, name, color):
        super().__init__(name, color)

    def make_move(self, board):
        # AI logic to make a move
        piece = self.choose_piece()
        self.get_possible_moves(piece, board)
        self.choose_move(board)

    def choose_piece(self):
        # AI logic to choose a piece
        return random.choice(self._pieces)

    def choose_move(self, board):
        # AI logic to choose a move
        pass

    def get_possible_moves(self, piece, board):
        # AI logic to get possible moves
        pass
