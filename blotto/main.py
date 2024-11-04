from itertools import combinations_with_replacement, product

class BlottoGame():

    def __init__(self, player1_units=3, player2_units=3, posts=2):
        self.posts = posts
        self.player1 = Player(game=self, name="Blotto", units=player1_units)
        self.player2 = Player(game=self, name="Kije", units=player2_units)
        self.group_matrix = GroupMatrix(game=self)

    def score_strat(self, strat1, strat2):
        score = 0
        for i in range(self.posts):
            if strat1[i] > strat2[i]:
                score += 1
            elif strat1[i] < strat2[i]:
                score -= 1
        return score

    def score_group(self, group1, group2):
        score = 0
        for strat1 in group1.strategies:
            for strat2 in group2.strategies:
                score += self.score_strat(strat1, strat2)
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
        # self.name = f"[{primary_strat[0]} {primary_strat[1]} {primary_strat[2]}]*"
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

    def generate(self):
        return [[self.game.score_group(group1, group2) for group2 in self.player2.strat_groups] for group1 in self.player1.strat_groups]

    def __str__(self):
        output = f"{''.center(11)}"

        for group in self.player2.strat_groups:
            output += f"{group.name.center(11)}"
        output += "\n"
        
        for group, row in zip(self.player1.strat_groups, self.matrix):
            output += f"{group.name.center(11)}"
            for score in row:
                output += f"{str(score).center(11)}"
            output += "\n"
            
        return output

if __name__ == '__main__':
    game = BlottoGame(player1_units=8, player2_units=5, posts=3)
    print(game.player1)
    print(game.group_matrix)