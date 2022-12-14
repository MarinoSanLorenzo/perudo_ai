"""
Module testing the proba calculator module
"""

import pytest
from math import factorial as fact
import math
from perudo_ai.proba_calculator import *
from constants import *
from typing import *

# install with pip install -e src/


class TestProbaCalculator:
    @pytest.mark.parametrize(
        "dice_face, n_dices, n_dices_left_in_game, dices_details_per_player, proba_expected",
        [
            ("2", 2, 2, {"2": 1}, 1 / 3),
            (PACO, 2, 2, {PACO: 1}, 1 / 6),
            (PACO, 10, 10, {"3": 1}, 0),
        ],
    )
    def test_calc_discrete_proba4(
        self,
        dice_face: str,
        n_dices: int,
        n_dices_left_in_game: int,
        dices_details_per_player: Dict[str, int],
        proba_expected: float,
    ) -> None:
        proba_discrete_of_having_exactly_k_dices = calc_discrete_proba(
            dice_face, n_dices, n_dices_left_in_game, dices_details_per_player
        )
        assert proba_discrete_of_having_exactly_k_dices >= 0
        assert proba_discrete_of_having_exactly_k_dices <= 1
        assert math.isclose(proba_discrete_of_having_exactly_k_dices, proba_expected)

    @pytest.mark.parametrize(
        "dice_face, n_dices, n_dices_left_in_game, dices_details_per_player",
        [
            ("2", 5, 20, {"3": 5}),
            (PACO, 5, 20, {"3": 5}),
            (PACO, 10, 10, {"3": 5}),
        ],
    )
    def test_calc_discrete_proba3(
        self,
        dice_face: str,
        n_dices: int,
        n_dices_left_in_game: int,
        dices_details_per_player: Dict[str, int],
    ) -> None:
        proba_discrete_of_having_exactly_k_dices = calc_discrete_proba(
            dice_face, n_dices, n_dices_left_in_game, dices_details_per_player
        )
        assert proba_discrete_of_having_exactly_k_dices >= 0
        assert proba_discrete_of_having_exactly_k_dices <= 1

    def test_calc_discrete_proba2(self) -> None:
        # dice_face, n_dices, n_dices_left_in_game, dices_details_per_player
        data_1 = ("2", 5, 20, {"3": 5})
        data_2 = (PACO, 5, 20, {"3": 5})
        data_3 = (PACO, 10, 10, {"3": 5})
        proba_1 = calc_discrete_proba(*data_1)
        proba_2 = calc_discrete_proba(*data_2)
        proba_3 = calc_discrete_proba(*data_3)

        assert proba_1 >= 0
        assert proba_1 <= 1

        assert proba_2 >= 0
        assert proba_2 <= 1

        assert proba_3 >= 0
        assert proba_3 <= 1

        assert proba_1 > proba_2
        assert math.isclose(proba_3, 0)

    def test_calc_discrete_proba(self) -> None:
        n_dices_left_in_game = 20  # n
        dices_details_per_player = {"2": 5}
        n_dices = 6  # k
        dice_face = "2"
        p = 1 / 3 if dice_face != PACO else 1 / 6
        assert math.isclose(p, 1 / 3)

        n_dices_adjusted = max(
            n_dices - dices_details_per_player.get(dice_face), 0
        )  # k_adjusted
        assert n_dices_adjusted == 1
        n_dices_left_in_game_adjusted = n_dices_left_in_game - sum(
            list(dices_details_per_player.values())
        )  # n_adjusted
        assert n_dices_left_in_game_adjusted == 15
        n = n_dices_left_in_game_adjusted
        k = n_dices_adjusted
        proba_discrete_of_having_exactly_k_dices_of_some_value = (
            (fact(n) / (fact(k) * fact(n - k))) * (p**k) * ((1 - p) ** (n - k))
        )
        assert proba_discrete_of_having_exactly_k_dices_of_some_value >= 0
        assert proba_discrete_of_having_exactly_k_dices_of_some_value <= 1

        assert (
            calc_discrete_proba(
                dice_face, n_dices, n_dices_left_in_game, dices_details_per_player
            )
            == proba_discrete_of_having_exactly_k_dices_of_some_value
        )
