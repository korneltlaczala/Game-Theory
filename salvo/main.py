import numpy as np
from itertools import combinations, permutations

class SalvoGame:

    def __init__(self, board_size=3):
        self.board_size = board_size
        self.reset_board()
        self.p1_strats = self.generate_p1_strats()
        self.p2_strats = self.generate_p2_strats()
        self.payoff_matrix = self.generate_payoff_matrix()
        self.p1_strat_groups = None
        self.p2_strat_groups = None

    def reset_board(self):
        self.board = [0 for i in range(self.board_size*self.board_size)]

    def add_ship(self, a, b):
        self.board[a-1] = 1
        self.board[b-1] = 1

    def print_board(self):
        for i in range(self.board_size):
            print(self.board[i*self.board_size:(i+1)*self.board_size])
        print("-----------------")

    def generate_p1_strats(self):
        p1_strats = []
        for i in range(self.board_size):
            for j in range(self.board_size-1):
                f1 = i*self.board_size + j+1
                f2 = i*self.board_size + j+2
                p1_strats.append((f1, f2))
        for i in range(self.board_size-1):
            for j in range(self.board_size):
                f1 = i*self.board_size + j+1
                f2 = (i+1)*self.board_size + j+1
                p1_strats.append((f1, f2))
        
        return p1_strats

    def generate_p2_strats(self):
        return list(permutations(range(1, self.board_size*self.board_size + 1)))

    def generate_payoff_matrix(self):
        payoff_matrix = np.zeros((len(self.p1_strats), len(self.p2_strats)))
        for i, p1_strat in enumerate(self.p1_strats):
            for j, p2_strat in enumerate(self.p2_strats):
                payoff_matrix[i][j] = self.get_payoff(p1_strat, p2_strat)
        return payoff_matrix

    def generate_p1_group_payoff_matrix(self):
        pass

    def get_payoff(self, p1_strat, p2_strat):
        hits = 0
        ship_size = len(p1_strat)
        for i in range(len(p2_strat)):
            if p2_strat[i] in p1_strat:
                hits += 1
            if hits == ship_size:
                return i+1
        return -1

    def display_payoff_matrix(self, group=False):
        m, n = self.payoff_matrix.shape
        for i in range(n):
            col = self.payoff_matrix[:, i]
            print(self.p2_strats[i], end="\t")
            print(np.mean(col))
        # for i, row in enumerate(self.payoff_matrix):
        #     print(self.p1_strats[i], end="\t")
        #     print(np.mean(row))
    
class P1_StrategyGroup():
    def __init__(self, name="untitled"):
        self.strategies = []
        self.name = name

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def head(self, n=6):
        outcome = ""
        outcome += f"StrategyGroup {self.name}\n"
        for i, strat in enumerate(self.strategies):
            if i >= n:
                break
            outcome += f"{strat}\n"
        outcome += "-----------------"
        print(outcome)

    def __str__(self):
        outcome = ""
        outcome += f"StrategyGroup {self.name}\n"
        for strat in self.strategies:
            outcome += f"{strat}\n"
        outcome += "-----------------"
        return outcome

if __name__ == '__main__':
    game = SalvoGame()

    p1_sg1 = P1_StrategyGroup(name="[1,2]*")
    p1_sg2 = P1_StrategyGroup(name="[2,5]*")

    for strat in game.p1_strats:
        if 5 not in strat:
            p1_sg1.add_strategy(strat)
        else:
            p1_sg2.add_strategy(strat)

    print(p1_sg1)
    print(p1_sg2)

    game.display_payoff_matrix()