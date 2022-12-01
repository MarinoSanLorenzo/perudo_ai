from constants import *
import random
import names
from typing import *
from perudo_ai.decision import Decision, Raise
from perudo_ai.custom_exceptions_and_errors import *


class Player:
    def __init__(
        self,
        name: Union[str, None] = None,
        n_players: int = N_PLAYERS,
        n_init_dices: int = N_INIT_DICES,
    ) -> None:
        if not name:
            name = names.get_full_name()
        self.name = name
        self.n_dices_left = n_init_dices
        self.n_players = n_players
        self._dices: List[str] = random.choices(POSSIBLE_VALUES, k=n_init_dices)
        # self.n_dices_left = n_init_dices
        self.n_max_dices: int = n_init_dices * n_players

    def __repr__(self) -> str:
        return f"Player(name={self.name})"

    @property
    def n_dices_left(self) -> int:
        return self._n_dices_left

    @property
    def dices(self) -> List[str]:
        return self._dices

    @n_dices_left.setter
    def n_dices_left(self, n_dices: int) -> None:
        if not (isinstance(n_dices, int) and n_dices >= 0):
            raise InvalidGameInput(n_dices, GameErrorMessage.INVALID_PLAYER_INPUT)
        self._dices: List[str] = random.choices(POSSIBLE_VALUES, k=n_dices)
        self._n_dices_left = n_dices

    def shuffle_dices(self) -> None:
        self._dices = random.choices(POSSIBLE_VALUES, k=self.n_dices_left)

    def take_one_dice_out(self) -> None:
        self.n_dices_left -= 1

    def choose_decision(self) -> Decision:
        pass

    def give_decision_to_other_player(
        self, decision: Union[Decision, None, str] = None
    ) -> Decision:
        if DEV_MODE:
            return decision
        else:  # TODO:User input
            is_input_decision_valid = False
            while not is_input_decision_valid:
                decision = input(
                    "Do you want to raise, call for a bluff or equal?[r/b/e]"
                )
                if decision in ["b", "e", "r", "bluff", "equal", "raise"]:
                    if decision in ["b", "bluff"]:
                        return Decision(bluff=True)
                    elif decision in ["e", "equal"]:
                        return Decision(equal=True)
                    elif decision in ["r", "raise"]:
                        raise_value = input(
                            "What is your raise?[Enter the number of dices then the value] eg: 5 PACO"
                        ).split(" ")
                        return Decision(
                            raise_=Raise(int(raise_value[0]), raise_value[1])
                        )
                    else:
                        raise NotImplementedError
                    is_input_decision_valid = True

    @property
    def n_max_dices(self) -> int:
        return self._n_max_dices

    @n_max_dices.setter
    def n_max_dices(self, n_max_dices: int) -> None:
        if isinstance(n_max_dices, int) and n_max_dices >= 0:
            self._n_max_dices = n_max_dices
        else:
            raise InvalidGameInput(
                n_max_dices, message=GameErrorMessage.INVALID_PLAYER_INPUT
            )

    # @property
    # def n_init_dices(self) -> int:
    #     return self._n_init_dices
    #
    # @n_init_dices.setter
    # def n_init_dices(self, n_dices) -> None:
    #     if not (isinstance(n_dices, int) and n_dices > 0):
    #         raise InvalidGameInput(n_dices, GameErrorMessage.INVALID_PLAYER_INPUT)
    #     self._n_init_dices = n_dices

    @property
    def n_players(self) -> int:
        return self._n_players

    @n_players.setter
    def n_players(self, nb_players: int) -> None:
        if not (isinstance(nb_players, int) and nb_players > 1):
            raise InvalidGameInput(nb_players, GameErrorMessage.INVALID_PLAYER_INPUT)
        self._n_players = nb_players
