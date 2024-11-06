from scipy.optimize import linprog
import numpy as np

class Solver():

    def __init__(self, matrix=None):
        self.matrix = matrix
        if matrix is not None:
            self.solve()

    def set_matrix(self, matrix):
        self.matrix = matrix

    def solve(self):
        result1 = self.solve_for(player=1)
        result2 = self.solve_for(player=2)

        value1 = result1.fun
        value2 = result2.fun
        # if (value1 != value2):
        #     raise ArithmeticError("Value for player1 does not match Value for player 2")
        self.value = value1
        self.value1 = value1
        self.value2 = value2
        self.strat1 = result1.x[:-1]
        self.strat2 = result2.x[:-1]

    def display_result(self):
        print(f"Value of the game: {self.value}\nValue 1: {self.value1}\nValue 2: {self.value2}")
        print(f"Optimal strategy for player 1: {self.strat1}")
        print(f"Optimal strategy for player 2: {self.strat2}")

    def solve_for(self, player=1):
        if player == 1:
            matrix = self.matrix.T
        else:
            matrix = self.matrix

        c = np.hstack([np.zeros(matrix.shape[1]), 1])
        b_ub = np.zeros(matrix.shape[0])
        A_ub = np.hstack([matrix, -np.ones((matrix.shape[0], 1))])
        sum_is_one = np.array([np.hstack([np.ones(matrix.shape[1]), 0])])
        one = np.array([1])
        bounds = np.array([(0, None) for _ in range(matrix.shape[1])] + [(None, None)])

        return linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=sum_is_one, b_eq=one, bounds=bounds, method='highs')
