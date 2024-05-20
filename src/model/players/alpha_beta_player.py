from src.model.enums.color import Color
from src.model.pieces.pawn import Pawn
from src.model.players.player import Player

import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time} seconds")
        return result
    return wrapper


class AlphaBeta(Player):
    def __init__(self, name: str, color, board, time: int):
        super().__init__(name, color, board, time)
        self.selected_piece = None
        self.chosen_move = None
        self.state_counter = 0

    @timer_decorator
    def choose_move(self, opponent):
        best_move = None
        max_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for piece in self.get_movable_pieces():
            for move in piece.possible_fields:
                score = self.minimax(0, 2, alpha, beta, True, move, piece, opponent)  # depth, max_depth, alpha, beta, is_maximizing_player
                if score > max_value:
                    max_value = score
                    self.selected_piece = piece
                    best_move = move
        print(f"State counter: {self.state_counter}")
        return best_move

    def minimax(self, depth, max_depth, alpha, beta, is_maximizing_player, move, piece, opponent):
        self.state_counter += 1
        if depth == max_depth or self.is_game_over():
            return self.simulate_move(move, piece, opponent)

        if is_maximizing_player:
            max_eval = float('-inf')
            for piece in self.get_movable_pieces():
                for move in piece.possible_fields:
                    eval = self.minimax(depth + 1, max_depth, alpha, beta, False, move, piece, opponent)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for piece in opponent.get_movable_pieces():
                for move in piece.possible_fields:
                    eval = self.minimax(depth + 1, max_depth, alpha, beta, True, move, piece, self)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def is_game_over(self):
        return False

    def simulate_move(self, move, piece, opponent) -> int:
        score = 0
        color = self.color
        from_row, from_col = piece.coordinates
        to_row, to_col = move

        piece.coordinates = move

        captured_piece = None
        if opponent.has_piece_at(*move):
            captured_piece = opponent.get_piece_at(*move)
            opponent.remove_piece_at(*move)

        self.update_pieces_attacked_fields(opponent.piece_coordinates)

        # Attacking the opponent's king is rewarded
        if opponent.king.coordinates in self._attacked_fields:
            score += 3

        # Capture opponent's pieces is rewarded
        score += self.get_score() - opponent.get_score()

        # Getting closer to the enemy's side is beneficial
        if isinstance(piece, Pawn) and (
                (color == Color.WHITE and from_row > to_row) or (color != Color.WHITE and from_row < to_row)):
            score += 4

        score += int(3.5 - abs(3.5 - to_col))

        if captured_piece is not None:
            opponent.add_piece(captured_piece)

        piece.coordinates = (from_row, from_col)

        return score