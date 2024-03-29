from perudo_ai.perudo_ai import *
from constants import *
import pytest
from perudo_ai.player import Player
from perudo_ai.game import Game
from typing import *
from tests.fixtures import *
import random
from perudo_ai.proba_calculator import calculate_probas_of_all_decisions
from perudo_ai.decision import Decision, Raise
from perudo_ai.custom_exceptions_and_errors import InvalidGameInput


class TestPerudoAI:
    def test_check_is_decision_valid(self) -> None:
        game = Game(players=[PerudoAI("AI"), PerudoAI("Marc")], n_init_dices=2)
        assert game.hand_nb == 0
        ai = game.players.get("AI")
        right_player = ai
        left_player = right_player.left_player
        total_nb_dices_left_in_game = game.total_nb_dices
        hand_nb = game.hand_nb
        potential_right_player_decision = Decision(Raise(n_dices=0, dice_face="2"))
        right_player_decision_pair = (right_player, potential_right_player_decision)
        left_player_decision_pair = (left_player, None)
        total_nb_dices = game.total_nb_dices

        is_decision_valid_output = check_if_decision_is_valid(
            hand_nb=hand_nb,
            right_player_decision_pair=right_player_decision_pair,
            left_player_decision_pair=left_player_decision_pair,
            total_nb_dices=total_nb_dices,
        )

        assert is_decision_valid_output == True

    def test_take_optimal_decision_with_valid_decisions(self) -> None:  # TODO: test
        game = Game(players=[PerudoAI("AI"), PerudoAI("Marc")], n_init_dices=2)
        assert game.hand_nb == 0
        ai = game.players.get("AI")

        right_player = ai
        total_nb_dices_left_in_game = game.total_nb_dices
        hand_nb = game.hand_nb
        assert hand_nb == 0
        right_player_decision_pair = (right_player, None)
        left_player_decision_pair = (None, None)

        right_player_decision = right_player.take_optimal_decision(
            hand_nb,
            total_nb_dices_left_in_game,
            right_player_decision_pair=right_player_decision_pair,
            left_player_decision_pair=left_player_decision_pair,
        )
        assert isinstance(right_player_decision, Decision)
        left_player = right_player.left_player
        left_player_decision = left_player.take_optimal_decision(
            hand_nb,
            total_nb_dices_left_in_game,
            right_player_decision_pair=(right_player, right_player_decision),
            left_player_decision_pair=(left_player, None),
        )
        assert isinstance(left_player_decision, Decision)
        right_player = left_player
        right_player_decision = left_player_decision
        left_player = right_player.left_player

        # left_player_decision = left_player.take_optimal_decision(
        #     hand_nb, total_nb_dices_left_in_game,
        #     right_player_decision_pair=(right_player, right_player_decision),
        #     left_player_decision_pair=(left_player, None)
        # )
        # assert isinstance(left_player_decision, Decision)
        #
        # right_player = left_player
        # right_player_decision = left_player_decision
        # left_player = right_player.left_player
        #
        # left_player_decision = left_player.take_optimal_decision(
        #     hand_nb, total_nb_dices_left_in_game,
        #     right_player_decision_pair=(right_player, right_player_decision),
        #     left_player_decision_pair=(left_player, None)
        # )
        # assert isinstance(left_player_decision, Decision)

    @pytest.mark.parametrize(
        "is_valid_raise, is_valid_bluff,  right_player_decision, left_player_decision",
        [
            (
                False,
                False,
                Decision(Raise(n_dices=1, dice_face=PACO)),
                Decision(Raise(n_dices=1, dice_face="1")),
            ),
            (
                True,
                True,
                Decision(Raise(n_dices=1, dice_face="3")),
                Decision(Raise(n_dices=1, dice_face=PACO)),
            ),
            (
                False,
                False,
                Decision(Raise(n_dices=5, dice_face="3")),
                Decision(Raise(n_dices=2, dice_face=PACO)),
            ),
            (
                False,
                True,
                Decision(Raise(n_dices=4, dice_face="3")),
                Decision(Raise(n_dices=5, dice_face="3")),
            ),
            (
                True,
                True,
                Decision(Raise(n_dices=3, dice_face="3")),
                Decision(Raise(n_dices=2, dice_face=PACO)),
            ),
            (
                False,
                True,
                Decision(Raise(n_dices=3, dice_face="3")),
                Decision(Raise(n_dices=3, dice_face="2")),
            ),
        ],
    )
    def test_take_valid_decisions(
        self,
        is_valid_raise: bool,
        is_valid_bluff: bool,
        right_player_decision: Decision,
        left_player_decision: Decision,
    ) -> None:
        game = Game(players=[PerudoAI("AI"), PerudoAI("Marc")], n_init_dices=2)
        assert game.hand_nb == 0
        ai = game.players.get("AI")
        assert ai.name == "AI"
        right_player = ai
        left_player = right_player.left_player
        total_nb_dices_left_in_game = game.total_nb_dices
        df_probas_raise, df_probas_bluff, probas = calculate_probas_of_all_decisions(
            total_nb_dices_left_in_game, right_player.dices
        )
        total_nb_dices = game.total_nb_dices
        is_decision_valid_output = check_if_decision_is_valid(
            game.hand_nb,
            (right_player, right_player_decision),
            (left_player, left_player_decision),
            game.total_nb_dices,
        )

        assert is_valid_raise == is_decision_valid_output
        df_probas_raise, df_probas_bluff = add_valid_decision(
            df_probas_raise,
            df_probas_bluff,
            game.hand_nb,
            (right_player, right_player_decision),
            (left_player, left_player_decision),
            game.total_nb_dices,
        )
        assert "is_decision_valid" in df_probas_raise
        assert "is_decision_valid" in df_probas_bluff
        if not is_valid_raise:
            assert df_probas_raise.is_decision_valid.unique()[0] == is_valid_raise
        if not is_valid_bluff:
            assert df_probas_bluff.is_decision_valid.unique()[0] == is_valid_bluff

    def test_take_optimal_decision_first_hand(self, game_with_ai: Game) -> None:
        game = game_with_ai
        ai = game.players.get("AI")
        assert ai.name == "AI"

        right_player = ai
        total_nb_dices_left_in_game = game.total_nb_dices
        hand_nb = game.hand_nb
        assert hand_nb == 0
        right_player_decision = right_player.take_optimal_decision(
            hand_nb,
            total_nb_dices_left_in_game,
            right_player_decision_pair=(right_player, None),
            left_player_decision_pair=(right_player.left_player, None),
        )
        assert isinstance(right_player_decision, Decision)
        assert right_player_decision.raise_.n_dices == 4
        assert right_player_decision.raise_.dice_face == "2"
        left_player = right_player.left_player
        left_player_decision = Decision(Raise(n_dices=4, dice_face="3"))
        game.process_decisions(
            (right_player, right_player_decision), (left_player, left_player_decision)
        )
        right_player, right_player_decision = left_player, left_player_decision
        left_player, left_player_decision = right_player.left_player, Decision(
            Raise(n_dices=5, dice_face="2")
        )
        game.process_decisions(
            (right_player, right_player_decision), (left_player, left_player_decision)
        )
        right_player, right_player_decision = left_player, left_player_decision
        left_player = right_player.left_player
        hand_nb = game.hand_nb
        assert hand_nb == 2
        left_player_decision = left_player.take_optimal_decision(
            hand_nb, total_nb_dices_left_in_game, (right_player, right_player_decision)
        )
        game.process_decisions(
            (right_player, right_player_decision), (left_player, left_player_decision)
        )
        right_player, right_player_decision = left_player, left_player_decision
        left_player, left_player_decision = right_player.left_player, Decision(
            bluff=True
        )
        game.process_decisions(
            (right_player, right_player_decision), (left_player, left_player_decision)
        )

    def test_initialize_ai(self) -> None:
        ai = PerudoAI()
        assert ai.name is not None
        assert ai.n_dices_left == N_INIT_DICES_PER_PLAYER
        assert ai.n_players == N_PLAYERS
