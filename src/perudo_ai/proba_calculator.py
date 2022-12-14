import math
from typing import *
from constants import *
from math import factorial as fact

__all__ = ["calc_discrete_proba"]

# TOOD:
# 1. calculate probabilities of having exactly a number of dices + probabilities --> OK
# 2. calculate probabilities of having less than a number assert
# 3. calculate proba to have more than or equal (1-2.)
# 4. calculate confidence intervals
# 5. optimal decision

def calc_proba_to_have_more_than_or_equal(dice_face: str,
    n_dices: int,
    n_dices_left_in_game: int,
    dices_details_per_player: Dict[str, int],
) -> float:#TODO:test
    return 1- calc_proba_to_have_less_than_strictly(dice_face, n_dices, n_dices_left_in_game, dices_details_per_player)

def calc_proba_to_have_less_than_strictly(    dice_face: str,
    n_dices: int,
    n_dices_left_in_game: int,
    dices_details_per_player: Dict[str, int],
) -> float:#TODO:test
    return sum(list[calc_discrete_proba(dice_face, n_dices, n_dices_left_in_game, dices_details_per_player) for n_dice in range(n_dices)])

def calc_discrete_proba(
    dice_face: str,
    n_dices: int,
    n_dices_left_in_game: int,
    dices_details_per_player: Dict[str, int],
) -> float:
    p = 1 / 3 if dice_face != PACO else 1 / 6
    nb_pacos = dices_details_per_player.get(PACO, 0)
    if dice_face != PACO:
        n_dices_adjusted = max(
            n_dices - dices_details_per_player.get(dice_face, 0) - nb_pacos, 0
        )  # k_adjusted
    else:
        n_dices_adjusted = max(n_dices - nb_pacos, 0)
    n_dices_left_in_game_adjusted = n_dices_left_in_game - sum(
        list(dices_details_per_player.values())
    )  # n_adjusted
    n = n_dices_left_in_game_adjusted
    k = n_dices_adjusted
    if n < k:
        return 0
    else:
        proba_discrete_of_having_exactly_k_dices = (
            (fact(n) / (fact(k) * fact(n - k))) * (p**k) * ((1 - p) ** (n - k))
        )  # discrete binomial probability
        return proba_discrete_of_having_exactly_k_dices
