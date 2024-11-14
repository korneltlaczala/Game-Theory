# page 9
# Saddle Points

import old_solver
import game_solver
matrix = [[4, 1, -3],
          [3, 2, 5],
          [0, 1, 6]]
print(f"========== solver 1 ==========")
solver = old_solver.Solver(matrix)
solver.display_matrix()
solver.display_result()

print(f"========== solver 2 ==========")
game_solver = game_solver.Solver(matrix)
game_solver.display_matrix()
game_solver.display_result(player=1)
game_solver.display_result(player=2)