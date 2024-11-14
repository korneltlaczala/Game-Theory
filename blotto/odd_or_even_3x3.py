# page 
# Saddle Points

import old_solver
matrix = [[0, 1, -2],
          [1, -2, 3],
          [-2, 3, -4]]
solver = old_solver.Solver(matrix)
solver.display_matrix()
solver.display_result()

print(solver.partial_payoff(1))
print(solver.partial_payoff(2))