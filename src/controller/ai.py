import random


class RandomAI:
    def __init__(self):
        pass

    def get_move(self, board):
        return random.choice(board.get_valid_moves())



class GreedyAI:
    def __init__(self):
        pass

    def get_move(self, board):
        best_move = None
        best_score = -9999
        for move in board.get_valid_moves():
            board.make_move(move)
            score = -board.evaluate()
            board.undo_move()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move


class MinimaxAI:
    def __init__(self, depth):
        self.depth = depth

    def get_move(self, board):
        return self.minimax(board, self.depth, True)[1]

    def minimax(self, board, depth, is_maximizing):
        if depth == 0 or board.is_game_over():
            return board.evaluate(), None

        if is_maximizing:
            best_score = -9999
            best_move = None
            for move in board.get_valid_moves():
                board.make_move(move)
                score = self.minimax(board, depth - 1, False)[0]
                board.undo_move()
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = 9999
            best_move = None
            for move in board.get_valid_moves():
                board.make_move(move)
                score = self.minimax(board, depth - 1, True)[0]
                board.undo_move()
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move