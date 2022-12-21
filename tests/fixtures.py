from perudo_ai.game import Game
import pytest
from typing import *
from constants import *
from perudo_ai.player import Player

__all__ = ["three_players", "dices_lst", "game"]

three_players = [Player(name="Marc"), Player("Jean"), Player("Luc")]
dices_lst = [
    ["2", "2", PACO, PACO, "5"],
    ["3", "3", PACO, PACO, "6"],
    ["2", "2", PACO, PACO, "5"],
]
game = Game(three_players)
for player, dices in zip(game.players.values(), dices_lst):
    player._dices = dices


@pytest.fixture
def three_players() -> List[Player]:
    return [Player(name="Marc"), Player("Jean"), Player("Luc")]


@pytest.fixture
def dices_lst() -> List[List[str]]:
    return [
        ["2", "2", PACO, PACO, "5"],
        ["3", "3", PACO, PACO, "6"],
        ["2", "2", PACO, PACO, "5"],
    ]


@pytest.fixture()
def game(three_players: List[Player], dices_lst: List[List[str]]) -> Game:
    game = Game(three_players)
    for player, dices in zip(game.players.values(), dices_lst):
        player._dices = dices
    return game
