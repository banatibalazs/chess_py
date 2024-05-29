import random
import time
from abc import ABC, abstractmethod
from typing import Tuple, List, Optional

import numpy as np

from src.controller.game_state import GameState
from src.model.pieces.piece_logics import PieceLogics

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute.")
        return result
    return wrapper


class AI(ABC):
    def __init__(self, is_white):
        self.is_white = is_white

    @abstractmethod
    def get_move(self, game_state: GameState) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        pass


class RandomAI(AI):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.is_white = is_white
        self.selected_piece_position = None

    @timer_decorator
    def get_move(self, game_state: GameState):
        positions_of_movable_pieces = self.get_positions_of_movable_pieces(game_state)
        if positions_of_movable_pieces is None or len(positions_of_movable_pieces) == 0:
            return None
        else:
            position_of_chosen_piece = random.choice(positions_of_movable_pieces)
            legal_moves_of_chosen_piece = PieceLogics.get_legal_moves_of_piece(game_state, position_of_chosen_piece)
            if len(legal_moves_of_chosen_piece) == 0:
                return None
            chosen_move = random.choice(list(legal_moves_of_chosen_piece))

        return position_of_chosen_piece, chosen_move

    def get_positions_of_movable_pieces(self, game_state: GameState):
        piece_positions = np.argwhere(game_state.board > 0) if self.is_white else np.argwhere(game_state.board < 0)

        if len(piece_positions) == 0:
            return None
        else:
            movable_piece_positions = []
            for position in piece_positions:
                if PieceLogics.piece_has_legal_move(game_state, position):
                    movable_piece_positions.append(tuple(position))

            return movable_piece_positions


class GreedyAI(AI):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.is_white = is_white

    @timer_decorator
    def get_move(self, game_state: GameState):
        best_score = -9999
        best_move = None
        positions_of_movable_pieces = self.get_positions_of_movable_pieces(game_state)

        if positions_of_movable_pieces is None or len(positions_of_movable_pieces) == 0:
            return None
        else:
            for position in positions_of_movable_pieces:
                legal_moves_of_piece = PieceLogics.get_legal_moves_of_piece(game_state, position)
                for move in legal_moves_of_piece:
                    score = self.evaluate_move(game_state, position, move)
                    if score > best_score:
                        best_score = score
                        best_move = (position, move)

        return best_move

    def get_positions_of_movable_pieces(self, game_state: GameState) -> Optional[List[Tuple[int, int]]]:
        piece_positions = np.argwhere(game_state.board > 0) if self.is_white else np.argwhere(game_state.board < 0)

        if len(piece_positions) == 0:
            return None
        else:
            movable_piece_positions = []
            for position in piece_positions:
                if PieceLogics.piece_has_legal_move(game_state, tuple(position)):
                    movable_piece_positions.append(tuple(position))

            return movable_piece_positions

    def evaluate_move(self, game_state: GameState, from_position: Tuple[int, int], to_position: Tuple[int, int]):
        # This is a placeholder for your actual evaluation function.
        # It should return a score for the given move.
        # You might consider factors like the value of the piece being moved,
        # the value of the piece being captured (if any), the safety of the
        # piece's new position, etc.
        score: int = 0

        moving_piece = game_state.board[from_position]
        captured_piece = game_state.board[to_position]
        game_state.board[to_position] = moving_piece

        if self.is_white:
            own_piece_positions = np.argwhere(game_state.board > 0)
            opponent_piece_positions = np.argwhere(game_state.board < 0)
        else:
            own_piece_positions = np.argwhere(game_state.board < 0)
            opponent_piece_positions = np.argwhere(game_state.board > 0)

        for position in own_piece_positions:
            piece = game_state.board[tuple(position)]
            print(f"Own piece: {piece}")
            score += piece
        for position in opponent_piece_positions:
            score -= game_state.board[tuple(position)]

        game_state.board[to_position] = captured_piece
        game_state.board[from_position] = moving_piece

        return score


class MinimaxAI(AI):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.is_white = is_white
        self.depth = 2
        self.counter = 0

    @timer_decorator
    def get_move(self, game_state: GameState):
        best_score, best_move = self.minimax(game_state, self.depth, -9999, 9999, self.is_white)
        print(f"Counter: {self.counter}")
        return best_move

    def minimax(self, game_state: GameState, depth, alpha, beta, maximizing_player):
        self.counter += 1
        if depth == 0 or game_state.is_game_over:
            return self.evaluate_board(game_state), None

        best_move = None

        if maximizing_player:
            max_eval = -9999
            positions_of_movable_pieces = self.get_positions_of_movable_pieces(game_state, self.is_white)
            if positions_of_movable_pieces is None:
                return None
            for piece_position in positions_of_movable_pieces:
                legal_moves_of_piece = PieceLogics.get_legal_moves_of_piece(game_state, piece_position)
                for move in legal_moves_of_piece:

                    # game_state.make_move(position, move)
                    moving_piece = game_state.board[piece_position]
                    captured_piece = game_state.board[move]
                    game_state.board[move] = moving_piece

                    eval = self.minimax(game_state, depth - 1, alpha, beta, False)[0]

                    game_state.board[move] = captured_piece
                    game_state.board[piece_position] = moving_piece
                    # game_state.undo_move()

                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece_position, move)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = 9999
            positions_of_movable_pieces = self.get_positions_of_movable_pieces(game_state, not self.is_white)
            for piece_position in positions_of_movable_pieces:
                legal_moves_of_piece = PieceLogics.get_legal_moves_of_piece(game_state, piece_position)
                for move in legal_moves_of_piece:
                    # game_state.make_move(position, move)
                    moving_piece = game_state.board[piece_position]
                    captured_piece = game_state.board[move]
                    game_state.board[move] = moving_piece

                    eval = self.minimax(game_state, depth - 1, alpha, beta, True)[0]
                    # game_state.undo_move()
                    game_state.board[move] = captured_piece
                    game_state.board[piece_position] = moving_piece


                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece_position, move)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def get_positions_of_movable_pieces(self, game_state: GameState, is_white: bool) -> Optional[List[Tuple[int, int]]]:
        piece_positions = np.argwhere(game_state.board > 0) if is_white else np.argwhere(game_state.board < 0)

        if len(piece_positions) == 0:
            return None
        else:
            movable_piece_positions = []
            for position in piece_positions:
                if PieceLogics.piece_has_legal_move(game_state, tuple(position)):
                    movable_piece_positions.append(tuple(position))

            return movable_piece_positions

    def evaluate_board(self, game_state: GameState) -> int:
        score: int = 0
        if self.is_white:
            own_piece_positions = np.argwhere(game_state.board > 0)
            opponent_piece_positions = np.argwhere(game_state.board < 0)
        else:
            own_piece_positions = np.argwhere(game_state.board < 0)
            opponent_piece_positions = np.argwhere(game_state.board > 0)

        for position in own_piece_positions:
            piece = game_state.board[tuple(position)]
            # print(f"Own piece: {piece}")
            score += piece
        for position in opponent_piece_positions:
            score -= game_state.board[tuple(position)]

        return score
