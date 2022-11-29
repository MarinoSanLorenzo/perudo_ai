from typing import *


__all__ = ["Decision", "Raise"]


class Raise(NamedTuple):
    n_dices: int
    dice_face: str


class Decision(NamedTuple):
    raise_: Union[Raise, None] = None
    bluff: bool = False
    equal: bool = False  # calza
    # _BLUFF = "bluff"
    # _RAISE = "raise"
    # _EQUAL = "equal"
