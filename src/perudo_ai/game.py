import random
import math

import pandas as pd
import os
from perudo_ai.player import Player
from perudo_ai.perudo_ai import PerudoAI
from perudo_ai.decision import Decision
from constants import *
from typing import *
from perudo_ai.custom_exceptions_and_errors import *
from collections import Counter, defaultdict
from datetime import datetime
import time

__all__ = [
    "Game",
]


class Game:
    def __init__(
        self,
        players: Union[int, List[Player]] = N_PLAYERS,
        n_init_dices: int = N_INIT_DICES_PER_PLAYER,
    ) -> None:
        self.n_init_dices = n_init_dices
        self.players = players
        self.round = 0
        self.hand_nb = 0
        self.allocate_left_players_to_right_players(allocate_same_number_of_dices=True)
        self.n_max_dices: int = len(list(self.players.values())) * n_init_dices
        self._rounds_history: Dict[str, Any] = defaultdict(lambda: defaultdict(list))
        self._decision_outcome_details = {}
        self.is_round_finished = False
        self.is_game_finished = False
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

    def run(self):
        while not self.is_game_finished:
            if self.hand_nb == 0:
                print(f'{"*"*20} STARTING NEW HAND {"*"*20}\n')

                if self.round == 0:
                    right_player = random.choice(list(self.players.values()))
                elif self.round != 0:
                    looser_from_past_round = self._rounds_history[self.round - 1].get(
                        "looser"
                    )
                    if looser_from_past_round:
                        right_player = self.players.get(looser_from_past_round)
                    elif not looser_from_past_round:
                        right_player = self._rounds_history[self.round - 1].get(
                            "left_player_to_looser_player"
                        )
                    else:
                        raise NotImplementedError
                else:
                    raise NotImplementedError
                right_player_decision = self.ask_player_to_make_decision(right_player)
            elif self.hand_nb != 0:
                right_player, right_player_decision = left_player, left_player_decision
            else:
                raise NotImplementedError
            print(f"Right Player - {right_player.name}:\t{right_player_decision}")
            time.sleep(5)
            left_player = right_player.left_player
            left_player_decision = self.ask_player_to_make_decision(
                left_player, right_player_decision
            )
            print(f"Left Player - {left_player.name}:\t{left_player_decision}")

            self.process_decisions(
                (right_player, right_player_decision),
                (left_player, left_player_decision),
            )

    def ask_player_to_make_decision(
        self,
        player: Union[Player, PerudoAI],
        right_player_decision: Union[None, Decision] = None,
    ) -> Decision:
        if isinstance(player, PerudoAI):
            player_decision = player.take_decision(
                self.hand_nb, self.total_nb_dices, right_player_decision
            )
        elif isinstance(player, Player):
            player_decision = player.take_decision()
        else:
            raise NotImplementedError
        return player_decision

    @property
    def players(self) -> Dict[str, Player]:
        return self._players

    @players.setter
    def players(self, players: Union[int, List[Player]]) -> None:
        if isinstance(players, int):
            if players >= 2:
                players_lst = [
                    Player(n_init_dices_per_player=self.n_init_dices)
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
                        # self._players = {player.name: player for player in players}
                        self._players = {}
                        for player in players:
                            player.n_init_dices = self.n_init_dices
                            self.players[player.name] = player
                    elif len(set([player.name for player in players])) != len(players):
                        raise InvalidGameInput(
                            ", ".join([player.name for player in players]),
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

    def process_decisions(
        self,
        right_player_decision_pair: Tuple[Player, Decision],
        left_player_decision_pair: Tuple[Player, Decision],
    ) -> Dict[str, Any]:
        left_player, left_player_decision = left_player_decision_pair  # right
        right_player, right_player_decision = right_player_decision_pair  # start
        right_player_name, left_player_name = right_player.name, left_player.name
        self.is_round_finished = False
        round = self.round
        dices_details_per_player = self.get_dices_details_per_player()
        all_dices_details = self.get_all_dices_details()
        nb_total_dices_at_beginning_round = sum(
            list(self.get_all_dices_details().values())
        )
        n_dices_per_player_at_beginning_round = {
            player.name: player.n_dices_left for player in self.players.values()
        }
        n_players_at_beginning_round = len(self.players)

        first_play = self.hand_nb == 0
        hand_nb = self.hand_nb
        decision_outcome = None
        decision_code = None
        nb_dices_bet_on_and_present_in_game = None
        winner, looser, left_player_to_looser_player = None, None, None

        if (
            first_play
            and (right_player_decision.raise_)
            and (right_player.n_dices_left > 1)
        ):
            if right_player_decision.raise_.dice_face == PACO:
                raise InvalidGameInput(
                    right_player.n_dices_left,
                    GameErrorMessage.NO_PACO_WHEN_STARTING_ROUND,
                )
        if right_player_decision.bluff:
            raise InvalidGameInput("Can not call bluff at the beginning of the hand.")
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
                    self.hand_nb += 1  # TODO:test
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
                        self.hand_nb += 1
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
                            self.hand_nb += 1
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
                    self.hand_nb += 1
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
                    ):  # 1.3.2.1 left player played with pacos  and raise enough
                        decision_outcome, decision_code = (
                            f"{left_player.left_player.name} to talk",
                            "1.3.2.1",
                        )
                        self.hand_nb += 1
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
            dices_details_per_player = self.get_dices_details_per_player()
            nb_dices_bet_on_and_present_in_game = (
                all_dices_details.get(right_player_decision.raise_.dice_face, 0)
                + all_dices_details.get(PACO, 0)
                if right_player_decision.raise_.dice_face != PACO
                else all_dices_details.get(PACO, 0)
            )
            if (
                right_player_decision.raise_.n_dices
                <= nb_dices_bet_on_and_present_in_game
            ):  # 2.1 right player has more dices
                decision_outcome, decision_code = (
                    f"Right Player:\t{right_player_name} won.\nLeft Player:\t{left_player_name} lost.",
                    "2.1",
                )
                left_player.take_one_dice_out()
                winner, looser = right_player_name, left_player_name
                left_player_to_looser_player = left_player.left_player
                self.close_round()

            elif (
                right_player_decision.raise_.n_dices
                > nb_dices_bet_on_and_present_in_game
            ):  # 2.2 right player has not as many dices as he claimed
                decision_outcome, decision_code = (
                    f"Right Player:\t{right_player_name} lost.\nLeft Player:\t{left_player_name} won.",
                    "2.2",
                )
                right_player.take_one_dice_out()
                winner, looser = left_player_name, right_player_name
                left_player_to_looser_player = right_player.left_player
                self.close_round()
            else:  # 2.3
                raise NotImplementedError("2.3")
        elif (
            left_player_decision.equal is True
        ):  # 3. Left Player calls equal on right players
            raise NotImplementedError

        else:  # 4. not raising, nor bluffing nor equalling, do not know what it is
            raise NotImplementedError("4")

        decision_outcome_details = {
            "round": round,
            "right_player_decision": right_player_decision,
            "left_player_decision": left_player_decision,
            "right_player_name": right_player_name,
            "left_player_name": left_player_name,
            "decision_outcome": decision_outcome,
            "is_round_finished": self.is_round_finished,
            "hand_nb": hand_nb,
            "dices_details_per_player": dices_details_per_player,
            "all_dices_details": all_dices_details,
            "winner": winner,
            "looser": looser,
            "left_player_to_looser_player": left_player_to_looser_player,
            "nb_total_dices_at_beginning_round": nb_total_dices_at_beginning_round,
            "nb_total_dices_at_end_round": sum(
                list(self.get_all_dices_details().values())
            ),
            "n_dices_per_player_at_beginning_round": n_dices_per_player_at_beginning_round,
            "n_dices_per_player_at_end_round": {
                player.name: player.n_dices_left for player in self.players.values()
            },
            "n_players_at_beginning_round": n_players_at_beginning_round,
            "n_players_at_end_round": len(self.players),
            "decision_code": decision_code,
            "nb_dices_bet_on_and_present_in_game": nb_dices_bet_on_and_present_in_game,
        }
        print(decision_outcome)
        self._decision_outcome_details = decision_outcome_details
        self.save_round_info_to_history()
        return decision_outcome_details

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

    @property
    def hand_nb(self) -> int:
        return self._hand_nb

    @hand_nb.setter
    def hand_nb(self, hand: int) -> None:
        if not (isinstance(hand, int) and hand >= 0):
            raise InvalidGameInput(hand)
        self._hand_nb = hand

    @property
    def is_round_finished(self) -> bool:
        return self._is_round_finished

    @is_round_finished.setter
    def is_round_finished(self, is_finished: bool) -> None:
        if not (isinstance(is_finished, bool)):
            raise InvalidGameInput(is_finished)
        self._is_round_finished = is_finished

    def save_round_info_to_history(self) -> None:  # TODO: testing
        decision_outcome_details: Dict[str, Any] = self._decision_outcome_details

        round = decision_outcome_details.get("round")
        right_player_decision = decision_outcome_details.get("right_player_decision")
        left_player_decision = decision_outcome_details.get("left_player_decision")
        right_player_name = decision_outcome_details.get("right_player_name")
        left_player_name = decision_outcome_details.get("left_player_name")
        left_player_to_looser_player = decision_outcome_details.get(
            "left_player_to_looser_player"
        )
        decision_outcome = decision_outcome_details.get("decision_outcome")
        hand_nb = decision_outcome_details.get("hand_nb")
        dices_details_per_player = decision_outcome_details.get(
            "dices_details_per_player"
        )
        all_dices_details = decision_outcome_details.get("all_dices_details")
        winner = decision_outcome_details.get("winner")
        looser = decision_outcome_details.get("looser")
        nb_total_dices_at_beginning_round = decision_outcome_details.get(
            "nb_total_dices_at_beginning_round"
        )
        nb_total_dices_at_end_round = decision_outcome_details.get(
            "nb_total_dices_at_end_round"
        )
        n_dices_per_player_at_beginning_round = decision_outcome_details.get(
            "n_dices_per_player_at_beginning_round"
        )
        n_dices_per_player_at_end_round = decision_outcome_details.get(
            "n_dices_per_player_at_end_round"
        )
        n_players_at_beginning_round = decision_outcome_details.get(
            "n_players_at_beginning_round"
        )
        n_players_at_end_round = decision_outcome_details.get("n_players_at_end_round")

        self._rounds_history[round]["right_player_decision_by_name"].append(
            {right_player_name: right_player_decision}
        )
        self._rounds_history[round]["left_player_decision_by_name"].append(
            {left_player_name: left_player_decision}
        )
        self._rounds_history[round]["decision_pairs"].append(
            {
                "right_player_name": right_player_name,
                "left_player_name": left_player_name,
                "right_player_decision": right_player_decision,
                "left_player_decision": left_player_decision,
            }
        )
        self._rounds_history[round]["decision_outcome"].append(decision_outcome)
        self._rounds_history[round]["is_round_finished"].append(self.is_round_finished)
        self._rounds_history[round]["hand_nb"].append(hand_nb)
        self._rounds_history[round][
            "dices_details_per_player"
        ] = dices_details_per_player
        self._rounds_history[round]["all_dices_details"] = all_dices_details
        self._rounds_history[round]["winner"] = winner
        self._rounds_history[round]["looser"] = looser
        self._rounds_history[round][
            "left_player_to_looser_player"
        ] = left_player_to_looser_player
        self._rounds_history[round][
            "nb_total_dices_at_beginning_round"
        ] = nb_total_dices_at_beginning_round
        self._rounds_history[round][
            "nb_total_dices_at_end_round"
        ] = nb_total_dices_at_end_round
        self._rounds_history[round][
            "n_dices_per_player_at_beginning_round"
        ] = n_dices_per_player_at_beginning_round
        self._rounds_history[round][
            "n_dices_per_player_at_end_round"
        ] = n_dices_per_player_at_end_round
        self._rounds_history[round][
            "n_players_at_beginning_round"
        ] = n_players_at_beginning_round
        self._rounds_history[round]["n_players_at_end_round"] = n_players_at_end_round
        self._rounds_history[round]["decision_code"] = decision_outcome_details.get(
            "decision_code"
        )
        if self.is_game_finished:
            if IS_DEBUG_MODE:
                print("Logging round history...")
            self.log_rounds_history()

    def log_rounds_history(self) -> None:
        now = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        rounds_history_logs_name = f"rounds_history_logs_name_{now}"
        with open(
            os.path.join(PATH_TO_ROUNDS_HISTORY, rounds_history_logs_name + ".json"),
            "w",
        ) as f:
            f.write(str(self._rounds_history))
        pd.DataFrame(self._rounds_history).to_csv(
            os.path.join(PATH_TO_ROUNDS_HISTORY, rounds_history_logs_name + ".csv")
        )

    def allocate_left_players_to_right_players(
        self, allocate_same_number_of_dices: bool = False
    ) -> None:
        players_lst = list(self.players.values())
        for i, player in enumerate(
            players_lst
        ):  # game attributes a left playeallocate_left_players_to_right_playersr to all players and also the same number of dices
            player.left_player = players_lst[i - 1]
            if allocate_same_number_of_dices:
                player.n_dices_left = self.n_init_dices

    def close_round(self) -> None:
        # put hand_nb to 0
        # check how many dices has the looser
        # if 0 remove this player from the game
        # reallocate the left player to the new circle of players
        # shuffle all dices
        if IS_DEBUG_MODE:
            print(f"close round being called with {self.players}")
        self.is_round_finished = True
        self.round += 1
        self.hand_nb = 0
        player_to_be_removed = None
        for player in self.players.values():
            if player.n_dices_left == 0:
                player_to_be_removed = (
                    player.name
                )  # avoir RuntimeError, dictionary changed size during iteration
                if IS_DEBUG_MODE:
                    print(f"Player to be removed {player}")
        if player_to_be_removed:
            del self.players[player_to_be_removed]
            for player in self.players.values():
                player.shuffle_dices()
            self.allocate_left_players_to_right_players()

        if len(self.players) == 1:
            if IS_DEBUG_MODE:
                print("The game is finished!")
            self.is_game_finished = True
