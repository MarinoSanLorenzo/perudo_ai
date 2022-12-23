from perudo_ai.perudo_ai import PerudoAI
from constants import *
import pytest
from perudo_ai.player import Player
from perudo_ai.game import Game
from typing import *
from tests.fixtures import *
import random
from perudo_ai.proba_calculator import calculate_probas_of_all_decisions
from perudo_ai.decision import Decision, Raise


class TestPerudoAI:
    def test_take_optimal_decision_first_hand(self, game_with_ai: Game) -> None:
        game = game_with_ai
        ai = game.players.get("AI")
        assert ai.name == "AI"

        right_player = ai
        total_nb_dices_left_in_game = game.total_nb_dices
        hand_nb = game.hand_nb
        assert hand_nb == 0
        right_player_decision = right_player.take_optimal_decision(
            hand_nb, total_nb_dices_left_in_game, right_player_decision=None
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
            hand_nb, total_nb_dices_left_in_game, right_player_decision
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
