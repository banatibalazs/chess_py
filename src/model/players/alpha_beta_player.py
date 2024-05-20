# def alpha_beta_search(board, depth, alpha, beta, maximizing_player):
#     if depth == 0 or game_over(board):
#         return evaluate_board(board)
#
#     if maximizing_player:
#         max_eval = float('-inf')
#         for child in get_children(board):
#             eval = alpha_beta_search(child, depth - 1, alpha, beta, False)
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for child in get_children(board):
#             eval = alpha_beta_search(child, depth - 1, alpha, beta, True)
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return min_eval