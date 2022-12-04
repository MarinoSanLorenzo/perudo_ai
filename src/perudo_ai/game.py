import random
import math

from perudo_ai.player import Player
from perudo_ai.decision import Decision
from constants import *
from typing import *
from perudo_ai.custom_exceptions_and_errors import *
from collections import Counter, defaultdict

__all__ = [
    "Game",
]


class Round:
    pass


class Game:
    def __init__(
        self,
        players: Union[int, List[Player]] = N_PLAYERS,
        n_init_dices: int = N_INIT_DICES_PER_PLAYER,
    ) -> None:
        self.n_init_dices = n_init_dices
        self.players = players
        self._round = 1
        players_lst = list(self.players.values())
        for i, player in enumerate(
            players_lst
        ):  # game attributes a left player to all players and also the same number of dices
            player.left_player = players_lst[i - 1]
            player.n_dices_left = n_init_dices
        self.n_max_dices: int = len(players_lst) * n_init_dices
        self._rounds_history: Dict[str, Any] = {}
        """
        {'round 1':{'decisions_given':[{'player_1_name':Decision1}, {'player_2_name:Decision2}, ....],
                    'decisions_received':[{'player_2_name:Decision1}, {'player_3_name:Decision2},....],
                    'decisions_pairs':[{'player_2_name:Decision1}, {'player_3_name:Decision2},....],
                    'pair_decision_outcomes':[{'right_player_decision':Decision1 , 'right_player_name':'player_1_name', 'left_player_decision':Decision2 , 'left_player_name':'player_2_name', 'decision_outcome': 'Player 3 to talk','is_round_finished':False, 'hand_nb':0', 'dices_details_per_player':None, 'all_dices_details':None},\
                                            {'right_player_decision':Decision2 , 'left_player_decision':Decision3 , 'decision_outcome': 'Player 3 looses dices,'is_round_finished':True, 'hand_nb':1', 'dices_details':{'6':1,, '2':1, '5 :3}, 'player_2_name:{'3':2, 'PACO':3}, ....} '}, 'all_dices_details':{'6':1, '2':1, '5':3, '3':2, 'PACO':3}],
                    'winner':'player_name', 
                    'looser':'player_name', 
                    'nb_total_dices_at_beginning_round': 25, 
                    'nb_total_dices_at_end_round': 24,
                    'dices_details_per_player' :{'player_1_name':{'6':1,, '2':1, '5 :3}, 'player_2_name:{'3':2, 'PACO':3}, ....},
                    'all_dices_details' :{'6':1, '2':1, '5':3, '3':2, 'PACO':3, ...},
                    'n_dices':{'player_1_name':5, 'player_2_name':5},
                    'n_players':4,
                    'player-left_player':['player_1_name-player_2_name', 'player_2_name-player_3_name', 'player_3_name-player_1_name'],
                    }
        'round2
        
        """

    @property
    def players(self) -> Dict[str, Player]:
        return self._players

    @players.setter
    def players(self, players: Union[int, List[Player]]) -> None:
        if isinstance(players, int):
            if players >= 2:
                players_lst = [
                    Player()
                    for _ in range(
                        players
                    )  # game makes sure that the players have the same dices as the game prescribes
                ]  # TODO: check unique names
                self._players = {player.name: player for player in players_lst}
            elif players < 2:
                raise InvalidGameInput(players, GameErrorMessage.LESS_THAN_TWO_PLAYERS)
            else:
                raise NotImplementedError
        elif isinstance(players, list):
            if all([isinstance(player, Player) for player in players]):
                if len(players) >= 2:
                    if len(set([player.name for player in players])) == len(players):
                        self._players = {player.name: player for player in players}
                    elif len(set([player.name for player in players])) != len(players):
                        raise InvalidGameInput(
                            "".join([player.name for player in players]),
                            GameErrorMessage.UNIQUE_PLAYERS_NAME,
                        )
                    else:
                        raise NotImplementedError
                elif len(players) < 2:
                    raise InvalidGameInput(GameErrorMessage.LESS_THAN_TWO_PLAYERS)
            else:
                raise InvalidGameInput(GameErrorMessage.INVALID_PLAYERS_TYPE)
        else:
            raise InvalidGameInput(GameErrorMessage.INVALID_PLAYERS_TYPE)

    @property
    def total_nb_dices(self) -> int:
        return sum([player.n_dices_left for player in self.players.values()])

    @total_nb_dices.setter
    def total_nb_dices(self, nb_dices: int) -> None:
        if isinstance(nb_dices, int):
            self._total_nb_dices = nb_dices
        else:
            raise InvalidGameInput(nb_dices, GameErrorMessage.INVALID_DICE_TYPE)

    @property
    def round(self) -> int:
        return self._round

    @round.setter
    def round(self, n_round) -> None:
        if isinstance(n_round, int):
            self._round = n_round
        else:
            raise InvalidGameInput(n_round, GameErrorMessage.INVALID_GAME_TYPE)

    def start_round(self):  # TODO
        if self.round == 1:
            player_to_play = random.choice(self.players.values())

    def process_decisions(
        self,
        right_player_decision_pair: Tuple[Player, Decision],
        left_player_decision_pair: Tuple[Player, Decision],
        hand_nb: int,
    ) -> Dict[str, Any]:
        left_player, left_player_decision = left_player_decision_pair  # right
        right_player, right_player_decision = right_player_decision_pair  # start
        right_player_name, left_player_name = right_player.name, left_player.name
        is_round_finished = False
        dices_details_per_player = None
        all_dices_details = None
        first_play = hand_nb == 0
        decision_outcome = None
        decision_code = None
        nb_dices_raised_on = None

        if (
            first_play
            and (right_player_decision.raise_.dice_face == PACO)
            and (right_player.n_dices_left > 1)
        ):
            raise InvalidGameInput(
                right_player.n_dices_left, GameErrorMessage.NO_PACO_WHEN_STARTING_ROUND
            )
        if right_player_decision.raise_.n_dices > self.total_nb_dices:
            raise InvalidGameInput(
                f"raise= {right_player.name}:{right_player_decision.raise_.n_dices}, {left_player.name}:{left_player_decision.raise_.n_dices}  vs total_nb_dices={self.total_nb_dices}",
                GameErrorMessage.RAISE_EXCEED_TOTAL_NB_DICES_LEFT,
            )
        if left_player_decision.raise_:
            if left_player_decision.raise_.n_dices > self.total_nb_dices:
                raise InvalidGameInput(
                    f"raise= {right_player.name}:{right_player_decision.raise_.n_dices}, {left_player.name}:{left_player_decision.raise_.n_dices}  vs total_nb_dices={self.total_nb_dices}",
                    GameErrorMessage.RAISE_EXCEED_TOTAL_NB_DICES_LEFT,
                )

        if right_player_decision.raise_ and left_player_decision.raise_:  # 1.RAISE
            if (
                left_player_decision.raise_.n_dices
                == right_player_decision.raise_.n_dices
            ):  # 1.1 same number of dices
                if (
                    left_player_decision.raise_.dice_face
                    > right_player_decision.raise_.dice_face
                ):  # 1.1.1 higher dice value
                    decision_outcome, decision_code = (
                        f"{left_player.left_player.name} to talk",
                        "1.1.1",
                    )
                else:  # 1.1.2 NO_LOWER_DICE_VALUE_WHEN_SAME_NUMBER_OF_DICES
                    raise InvalidGameInput(
                        f"left_player={left_player_name}-{left_player_decision} vs right_player={right_player_name}-{right_player_decision}",
                        GameErrorMessage.NO_LOWER_DICE_VALUE_WHEN_SAME_NUMBER_OF_DICES,
                    )
            elif (
                left_player_decision.raise_.n_dices
                > right_player_decision.raise_.n_dices
            ):  # 1.2 higher number of dices
                if (
                    right_player_decision.raise_.dice_face == PACO
                ):  # 1.2.1 Left player higher number of dices but right player played PACOS
                    if (
                        left_player_decision.raise_.dice_face == PACO
                    ):  # 1.2.1.1 left player played higher number of PACO
                        decision_outcome, decision_code = (
                            f"{left_player.left_player.name} to talk",
                            "1.2.1.1",
                        )
                    elif (
                        left_player_decision.raise_.dice_face != PACO
                    ):  # 1.2.1.2 left player played higher number of dices but not PACOS
                        if left_player_decision.raise_.n_dices >= (
                            right_player_decision.raise_.n_dices * 2 + 1
                        ):  # 1.2.1.2.1 Left player said more than twice +1
                            decision_outcome, decision_code = (
                                f"{left_player.left_player.name} to talk",
                                "1.2.1.2.1",
                            )
                        elif left_player_decision.raise_.n_dices < (
                            right_player_decision.raise_.n_dices * 2 + 1
                        ):  # 1.2.1.2.2 Left player did not say more than twice +1
                            raise InvalidGameInput(
                                GameErrorMessage.NO_LOWER_NUMBER_OF_DICES_UNLESS_IF_AT_LEAST_THE_HALF_IN_PACOS(
                                    "1.2.1.2.2",
                                    left_player_name,
                                    right_player_name,
                                    right_player_decision.raise_.n_dices * 2 + 1,
                                    left_player_decision.raise_.n_dices,
                                )
                            )
                    else:
                        raise NotImplementedError("1.2.1.3")
                elif (
                    right_player_decision.raise_.dice_face != PACO
                ):  # 1.2.2 Left player higher number of dices and right player did not play pacos
                    decision_outcome, decision_code = (
                        f"{left_player.left_player.name} to talk",
                        "1.2.2",
                    )
                else:
                    raise NotImplementedError("1.2.3")
            elif (
                left_player_decision.raise_.n_dices
                < right_player_decision.raise_.n_dices
            ):  # 1.3 lower number of dices
                half_nb_dices_pacos_needed = math.ceil(
                    right_player_decision.raise_.n_dices / 2
                )
                if (
                    left_player_decision.raise_.dice_face != "PACO"
                ):  # 1.3.1 left player did not raise with pacos
                    raise InvalidGameInput(
                        GameErrorMessage.NO_LOWER_NUMBER_OF_DICES_UNLESS_IF_AT_LEAST_THE_HALF_IN_PACOS(
                            "1.3.1.1",
                            left_player_name,
                            right_player_name,
                            half_nb_dices_pacos_needed,
                            left_player_decision.raise_.n_dices,
                        )
                    )
                elif (
                    left_player_decision.raise_.dice_face == "PACO"
                ):  # 1.3.2 left player played with pacos
                    if (
                        left_player_decision.raise_.n_dices < half_nb_dices_pacos_needed
                    ):  # 1.3.2.1 left player played with pacos but did not raise enough
                        raise InvalidGameInput(
                            GameErrorMessage.NO_LOWER_NUMBER_OF_DICES_UNLESS_IF_AT_LEAST_THE_HALF_IN_PACOS(
                                "1.3.2.1",
                                left_player_name,
                                right_player_name,
                                half_nb_dices_pacos_needed,
                                left_player_decision.raise_.n_dices,
                            )
                        )
                    elif (
                        left_player_decision.raise_.n_dices
                        >= half_nb_dices_pacos_needed
                    ):  # 1.3.2.1 left player played with pacos but and raise enough
                        decision_outcome, decision_code = (
                            f"{left_player.left_player.name} to talk",
                            "1.3.2.1",
                        )
                    else:  # 1.3.2.2
                        raise NotImplementedError("1.3.2.2")
                else:  # 1.3.3
                    raise NotImplementedError("1.3.3")
            else:  # 1.4
                raise NotImplementedError("1.4")
        elif (
            left_player_decision.bluff is True
        ):  # 2. Left player calls bluff on right player
            all_dices_details = self.get_all_dices_details()
            is_round_finished = True
            dices_details_per_player = self.get_dices_details_per_player()
            nb_dices_raised_on = (
                all_dices_details.get(right_player_decision.raise_.dice_face, 0)
                + all_dices_details.get(PACO, 0)
                if right_player_decision.raise_.dice_face != PACO
                else all_dices_details.get(PACO, 0)
            )
            if (
                right_player_decision.raise_.n_dices >= nb_dices_raised_on
            ):  # 2.1 right player has more dices
                decision_outcome, decision_code = (
                    f"Player {right_player_name} won.\nPlayer {left_player_name} lost.",
                    "2.1",
                )
            elif (
                right_player_decision.raise_.n_dices < nb_dices_raised_on
            ):  # 2.2 right player has not as many dices as he claimed
                decision_outcome, decision_code = (
                    f"Player {right_player_name} lost.\nPlayer {left_player_name} won.",
                    "2.2",
                )
            else:  # 2.3
                raise NotImplementedError("2.3")
        elif (
            left_player_decision.equal is True
        ):  # 3. Left Player calls equal on right players
            raise NotImplementedError

        else:  # 4. not raising, nor bluffing nor equalling, do not know what it is
            raise NotImplementedError("4")

        return {
            "right_player_decision": right_player_decision,
            "left_player_decision": left_player_decision,
            "right_player_name": right_player_name,
            "left_player_name": left_player_name,
            "decision_outcome": decision_outcome,
            "is_round_finished": is_round_finished,
            "hand_nb": hand_nb,
            "dices_details_per_player": dices_details_per_player,
            "all_dices_details": all_dices_details,
            "decision_code": decision_code,
            "nb_dices_raised_on": nb_dices_raised_on,
        }

    @property
    def n_max_dices(self) -> int:
        return self._n_max_dices

    @n_max_dices.setter
    def n_max_dices(self, n_max_dices: int) -> None:
        if isinstance(n_max_dices, int) and n_max_dices >= 0:
            self._n_max_dices = n_max_dices
        else:
            raise InvalidGameInput(n_max_dices, GameErrorMessage.INVALID_GAME_INPUT)

    @property
    def n_init_dices(self) -> int:
        return self._n_init_dices

    @n_init_dices.setter
    def n_init_dices(self, n_dices) -> None:
        if not (isinstance(n_dices, int) and n_dices > 0):
            raise InvalidGameInput(n_dices, GameErrorMessage.INVALID_GAME_INPUT)
        self._n_init_dices = n_dices

    def get_dices_details_per_player(self) -> Dict[str, Dict[str, int]]:
        dices_details = {}
        for player_name, player in self.players.items():
            dices_details[player_name] = Counter(player.dices)
        return dices_details

    def get_all_dices_details(self) -> Dict[str, int]:
        dices_details_per_player = self.get_dices_details_per_player()
        all_dices_details = defaultdict(lambda: 0)
        for dices_details in dices_details_per_player.values():
            for dice_face, nb_dices in dices_details.items():
                all_dices_details[dice_face] += nb_dices
        return all_dices_details

    def save_round_info_to_history(self):
        pass
