# page 9
# Saddle Points

import game_solver
matrix = [[4, 1, -3],
          [3, 2, 5],
          [0, 1, 6]]
solver = game_solver.Solver(matrix)
solver.display_matrix()
solver.display_result()

print(solver.partial_payoff(1))
print(solver.partial_payoff(2))