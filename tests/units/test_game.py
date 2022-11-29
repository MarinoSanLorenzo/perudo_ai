import pytest
from perudo_ai.game import Game, GameErrorMessage
from perudo_ai.player import Player
from typing import *
from constants import *


class TestGame:
    def test_next_round(self) -> None:
        game = Game(players=3)
        game.start_round()

    def test_everyone_has_neighboor(self):
        game = Game(players=[Player("Marc"), Player("Luc"), Player("Paul")])
        assert game.players[0].left_neighbor.name == "Paul"
        assert game.players[1].left_neighbor.name == "Marc"
        assert game.players[2].left_neighbor.name == "Luc"

    @pytest.mark.parametrize(
        "players, n_dices",
        [
            ([Player() for player in range(8)], 8 * N_INIT_DICES),
            ([Player() for player in range(10)], 10 * N_INIT_DICES),
            ([Player() for player in range(100)], 100 * N_INIT_DICES),
        ],
    )
    def test_total_nb_dices(
        self, players: Union[int, List[Player]], n_dices: int
    ) -> None:
        game = Game(players=players)
        assert game.total_nb_dices == n_dices

    @pytest.mark.parametrize("players", [([Player() for player in range(8)]), (8)])
    def test_instantiate_game(self, players: Union[int, List[Player]]) -> None:

        game = Game(players=players)

        assert len(game.players) == 8

    @pytest.mark.parametrize(
        "players",
        [
            ([Player("Test"), Player("Mark"), Player("Test")]),
            ([Player("Test"), Player("Test")]),
        ],
    )
    def test_players_with_same_names_error(self, players: Union[int, List[Player]]):
        with pytest.raises(ValueError) as e:
            Game(players)
        assert str(e.value) == GameErrorMessage.UNIQUE_PLAYERS_NAME

    @pytest.mark.skip(reason="Not yet implemented")
    def test_check_unique_names_when_players_instantiate_with_integer(self):
        pass

    @pytest.mark.parametrize(
        "players",
        [([Player() for _ in range(3)] + [2]), (["player", "player2", Player()])],
    )
    def test_initiate_game_with_invalid_type_players(
        self, players: Union[int, List[Player]]
    ) -> None:
        with pytest.raises(TypeError) as e:
            Game(players)
        assert str(e.value) == GameErrorMessage.INVALID_PLAYERS_TYPE

    @pytest.mark.parametrize("players", [(1), (0), -(1), ([Player()])])
    def test_initiate_game_with_less_than_two_players(
        self, players: Union[int, List[Player]]
    ) -> None:
        with pytest.raises(ValueError) as e:
            Game(players)

        assert str(e.value) == GameErrorMessage.LESS_THAN_TWO_PLAYERS
