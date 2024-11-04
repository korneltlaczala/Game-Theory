import numpy as np
from itertools import combinations, permutations

class SalvoGame:

    def __init__(self, board_size=3):
        self.board_size = board_size
        self.reset_board()
        self.generate_p1_strats()
        self.generate_p2_strats()
        self.p1_strat_groups = []
        self.p2_strat_groups = []

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
        self.p1_strats = []
        for i in range(self.board_size):
            for j in range(self.board_size-1):
                f1 = i*self.board_size + j+1
                f2 = i*self.board_size + j+2
                self.p1_strats.append((f1, f2))
        for i in range(self.board_size-1):
            for j in range(self.board_size):
                f1 = i*self.board_size + j+1
                f2 = (i+1)*self.board_size + j+1
                self.p1_strats.append((f1, f2))
        self.p1_strats

    def generate_p2_strats(self):
        self.p2_strats = list(permutations(range(1, self.board_size*self.board_size + 1)))

    def generate_payoff_matrix(self):
        self.payoff_matrix = []
        for p1_strat in self.p1_strats:
            row = []
            for p2_strat in self.p2_strats:
                row.append(self.get_payoff(p1_strat, p2_strat))
            self.payoff_matrix.append(row)

    def get_payoff(self, p1_strat, p2_strat):
        hits = 0
        ship_size = len(p1_strat)
        for i in range(len(p2_strat)):
            if p2_strat[i] in p1_strat:
                hits += 1
            if hits == ship_size:
                return i+1
        return -1

    def display_payoff_matrix(self):
        for i, row in enumerate(self.payoff_matrix):
            print(self.p1_strats[i], end="\t")
            print(np.mean(row))
    
class StrategyGroup():
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
    p1_sg1 = StrategyGroup(name="[1,2]*")
    p1_sg2 = StrategyGroup(name="[2,5]*")

    for strat in game.p1_strats:
        if 5 not in strat:
            p1_sg1.add_strategy(strat)
        else:
            p1_sg2.add_strategy(strat)

    print(p1_sg1)
    print(p1_sg2)

    p2_sg1 = StrategyGroup(name="Center")
    p2_sg2 = StrategyGroup(name="Border")
    CENTER = {5}
    BORDER = {2, 4, 6, 8}
    CORNER = {1, 3, 7, 9}
    for strat in game.p2_strats:
        if strat[0] in CENTER and strat[1:5] in BORDER:
            p2_sg1.add_strategy()