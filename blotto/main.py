from itertools import combinations_with_replacement, product

class BlottoGame():

    def __init__(self, blotto_units=3, kije_units=3, posts=2):
        self.posts = posts
        self.blotto = Player(game=self, name="Blotto", units=blotto_units)
        self.kije = Player(game=self, name="Kije", units=kije_units)

        # self.b_sg = []
        # for group in self.blotto_strat_groups:
        #     sg = StrategyGroup(name=f"Blotto {group}*")
        #     print(group)
        #     for strat in self.bstrats:
        #         if self.strat_in_group(strat=strat, group=group):
        #             sg.add_strategy(strat)


    def strat_in_group(self, strat, group):
        return sorted(strat) == sorted(group)

    def score(self, blotto_dist, kije_dist):
        score = 0
        for i in range(self.posts):
            if blotto_dist[i] > kije_dist[i]:
                score += 1
            elif blotto_dist[i] < kije_dist[i]:
                score -= 1
        return score


class Player():
    def __init__(self, game, name="Player", units=3):
        self.game = game
        self.name = name
        self.units = units
        self.strats = self.generate_strats()
        self.primary_strats = self.generate_primary_strats()

    def generate_strats(self):
        combinations = [(a1, a2, a3) for a1, a2, a3 in product(range(self.units + 1), repeat=3) if a1 + a2 + a3 == self.units]
        return combinations

    def generate_primary_strats(self):
        return [dist for dist in combinations_with_replacement(range(self.units + 1), self.game.posts) if sum(dist) == self.units]

    def __str__(self):
        output = f"{self.name} has {self.units} units\n"
        output += f"Primary Strategies: {self.primary_strats}\n"
        output += "-----------------"
        return output
    
class StrategyGroup():
    def __init__(self, primary_strat):
        self.primary_strat = primary_strat
        self.strategies = []
        self.name = f"[{primary_strat[0]} {primary_strat[1]} {primary_strat[2]}]*"

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def head(self, n=6):
        outcome = ""
        outcome += f"StrategyGroup {self.name}\n"
        for i, strat in enumerate(self.strategies):
            if i >= n:
                break
            outcome += f"{strat}\n"
        outcome += "-----------------"
        print(outcome)

    def __str__(self):
        outcome = f"{self.name}\n"
        for strat in self.strategies:
            outcome += f"{strat}\n"
        outcome += "-----------------"
        return outcome

if __name__ == '__main__':
    game = BlottoGame(blotto_units=8, kije_units=5, posts=3)
    print(game.blotto)
    print(game.kije)