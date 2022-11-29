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
        for i, player in enumerate(self.players):
            player.left_neighbor = self.players[i - 1]
        self._rounds_history: Dict[str, Any] = {}
        """
        {'round 1':{'decisions_given':[{'player_1_name':Decision1}, {'player_2_name:Decision2}, ....],
                    'decisions_received':[{'player_2_name:Decision1}, {'player_3_name:Decision2},....],
                    'winner':'player_name', 
                    'looser':'player_name', 
                    'nb_total_dices_at_beginning_round': 25, 
                    'nb_total_dices_at_end_round': 24,
                    'dices' :{'player_1_name':{'6':1,, '2':1, '5 :3}, 'player_2_name:{'3':2, 'PACO':3}, ....},
                    'n_dices':{'player_1_name':5, 'player_2_name':5},
                    'n_players':4,
                    'player-left_player':['player_1_name-player_2_name', 'player_2_name-player_3_name', 'player_3_name-player_1_name']
                    }
        'round2
        
        """

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
    def total_nb_dices(self, nb_dices: int) -> None:
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
        if self.round == 1:
            player_to_play = random.choice(self.players)

    def save_round_info_to_history(self):
        pass
