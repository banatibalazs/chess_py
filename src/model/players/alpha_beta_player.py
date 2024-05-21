from src.controller.game_saver import GameSaver
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
        self.game_saver = GameSaver()

    @timer_decorator
    def choose_move(self, opponent):
        self.state_counter = 0
        best_move = None
        max_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        selected_piece = None
        maximizing_player = self
        minimizing_player = opponent

        for piece in self.get_movable_pieces():
            for move in piece.possible_fields:
                score = self.alpha_beta(0, 2, alpha, beta, True, move, piece,
                                        maximizing_player, minimizing_player)  # depth, max_depth, alpha, beta, is_maximizing_player

                if score > max_value:
                    max_value = score
                    selected_piece = piece
                    best_move = move

        print(f"State counter: {self.state_counter}")
        self.selected_piece = selected_piece
        print(f"Best move: {best_move}"
              f"\nMax value: {max_value}")
        if self.selected_piece is not None:
            print(f"Selected piece: {self.selected_piece.coordinates}")
        return best_move

    def alpha_beta(self, depth, max_depth, alpha, beta, is_maximizing_player, move, piece, maximizing_player, minimizing_player):
        self.state_counter += 1
        from_row, from_col = piece.coordinates

        if depth == max_depth or self.is_game_over():
            return self.get_state_score(maximizing_player, minimizing_player)

        if is_maximizing_player:
            max_eval = float('-inf')
            captured_piece = self.simulate_move(move, piece, maximizing_player, minimizing_player)
            for next_piece in maximizing_player.get_movable_pieces():
                for next_move in next_piece.possible_fields:
                    eval = self.alpha_beta(depth + 1, max_depth, alpha, beta, False, next_move,
                                           next_piece, maximizing_player, minimizing_player)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break

            if captured_piece is not None:
                minimizing_player.add_piece(captured_piece)
            piece.coordinates = (from_row, from_col)

            return max_eval
        else:
            min_eval = float('inf')
            captured_piece = self.simulate_move(move, piece, minimizing_player, maximizing_player)
            for next_piece in minimizing_player.get_movable_pieces():
                for next_move in next_piece.possible_fields:
                    eval = self.alpha_beta(depth + 1, max_depth, alpha, beta, True, next_move,
                                           next_piece, maximizing_player, minimizing_player)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            if captured_piece is not None:
                maximizing_player.add_piece(captured_piece)
            piece.coordinates = (from_row, from_col)
            return min_eval


    def is_game_over(self):
        return False

    def get_state_score(self, maximizing_player, minimizing_player) -> int:
        score = (maximizing_player.get_score() - minimizing_player.get_score()) * 10
        if maximizing_player.king.coordinates in minimizing_player._attacked_fields:
            score -= 1000

        if minimizing_player.king.coordinates in maximizing_player._attacked_fields:
            score += 1000

        return score

    def simulate_move(self, move, piece, current_player, opponent):
        piece.coordinates = move
        captured_piece = None
        if opponent.has_piece_at(*move):
            captured_piece = opponent.get_piece_at(*move)
            opponent.remove_piece_at(*move)

        return captured_piece

    def restore_state(self):
        pass

    def save_state(self):
        pass

