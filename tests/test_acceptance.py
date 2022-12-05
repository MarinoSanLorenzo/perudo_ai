import pytest
from perudo_ai.game import *


@pytest.fixture
def number_players() -> int:
    return 8


class TestAcceptance:
    @pytest.mark.skip
    def test_initiate_game(self, number_players: int) -> None:
        game = Game(number_players=number_players)
        assert len(game.players) == number_players

    @pytest.mark.skip
    def test_random_dices_shuffling(self) -> None:
        game = Game(number_players=number_players)
        game.next_round()
        for player in game.players:
            player.shuffle_dices()
        game.next_round()
        for player in game.players:
            player.shuffle_dices()
        assert len(game.history) == 2
