import random

from perudo_ai.player import Player
from typing import *

__all__ = ["Game", "GameErrorMessage"]


class Decision:
    pass


class Round:
    pass


class GameErrorMessage:
    LESS_THAN_TWO_PLAYERS = "There can not be less than two players!"
    INVALID_PLAYERS_TYPE = (
        "A list of players or a number of players (integer) should be entered!"
    )
    UNIQUE_PLAYERS_NAME = "Can not have two players with same name!"
    INVALID_DICE_TYPE = "An integer should be entered"
    INVALID_GAME_TYPE = "An integer should be entered"
#
# class Table:
#
#     def __init__(self,players:List[Player]):
#         for i, player in enumerate(players):
#             player.left_neighbor = players[i-1]

class Game:
    def __init__(self, players: Union[int, List[Player]]) -> None:
        self.players = players
        self._round = 1
        for i, player in enumerate(players):
            player.left_neighbor = players[i-1]

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, players: Union[int, List[Player]]) -> None:
        if isinstance(players, int):
            if players >= 2:
                self._players = [
                    Player() for _ in range(players)
                ]  # TODO: check unique names
            elif players < 2:
                raise ValueError(GameErrorMessage.LESS_THAN_TWO_PLAYERS)
            else:
                raise NotImplementedError
        elif isinstance(players, list):
            if all([isinstance(player, Player) for player in players]):
                if len(players) >= 2:
                    if len(set([player.name for player in players])) == len(players):
                        self._players = players
                    elif len(set([player.name for player in players])) != len(players):
                        raise ValueError(GameErrorMessage.UNIQUE_PLAYERS_NAME)
                    else:
                        raise NotImplementedError
                elif len(players) < 2:
                    raise ValueError(GameErrorMessage.LESS_THAN_TWO_PLAYERS)
            else:
                raise TypeError(GameErrorMessage.INVALID_PLAYERS_TYPE)
        else:
            raise TypeError(GameErrorMessage.INVALID_PLAYERS_TYPE)


    @property
    def total_nb_dices(self) -> int:
        return sum([player.n_dices_left for player in self.players])

    @total_nb_dices.setter
    def total_nb_dices(self, nb_dices:int) -> None:
        if isinstance(nb_dices, int):
            self._total_nb_dices = nb_dices
        else:
            raise TypeError(GameErrorMessage.INVALID_DICE_TYPE)

    @property
    def round(self) -> int:
        return self._round

    @round.setter
    def round(self, n_round) -> None:
        if isinstance(n_round, int):
            self._round = n_round
        else:
            raise TypeError(GameErrorMessage.INVALID_GAME_TYPE)

    def start_round(self):
        if self.round ==1:
            player_to_play = random.choice(self.players)


    def save_round_info_to_history(self):
        pass
