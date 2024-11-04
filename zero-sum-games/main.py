import random

class Game():

    def __init__(self):

        self.payoff_matrix = {
            ("1", "1"): -2,
            ("1", "2"): 3,
            ("2", "1"): 3,
            ("2", "2"): -4
        }
        self.player1 = MixedPlayer(name = "player1", strategy = (0.5, 0.5))
        self.player2 = MixedPlayer(name = "player2", strategy = (0.7, 0.3))
        self.score = 0

    def play(self, moves = 10):

        print(f"Match between {self.player1.name} and {self.player2.name}")
        print(self.player1)
        print(self.player2)

        for _ in range(moves):
            move1 = self.player1.next_move()
            move2 = self.player2.next_move()
            self.score += self.payoff_matrix[(move1, move2)]

        print(f"Final score after {moves} moves: {self.score}")
        print(f"Estimated Value: {self.score/moves}")



class Player():

    def __init__(self, name):
        self.name = name

class PurePlayer(Player):

    def __init__(self, name, strategy):
        super().__init__(name)
        self.strategy = strategy
        if strategy is None:
            self.strategy = self.ask_for_strategy()

    def ask_for_strategy(self):
        print(f"Choose a strategy for {self.name}: ")
        return input("1 or 2: ")

    def __str__(self):
        return f"{self.name} with a pure strategy {self.strategy}"

class MixedPlayer(Player):

    def __init__(self, name, strategy = None):
        super().__init__(name)
        self.strategy = strategy
        if strategy is None:
            self.strategy = self.ask_for_strategy()

    def ask_for_strategy(self):
        print(f"Choose a strategy for {self.name}: ")
        p1 = int(input("p1: "))
        p2 = int(input("p2: "))
        total = p1 + p2
        return (p1/total, p2/total)

    def next_move(self):
        if random.random() < self.strategy[0]:
            return "1"
        return "2"

    def __str__(self):
        return f"{self.name} with a mixed strategy {self.strategy}"


if __name__ == "__main__":
    game = Game()
    game.play(moves=1000000)
