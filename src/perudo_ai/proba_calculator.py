import math
from typing import *
from constants import *
from math import factorial as fact
from perudo_ai.custom_exceptions_and_errors import GameErrorMessage, InvalidGameInput
from scipy.stats import norm
from perudo_ai.decision import Decision
import pandas as pd
from collections import defaultdict

__all__ = [
    "calc_discrete_proba",
    "calc_proba_to_have_less_than_strictly",
    "calc_proba_to_have_more_than_or_equal",
    "find_n_k_adjusted",
    "calculate_probas_of_all_decisions",
]

# TOOD:
# 1. calculate probabilities of having exactly a number of dices + probabilities --> OK
# 2. calculate probabilities of having less than a number assert
# 3. calculate proba to have more than or equal (1-2.)
# 4. calculate confidence intervals
# 5. optimal decision
infinite_defaultdict = lambda: defaultdict(infinite_defaultdict)


def calculate_probas_of_all_decisions(
    total_nb_dices_left_in_game: int, player_dices: Dict[str, int]
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Dict[int, Dict[str, float]]]]:
    dices_details_per_player = Counter(player_dices)  # TODO:test
    probas = infinite_defaultdict()
    # { 'raise' : {1:{PACO:proba, '2 :,...., '6':proba}, 2:{PACO:proba, '2 :,...., '6':proba}, ..., total_nb_dices:{PACO:proba, '2 :,...., '6':proba}}
    #   'bluff': {1:{PACO:proba, '2 :,...., '6':proba}, 2:{PACO:proba, '2 :,...., '6':proba}, ..., total_nb_dices:{PACO:proba, '2 :,...., '6':proba}}
    for decision in ["raise", "bluff"]:
        for n_dices_bet_on in range(total_nb_dices_left_in_game + 1):
            for dice_face in POSSIBLE_VALUES:
                if decision == "raise":
                    proba = calc_proba_to_have_more_than_or_equal(
                        dice_face,
                        n_dices_bet_on,
                        total_nb_dices_left_in_game,
                        dices_details_per_player,
                    )
                elif decision == "bluff":
                    proba = calc_proba_to_have_less_than_strictly(
                        dice_face,
                        n_dices_bet_on,
                        total_nb_dices_left_in_game,
                        dices_details_per_player,
                    )
                # print(decision, n_dices_bet_on, dice_face, proba)
                probas[decision][n_dices_bet_on][dice_face] = proba

    probas_raise, probas_bluff = probas.get("raise"), probas.get("bluff")
    return (
        pd.DataFrame(probas_raise).unstack(),
        pd.DataFrame(probas_bluff).unstack(),
        probas,
    )


def get_confidence_interval(
    dice_face: str,
    n_dices_bet_on: int,  # n: number of dices that Player bets on
    total_nb_dices_left_in_game: int,  # n:  total number of dices left in the game
    dices_details_per_player: Dict[str, int],
    alpha: float = 0.05,
) -> Tuple[int, int]:
    n, _, p = find_n_k_adjusted(
        dice_face, n_dices_bet_on, total_nb_dices_left_in_game, dices_details_per_player
    )
    z = norm.ppf(1 - alpha / 2)
    return p - math.sqrt((p * (1 - p)) / n), p + math.sqrt((p * (1 - p)) / n)


def find_n_k_adjusted(
    dice_face: str,
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
