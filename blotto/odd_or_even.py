# page 5
# Odd or Even

import old_solver
import game_solver
matrix = [[-2, 3],
          [3, -4]]
solver = old_solver.Solver(matrix)
solver.display_matrix()
solver.display_result()

print(f"========== solver 2 ==========")
game_solver.solve(matrix)