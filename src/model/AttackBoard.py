

class AttackBoard:


    def __init__(self, board):
        self.white_attack_board = [[0 for i in range(8)] for j in range(8)]
        self.black_attack_board = [[0 for i in range(8)] for j in range(8)]



        self.attackBoard = [[0 for i in range(10)] for j in range(10)]
        self.attackBoard = self.createAttackBoard()
        self.attackBoard = self.updateAttackBoard()