"""
Module testing the proba calculator module
"""

import pytest
from math import factorial as fact
import math
from perudo_ai.proba_calculator import *
from constants import *
from typing import *
from perudo_ai.decision import Decision, Raise
from perudo_ai.game import Game
from tests.fixtures import *
import random
from collections import Counter, defaultdict
from pprint import pprint
import pandas as pd

# install with pip install -e src/


class TestProbaCalculator:
    def test_calculate_probas_of_all_decisions(self, game: Game) -> None:

        right_player = random.choice(list(game.players.values()))
        total_nb_dices_left_in_game = game.total_nb_dices
        df_probas_raise, df_probas_bluff, probas = calculate_probas_of_all_decisions(
            total_nb_dices_left_in_game, right_player.dices
        )

        best_n_dices, best_dice_face = max(
            df_probas_raise[df_probas_raise == max(df_probas_raise)].index
        )
        decision_right_player = Decision(
            Raise(n_dices=best_dice_face, dice_face=best_dice_face)
        )
        assert "raise" in probas
        assert "bluff" in probas
        for n_dices_bet_on in range(total_nb_dices_left_in_game + 1):
            assert probas.get("raise")
            assert probas.get("bluff")
            for dice_face in POSSIBLE_VALUES:
                assert probas.get("raise").get(n_dices_bet_on)
                assert probas.get("bluff").get(n_dices_bet_on)
        assert best_n_dices == 4
        if (right_player.name == "Marc") or (right_player.name == "Luc"):
            assert (
                best_dice_face == "2"
            ), f"{right_player.name}\n{  df_probas_raise[df_probas_raise == max(df_probas_raise)]}"
        if right_player.name == "Jean":
            assert (
                best_dice_face == "3"
            ), f"{right_player.name}\n{  df_probas_raise[df_probas_raise == max(df_probas_raise)]}"

    @pytest.mark.parametrize(
        "dice_face, n_dices_bet_on, total_nb_dices_left_in_game, dices_details_per_player, proba_raise_expected, proba_bluff_expected",
        [
            (
                "2",
                2,
                2,
                {"2": 1},
                1 / 3,
                2 / 3,
            ),  # P[raise] = P[N_2 >=2 | N_DICES=2, D1="2"] = P[N_2 >=1 | N_DICES=1] = P[N_2=1] = 1/3
            # P[bluff] =  P[N_2 < 2 | N_DICES=2, D1="2"] = P[N_2 <1 | N_DICES=1] = P[N_2=0] = 2/3
            (
                PACO,
                2,
                2,
                {PACO: 1},
                1 / 6,
                5 / 6,
            ),  # P[bluff] =  P[N_paco < 2 | N_DICES=2, D1="PACO"] = P[N_PACO <1 | N_DICES=1] = P[N_PACO=0] = 5/3
            (
                PACO,
                2,
                2,
                {"3": 1},
                0,
                1,
            ),  # P(N_PACO<2 | N_DICES = 2, D1="3") = P(N_PACO<1 | N_DICES = 1) = P(N_PACO = 0 | N_DICES = 1)
            # P[bluff] = P(N_PACO<2 | N_DICES = 2, D1="3") = P(N_PACO<2 | N_DICES = 1) = P(N_PACO = 1 | N_DICES = 1)+ P(N_PACO = 0 | N_DICES = 1) = 1/6 + 5/6
            (
                "5",
                5,
                5,
                {"3": 5},
                0,
                1,
            ),  # P(N_5<5 | N_DICES = 5, D1="3", D2="3",  D3="3",  D4="3",  D5="3") =  P(N_5=0 | N_DICES = 5, D1="3", D2="3",  D3="3",  D4="3",  D5="3")=1 + P(N_5=1 | N_DICES = 5, D1="3", D2="3",  D3="3",  D4="3",  D5="3")=0 + ....=
            (
                "5",
                4,
                4,
                {"5": 4},
                1,
                0,
            ),  # P(N_5<4 | N_DICES = 4, D1="5", D2="3",  D3="3",  D4="3") =  P(N_5 = 0  | N_DICES = 4, D1="5", D2="5",  D3="5",  D4="5") = 0  + .. P(N_5 = 3  | N_DICES = 4, D1="5", D2="5",  D3="5",  D4="5") = 0
            ("5", 4, 10, {"5": 5}, 1, 0),
        ],
    )
    def test_calc_proba_to_have_less_than_strictly(  # tTODO: finish
        self,
        dice_face: str,
        n_dices_bet_on: int,
        total_nb_dices_left_in_game: int,
        dices_details_per_player: Dict[str, int],
        proba_raise_expected: float,
        proba_bluff_expected: float,
    ) -> None:
        proba_raise = calc_proba_to_have_more_than_or_equal(
            dice_face,
            n_dices_bet_on,
            total_nb_dices_left_in_game,
            dices_details_per_player,
        )
        proba_bluff = calc_proba_to_have_less_than_strictly(
            dice_face,
            n_dices_bet_on,
            total_nb_dices_left_in_game,
            dices_details_per_player,
        )
        assert proba_bluff >= 0
        assert proba_bluff <= 1
        assert proba_raise >= 0
        assert proba_raise <= 1
        assert math.isclose(
            proba_raise, proba_raise_expected
        ), f"proba_raise={proba_raise} vs expected={proba_raise_expected}"
        assert math.isclose(
            proba_bluff, proba_bluff_expected
        ), f"proba_bluff={proba_bluff} vs expected={proba_bluff_expected}"
        # assert math.isclose(proba_bluff, 1-proba_expected), f'{proba_bluff}'
        # assert math.isclose(proba_raise+ proba_bluff, 1), f'{proba_raise+ proba_bluff}'

    @pytest.mark.parametrize(
        "dice_face, n_dices_bet_on, total_nb_dices_left_in_game, dices_details_per_player, proba_expected",
        [
            ("2", 2, 2, {"2": 1}, 1 / 3),
            (PACO, 2, 2, {PACO: 1}, 1 / 6),
            (PACO, 10, 10, {"3": 1}, 0),
        ],
    )
    def test_calc_discrete_proba4(
        self,
        dice_face: str,
        n_dices_bet_on: int,
        total_nb_dices_left_in_game: int,
        dices_details_per_player: Dict[str, int],
        proba_expected: float,
    ) -> None:
        proba_discrete_of_having_exactly_k_dices = calc_discrete_proba(
            dice_face,
            n_dices_bet_on,
            total_nb_dices_left_in_game,
            dices_details_per_player,
        )
        assert proba_discrete_of_having_exactly_k_dices >= 0
        assert proba_discrete_of_having_exactly_k_dices <= 1
        assert math.isclose(proba_discrete_of_having_exactly_k_dices, proba_expected)

    @pytest.mark.parametrize(
        "dice_face, n_dices_bet_on, total_nb_dices_left_in_game, dices_details_per_player",
        [
            ("2", 5, 20, {"3": 5}),
            (PACO, 5, 20, {"3": 5}),
            (PACO, 10, 10, {"3": 5}),
        ],
    )
    def test_calc_discrete_proba3(
        self,
        dice_face: str,
        n_dices_bet_on: int,
        total_nb_dices_left_in_game: int,
        dices_details_per_player: Dict[str, int],
    ) -> None:
        proba_discrete_of_having_exactly_k_dices = calc_discrete_proba(
            dice_face,
            n_dices_bet_on,
            total_nb_dices_left_in_game,
            dices_details_per_player,
        )
        assert proba_discrete_of_having_exactly_k_dices >= 0
        assert proba_discrete_of_having_exactly_k_dices <= 1

    def test_calc_discrete_proba2(self) -> None:
        # dice_face, n_dices_bet_on, total_nb_dices_left_in_game, dices_details_per_player
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
        total_nb_dices_left_in_game = 20  # n
        dices_details_per_player = {"2": 5}
        n_dices_bet_on = 6  # k
        dice_face = "2"
        p = 1 / 3 if dice_face != PACO else 1 / 6
        assert math.isclose(p, 1 / 3)

        n_dices_bet_on_adjusted = max(
            n_dices_bet_on - dices_details_per_player.get(dice_face), 0
        )  # k_adjusted
        assert n_dices_bet_on_adjusted == 1
        total_nb_dices_left_in_game_adjusted = total_nb_dices_left_in_game - sum(
            list(dices_details_per_player.values())
        )  # n_adjusted
        assert total_nb_dices_left_in_game_adjusted == 15
        n = total_nb_dices_left_in_game_adjusted
        k = n_dices_bet_on_adjusted
        proba_discrete_of_having_exactly_k_dices_of_some_value = (
            (fact(n) / (fact(k) * fact(n - k))) * (p**k) * ((1 - p) ** (n - k))
        )
        assert proba_discrete_of_having_exactly_k_dices_of_some_value >= 0
        assert proba_discrete_of_having_exactly_k_dices_of_some_value <= 1

        assert (
            calc_discrete_proba(
                dice_face,
                n_dices_bet_on,
                total_nb_dices_left_in_game,
                dices_details_per_player,
            )
            == proba_discrete_of_having_exactly_k_dices_of_some_value
        )
