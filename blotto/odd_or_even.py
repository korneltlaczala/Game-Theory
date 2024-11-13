# page 5
# Odd or Even

import game_solver
matrix = [[-2, 3],
          [3, -4]]
solver = game_solver.Solver(matrix)
solver.display_matrix()
solver.display_result()

print(solver.partial_payoff(1))
print(solver.partial_payoff(2))