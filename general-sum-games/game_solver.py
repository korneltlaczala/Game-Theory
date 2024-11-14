import numpy as np
from scipy.optimize import linprog

class SimpleSolver():
    
    def __init__(self, matrix=None):
        self.matrix = np.array(matrix)
        self.result = [None for _ in range(3)]

    def solve(self):
        self.result[1] = self.solve_for(player=1)
        self.result[2] = self.solve_for(player=2)

        self.value = self.result[1].fun
        self.strats1 = self.result[1].x[:-1]
        self.strats2 = self.result[2].x[:-1]
    
    def run(self):
        self.solve()
        self.display_solution()
        self.compare_player_values()

    def solve_for(self, player=1):
        if player == 1:
            matrix = self.matrix
            coeff = -1
        else:
            matrix = self.matrix.T
            coeff = 1
        rows, cols = matrix.shape

        c = np.zeros(rows + 1)
        c[-1] = coeff
        A_ub = np.hstack((coeff*matrix.T, -coeff*np.ones((cols, 1))))
        b_ub = np.zeros(cols)
        A_eq = np.ones((1, rows + 1))
        A_eq[0, -1] = 0
        b_eq = np.ones(1)
        bounds = [(0, None) for _ in range(rows)] + [(None, None)]

        result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        result.fun *= coeff
        return result

    def display_solution(self):
        value = round(self.value, 2)
        strats1 = [round(x, 2) for x in self.strats1]
        strats2 = [round(x, 2) for x in self.strats2]

        print(f"Value of the game: {value}")
        print(f"Optimal strategy for player 1: {strats1}")
        print(f"Optimal strategy for player 2: {strats2}")

    def compare_player_values(self):
        value1 = round(self.result[1].fun, 2)
        value2 = round(self.result[2].fun, 2)
        print(f"Value for player 1: {value1}")
        print(f"Value for player 2: {value2}")

    def display_matrix(self):
        print(self.matrix)


class GeneralSolver():

    def __init__(self, A, B):
        self.A = np.array(A)
        self.B = np.array(B)

    def run(self):
        self.solverA = SimpleSolver(self.A)
        self.solverB = SimpleSolver(self.B.T)
        self.solverA.solve()
        self.solverB.solve()
        self.safety_levelA = self.solverA.value
        self.safety_levelB = self.solverB.value
        self.maxminA = self.solverA.strats1
        self.maxminB = self.solverB.strats1

    def display_solution(self):
        self.display_matrix()
        print(f"Safety level of player 1: {round(self.safety_levelA, 2)}")
        print(f"Safety level of player 2: {round(self.safety_levelB, 2)}")
        print(f"Optimal strategy for player 1: {self.maxminA}")
        print(f"Optimal strategy for player 2: {self.maxminB}")
    
    def display_matrix(self):
        print("Matrix A:")
        print(self.A)
        print("Matrix B:")
        print(self.B)

    def calc_maxmin_payoff(self):
        maxmin_payoffA = np.dot(self.maxminA, np.dot(self.A, self.maxminB))
        print(f"Maxmin payoff for player 1: {maxmin_payoffA}")
        maxmin_payoffB = np.dot(self.maxminA, np.dot(self.B, self.maxminB))
        print(f"Maxmin payoff for player 2: {maxmin_payoffB}")

def solve(matrix):
    solver = SimpleSolver(matrix)
    solver.run()

if __name__ == "__main__":
    A = [[2, 1],
        [0, 3]]
    B = [[0, 3],
        [1, 2]]
    solver = GeneralSolver(A, B)
    solver.run()
    solver.display_solution()
    solver.calc_maxmin_payoff()
