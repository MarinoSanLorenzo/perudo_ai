import math
from typing import *
from constants import *
from math import factorial as fact
from perudo_ai.custom_exceptions_and_errors import GameErrorMessage, InvalidGameInput

__all__ = [
    "calc_discrete_proba",
    "calc_proba_to_have_less_than_strictly",
    "calc_proba_to_have_more_than_or_equal",
    "find_n_k_adjusted",
]

# TOOD:
# 1. calculate probabilities of having exactly a number of dices + probabilities --> OK
# 2. calculate probabilities of having less than a number assert
# 3. calculate proba to have more than or equal (1-2.)
# 4. calculate confidence intervals
# 5. optimal decision
def find_n_k_adjusted(
    dice_face: str,  # raise
    n_dices_bet_on: int,  # n: number of dices that Player bets on
    total_nb_dices_left_in_game: int,  # n:  total number of dices left in the game
    dices_details_per_player: Dict[str, int],
) -> Tuple[int, int]:
    if n_dices_bet_on > total_nb_dices_left_in_game:  # handle issues
        raise InvalidGameInput(GameErrorMessage.RAISE_EXCEED_TOTAL_NB_DICES_LEFT)
    p = 1 / 3 if dice_face != PACO else 1 / 6
    nb_pacos = dices_details_per_player.get(PACO, 0)
    if dice_face != PACO:
        n_dices_bet_on_adjusted = max(
            n_dices_bet_on - dices_details_per_player.get(dice_face, 0) - nb_pacos, 0
        )  # k_adjusted
    else:
        n_dices_bet_on_adjusted = max(n_dices_bet_on - nb_pacos, 0)
    total_nb_dices_left_in_game_adjusted = total_nb_dices_left_in_game - sum(
        list(dices_details_per_player.values())
    )  # n_adjusted
    n = total_nb_dices_left_in_game_adjusted
    k = n_dices_bet_on_adjusted
    return n, k, p


def calc_proba_exactly_equal_to(n: int, k: int, p: float) -> float:
    if (n >= k) and (n >= 0) and (k >= 0):
        proba_discrete_of_having_exactly_k_dices = (
            (fact(n) / (fact(k) * fact(n - k))) * (p**k) * ((1 - p) ** (n - k))
        )  # discrete binomial probability
        return proba_discrete_of_having_exactly_k_dices
    else:
        return 0


def calc_proba_to_have_more_than_or_equal(
    dice_face: str,  # raise
    n_dices_bet_on: int,
    total_nb_dices_left_in_game: int,
    dices_details_per_player: Dict[str, int],
) -> float:
    n, k, p = find_n_k_adjusted(
        dice_face, n_dices_bet_on, total_nb_dices_left_in_game, dices_details_per_player
    )
    if k == 0:
        return 1
    return sum(
        [calc_proba_exactly_equal_to(n, n_dice, p) for n_dice in range(k, n + 1)]
    )


def calc_proba_to_have_less_than_strictly(
    dice_face: str,  # bluff
    n_dices_bet_on: int,
    total_nb_dices_left_in_game: int,
    dices_details_per_player: Dict[str, int],
) -> float:
    n, k, p = find_n_k_adjusted(
        dice_face, n_dices_bet_on, total_nb_dices_left_in_game, dices_details_per_player
    )
    return sum([calc_proba_exactly_equal_to(n, n_dice, p) for n_dice in range(k)])


def calc_discrete_proba(
    dice_face: str,
    n_dices_bet_on: int,
    total_nb_dices_left_in_game: int,
    dices_details_per_player: Dict[str, int],
) -> float:
    n, k, p = find_n_k_adjusted(
        dice_face, n_dices_bet_on, total_nb_dices_left_in_game, dices_details_per_player
    )
    return calc_proba_exactly_equal_to(n, k, p)
