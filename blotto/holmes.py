# page 8
# Holmes vs. Moriarty

import game_solver
matrix = [[100, -50],
          [0, 100]]
solver = game_solver.Solver(matrix)
solver.display_matrix()
solver.display_result()

print(solver.partial_payoff(1))
print(solver.partial_payoff(2))