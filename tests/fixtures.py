from perudo_ai.game import Game
import pytest
from typing import *
from constants import *
from perudo_ai.player import Player
from perudo_ai.perudo_ai import PerudoAI

__all__ = ["three_players", "dices_lst", "game", "game_with_ai"]

# three_players = [Player(name="Marc"), Player("Jean"), Player("Luc")]
# dices_lst = [
#     ["2", "2", PACO, PACO, "5"],
#     ["3", "3", PACO, PACO, "6"],
#     ["2", "2", PACO, PACO, "5"],
# ]
# # two_players_and_one_ai = [PerudoAI("AI"), Player("Jean"), Player("Luc")]
# two_players_and_one_ai = [PerudoAI("AI"), Player("Jean"), Player("Luc")]
# game_with_ai = Game(two_players_and_one_ai)
# for player, dices in zip(game_with_ai.players.values(), dices_lst):
#     player._dices = dices
# game = Game(three_players)
# for player, dices in zip(game.players.values(), dices_lst):
#     player._dices = dices


@pytest.fixture()
def three_players() -> List[Player]:
    return [Player(name="Marc"), Player("Jean"), Player("Luc")]


@pytest.fixture()
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


@pytest.fixture()
def two_players_and_ai() -> List[Union[Player, PerudoAI]]:
    return [PerudoAI("AI"), Player("Jean"), Player("Luc")]


@pytest.fixture()
def game_with_ai(dices_lst: List[List[str]]) -> Game:
    two_players_and_one_ai = [PerudoAI("AI"), Player("Jean"), Player("Luc")]
    game = Game(two_players_and_one_ai)
    for player, dices in zip(game.players.values(), dices_lst):
        player._dices = dices
    return game
