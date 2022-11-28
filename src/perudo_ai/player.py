from constants import *
import random
import names
from typing import *
from perudo_ai.decision import Decision, Raise


class Player:
    def __init__(self, name: Union[str, None] = None) -> None:
        if not name:
            name = names.get_full_name()
        self.name = name
        self._dices = random.choices(POSSIBLE_VALUES, k=N_INIT_DICES)
        self._n_dices_left = N_INIT_DICES

    def __repr__(self) -> str:
        return f'Player(name={self.name})'


    @property
    def n_dices_left(self) -> int:
        return self._n_dices_left

    @property
    def dices(self) -> List[str]:
        return self._dices

    @n_dices_left.setter
    def n_dices_left(self, n_dices: int) -> None:
        if n_dices < 0:
            self._n_dices_left = 0
        else:
            self._n_dices_left = n_dices

    def shuffle_dices(self) -> None:
        self._dices = random.choices(POSSIBLE_VALUES, k=self.n_dices_left)

    def take_one_dice_out(self) -> None:
        self.n_dices_left -= 1

    def take_decision(self, decision:Union[Decision, None, str]=None) -> Decision:
        if DEV_MODE:
            return decision
        else:
            is_input_decision_valid = False
            while not is_input_decision_valid:
                decision = input('Do you want to raise, call for a bluff or equal?[r/b/e]')
                if decision in ['b', 'e', 'r', 'bluff', 'equal', 'raise']:
                    if decision in ['b', 'bluff']:
                        return Decision(bluff=True)
                    elif decision in ['e', 'equal']:
                        return Decision(equal=True)
                    elif decision in ['r', 'raise']:
                        raise_value = input('What is your raise?[Enter the number of dices then the value] eg: 5 PACO').split(' ')
                        return Decision(raise_=Raise(int(raise_value[0]), raise_value[1]))
                    else:
                        raise NotImplementedError
                    is_input_decision_valid = True





