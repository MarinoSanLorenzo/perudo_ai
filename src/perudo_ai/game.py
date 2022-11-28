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


class Game:
    def __init__(self, players: Union[int, List[Player]]) -> None:
        self.players = players

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

    def next_round(self):
        pass

    def save_round_info_to_history(self):
        pass
