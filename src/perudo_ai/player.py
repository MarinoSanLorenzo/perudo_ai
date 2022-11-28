from constants import *
import random
import names
from typing import *

POSSIBLE_VALUES = params.get(Constants.POSSIBLE_VALUES)
N_INIT_DICES = params.get(Constants.N_INIT_DICES)


class Player:
    def __init__(self, name: Union[str, None] = None) -> None:
        if not name:
            name = names.get_full_name()
        self.name = name
        self._dices = random.choices(POSSIBLE_VALUES, k=N_INIT_DICES)
        self._n_dices_left = N_INIT_DICES

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
