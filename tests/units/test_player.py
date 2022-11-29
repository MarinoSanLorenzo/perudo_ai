import pytest
from perudo_ai.player import Player
from perudo_ai.decision import Decision, Raise
import random
from constants import *
import names

POSSIBLE_VALUES = params.get(Constants.POSSIBLE_VALUES)
N_INIT_DICES = params.get(Constants.N_INIT_DICES)


@pytest.fixture
def player() -> Player:
    return Player()


class TestPlayer:
    def test_player_give_decision_to_other_player(self) -> None:
        player1 = Player("Player 1")
        player2 = Player("Player 2")
        decision = player1.take_decision(player2, Decision(Raise(6, "PACO")))
        assert isinstance(decision, Decision)
        assert isinstance(decision.raise_, Raise)

    def test_take_one_dice_out(self, player: Player) -> None:
        for n_dices_left in range(N_INIT_DICES, -1, -1):
            assert player.n_dices_left == n_dices_left
            player.take_one_dice_out()
        player.take_one_dice_out()
        assert player.n_dices_left == 0

    @pytest.mark.parametrize(
        "n_dices_lost, n_dices_left",
        [
            (N_INIT_DICES + 1, 0),
            (0, N_INIT_DICES - 0),
            (1, N_INIT_DICES - 1),
            (2, N_INIT_DICES - 2),
            (3, N_INIT_DICES - 3),
            (4, N_INIT_DICES - 4),
            (5, N_INIT_DICES - 5),
        ],
    )
    def test_dices_setter(
        self, player: Player, n_dices_lost: int, n_dices_left: int
    ) -> None:
        player.n_dices_left -= n_dices_lost
        assert player.n_dices_left == n_dices_left

    def test_shuffle_dices(self) -> None:
        player = Player()
        old_dices = Player.dices
        player.shuffle_dices()
        assert player.dices != old_dices

    def test_init_player_random_name(self) -> None:
        player = Player()
        assert isinstance(player.name, str)

    def test_init_dices_player(self) -> None:

        dices = random.choices(POSSIBLE_VALUES, k=N_INIT_DICES)

        player = Player("player-test")
        assert len(player.dices) == len(dices)
        assert len(player.dices) == N_INIT_DICES
        for dice in player.dices:
            assert dice in POSSIBLE_VALUES
        assert player.n_dices_left == N_INIT_DICES
