from constants import *
from perudo_ai.game import Game
from perudo_ai.player import Player
from perudo_ai.perudo_ai import PerudoAI

if __name__ == "__main__":
    game = Game(
        players=[Player("Marino"), PerudoAI("AI_1"), PerudoAI("AI_2")], n_init_dices=2
    )
    game.run()
    # TODO: shuffling dices check + AI decision PACO
