from itertools import combinations_with_replacement, product
import numpy as np
import old_solver


class BlottoGame():

    def __init__(self, player1_units=3, player2_units=3, posts=2):
        self.posts = posts
        self.player1 = Player(game=self, name="Blotto", units=player1_units)
        self.player2 = Player(game=self, name="Kije", units=player2_units)
        self.group_matrix = GroupMatrix(game=self)
        self.solver = None

    def score_group(self, group1, group2):
        score = 0
        for strat1 in group1.strategies:
            for strat2 in group2.strategies:
                score += self.score_strat(strat1, strat2)
        score /= len(group1.strategies) * len(group2.strategies)
        return score

    def solve(self):
        if not self.group_matrix.simplified:
            matrix = self.group_matrix.matrix
        else:
            matrix = self.group_matrix.simple_matrix
        
        self.solver = old_solver.Solver(matrix)
        self.solver.display_result()

class BlottoNoCaptureGame(BlottoGame):

    def score_strat(self, strat1, strat2):
        score = 0
        for i in range(self.posts):
            if strat1[i] > strat2[i]:
                score += 1
            elif strat1[i] < strat2[i]:
                score -= 1
        return score


class BlottoCaptureGame(BlottoGame):

    def score_strat(self, strat1, strat2):
        score = 0
        for i in range(self.posts):
            if strat1[i] > strat2[i]:
                score += 1
                score += strat2[i]
            elif strat1[i] < strat2[i]:
                score -= 1
                score -= strat1[i]
        return score


class Player():
    def __init__(self, game, name="Player", units=3):
        self.game = game
        self.name = name
        self.units = units
        self.strats = self.generate_strats()
        self.primary_strats = self.generate_primary_strats()
        self.strat_groups = self.generate_strat_groups()

    def generate_strats(self):
        combinations = [combination for combination in product(range(self.units + 1), repeat=self.game.posts) if sum(combination) == self.units]
        return combinations

    def generate_primary_strats(self):
        return [dist for dist in combinations_with_replacement(range(self.units + 1), self.game.posts) if sum(dist) == self.units]

    def generate_strat_groups(self):
        groups = []
        for primary_strat in self.primary_strats:
            sg = StrategyGroup(primary_strat=primary_strat)
            for strat in self.strats:
                if sg.contains(strategy=strat):
                    sg.add_strategy(strategy=strat)
            groups.append(sg)
        return groups

    def __str__(self):
        output = f"{self.name} has {self.units} units\n"
        output += f"Primary Strategies: {self.primary_strats}\n"
        output += "-----------------"
        return output
    

class StrategyGroup():
    def __init__(self, primary_strat):
        self.primary_strat = primary_strat
        self.strategies = []
        self.name = f"[{' '.join(map(str, primary_strat[:]))}]*"

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def contains(self, strategy):
        return sorted(strategy) == sorted(self.primary_strat)

    def head(self, n=6):
        outcome = f"{self.name}  ~~~  "
        for i, strat in enumerate(self.strategies):
            if i >= n:
                break
            outcome += f"{strat}, "
        outcome = outcome[:-2]
        print(outcome)

    def __str__(self):
        outcome = f"{self.name}  ===  "
        for strat in self.strategies:
            outcome += f"{strat}, "
        outcome = outcome[:-2]
        return outcome


class GroupMatrix():

    def __init__(self, game):
        self.game = game
        self.player1 = game.player1
        self.player2 = game.player2
        self.matrix = self.generate()
        self.num_rows, self.num_columns = self.matrix.shape
        self.simplified = False

    def generate(self):
        return np.array([[self.game.score_group(group1, group2) for group2 in self.player2.strat_groups] for group1 in self.player1.strat_groups])

    def simplify(self, strictly_dominated=True):
        self.active_rows = np.ones(self.num_rows, dtype=bool)
        self.active_columns = np.ones(self.num_columns, dtype=bool)

        while True:
            if self.removed_dominated_row(strictly_dominated=strictly_dominated):
                continue
            if self.removed_dominated_column(strictly_dominated=strictly_dominated):
                continue
            break

        self.simple_matrix = self.matrix[self.active_rows, :][:, self.active_columns]
        self.simplified = True

    def dominates(self, entry_a, entry_b, strictly_dominated=True):
        if strictly_dominated:
            return np.all(entry_a > entry_b)
        return np.all(entry_a >= entry_b)

    def removed_dominated_row(self, strictly_dominated=True):
        for i in range(self.num_rows):
            if not self.active_rows[i]:
                continue
            for j in range(i+1, self.num_rows):
                if not self.active_rows[j]:
                    continue
                row_a = self.matrix[i, self.active_columns]
                row_b = self.matrix[j, self.active_columns]

                if self.dominates(row_a, row_b, strictly_dominated=strictly_dominated):
                    self.active_rows[j] = False
                    return True
                if self.dominates(row_b, row_a, strictly_dominated=strictly_dominated):
                    self.active_rows[i] = False
                    return True
        return False

    def removed_dominated_column(self, strictly_dominated=True):
        for i in range(self.num_columns):
            if not self.active_columns[i]:
                continue
            for j in range(i+1, self.num_columns):
                if not self.active_columns[j]:
                    continue
                column_a = -self.matrix[self.active_rows, i]
                column_b = -self.matrix[self.active_rows, j]

                if self.dominates(column_a, column_b, strictly_dominated=strictly_dominated):
                    self.active_columns[j] = False
                    return True
                if self.dominates(column_b, column_a, strictly_dominated=strictly_dominated):
                    self.active_columns[i] = False
                    return True

    def __str__(self, simple=False):
        matrix_to_use = self.simple_matrix if simple else self.matrix
        p1_strat_groups = np.array(self.player1.strat_groups)
        p2_strat_groups = np.array(self.player2.strat_groups)
        if simple:
            p1_strat_groups = p1_strat_groups[self.active_rows]
            p2_strat_groups = p2_strat_groups[self.active_columns]

        output = f"{''.center(11)}"
        for group in p2_strat_groups:
            output += f"{group.name.center(11)}"
        output += "\n"

        for group, row in zip(p1_strat_groups, matrix_to_use):
            output += f"{group.name.center(11)}"
            for score in row:
                output += f"{str(round(score, 2)).center(11)}"
            output += "\n"
            
        return output

    def show(self):
        print("Group Matrix:")
        print(self.__str__())

    def show_simple(self):
        print("Group Matrix simplified:")
        print(self.__str__(simple=True))


def play_game():
    # game = BlottoCaptureGame(player1_units=4, player2_units=3, posts=2)
    game = BlottoNoCaptureGame(player1_units=8, player2_units=5, posts=3)
    print(game.player1)
    print(game.player2)
    game.group_matrix.show()
    game.group_matrix.simplify(strictly_dominated=False)
    game.group_matrix.show_simple()
    game.solve()
    return game

if __name__ == '__main__':
    pass