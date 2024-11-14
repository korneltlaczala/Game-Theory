# page 8
# Holmes vs. Moriarty

import old_solver
import game_solver

matrix = [[100, -50],
          [0, 100]]

solver = old_solver.Solver(matrix)
solver.display_matrix()
print(f"========== solver 1 ==========")
solver.display_result()

print(f"========== solver 2 ==========")
game_solver = game_solver.Solver(matrix)
game_solver.display_matrix()
