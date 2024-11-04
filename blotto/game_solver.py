from scipy.optimize import linprog
import numpy as np

def solve_for(matrix, player=1):
    if player == 1:
        matrix = matrix.T

    c = np.hstack([np.zeros(matrix.shape[1]), 1])
    b_ub = np.zeros(matrix.shape[0])
    A_ub = np.hstack([matrix, -np.ones((matrix.shape[0], 1))])
    sum_is_one = np.array([np.hstack([np.ones(matrix.shape[1]), 0])])
    one = np.array([1])
    bounds = np.array([(0, None) for _ in range(matrix.shape[1])] + [(None, None)])

    return linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=sum_is_one, b_eq=one, bounds=bounds, method='highs')

def solve(matrix):
    result1 = solve_for(matrix, player=1)
    result2 = solve_for(matrix, player=2)

    print(f"Value of the game: {result1.fun} = {result2.fun}")
    print(f"Optimal strategy for player 1: {result1.x[:-1]}")
    print(f"Optimal strategy for player 2: {result2.x[:-1]}")