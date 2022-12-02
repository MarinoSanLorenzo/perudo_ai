import pytest
from perudo_ai.game import Game
from perudo_ai.custom_exceptions_and_errors import *
from perudo_ai.player import Player
from perudo_ai.decision import Decision, Raise
from typing import *
from constants import *


class TestGame:
    @pytest.mark.parametrize(
        "players, right_player_name, left_player_name, right_player_decision, left_player_decision, hand_nb, n_init_dices",
        [
            (
                [Player("Marc"), Player("Luc")],
                "Marc",
                "Luc",
                Decision(Raise(9, "3")),
                Decision(Raise(5, "PACO")),
                1,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(14, "4")),
                Decision(Raise(7, "PACO")),
                2,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(3, "5")),
                Decision(Raise(2, "PACO")),
                3,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(29, "6")),
                Decision(Raise(15, "PACO")),
                0,
                N_INIT_DICES_PER_PLAYER * 2,
            ),
        ],
    )
    def test_process_decisions_lower_number_of_dices_with_right_number_of_pacos(
        self,
        players: List[Player],
        right_player_name: str,
        left_player_name: str,
        right_player_decision: Decision,
        left_player_decision: Decision,
        hand_nb: int,
        n_init_dices: int,
    ) -> None:
        game = Game(players=players, n_init_dices=n_init_dices)
        right_player, left_player = game.players.get(
            right_player_name
        ), game.players.get(left_player_name)

        decision_details = game.process_decisions(
            (right_player, right_player_decision),
            (left_player, left_player_decision),
            hand_nb,
        )
        assert (
            decision_details.get("decision_outcome")
            == f"{left_player.left_player.name} to talk"
        )

    @pytest.mark.parametrize(
        "players, right_player_name, left_player_name, right_player_decision, left_player_decision, hand_nb, n_init_dices",
        [
            (
                [Player("Marc"), Player("Luc")],
                "Marc",
                "Luc",
                Decision(Raise(9, "PACO")),
                Decision(Raise(9, "3")),
                1,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(14, "3")),
                Decision(Raise(14, "2")),
                0,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(14, "4")),
                Decision(Raise(14, "3")),
                0,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(29, "4")),
                Decision(Raise(29, "4")),
                0,
                N_INIT_DICES_PER_PLAYER * 2,
            ),
        ],
    )
    def test_process_decisions_invalid_raise_lower_dice_value_when_same_number_dices(
        self,
        players: List[Player],
        right_player_name: str,
        left_player_name: str,
        right_player_decision: Decision,
        left_player_decision: Decision,
        hand_nb: int,
        n_init_dices: int,
    ) -> None:
        game = Game(players=players, n_init_dices=n_init_dices)
        right_player, left_player = game.players.get(
            right_player_name
        ), game.players.get(left_player_name)
        with pytest.raises(InvalidGameInput) as e:
            decisions_outcome = game.process_decisions(
                (right_player, right_player_decision),
                (left_player, left_player_decision),
                hand_nb,
            )
        assert GameErrorMessage.NO_LOWER_DICE_VALUE_WHEN_SAME_NUMBER_OF_DICES in str(
            e.value
        )

    @pytest.mark.parametrize(
        "dice_face1, dice_face2, outcome",
        [
            ("PACO", "2", True),
            ("3", "2", True),
            ("2", "2", False),
            ("2", "3", False),
            ("2", "4", False),
            ("2", "5", False),
            ("2", "6", False),
            ("3", "6", False),
            ("4", "6", False),
            ("5", "6", False),
            ("6", "6", False),
            ("6", "PACO", False),
            ("5", "2", True),
            ("5", "3", True),
            ("5", "4", True),
        ],
    )
    def test_dice_faces_relations(
        self, dice_face1: str, dice_face2: str, outcome: bool
    ) -> None:
        assert bool(dice_face1 > dice_face2) is outcome

    @pytest.mark.parametrize(
        "players, right_player_name, left_player_name, right_player_decision, left_player_decision, hand_nb, n_init_dices",
        [
            (
                [Player("Marc"), Player("Luc")],
                "Marc",
                "Luc",
                Decision(Raise(10, "2")),
                Decision(Raise(10, "3")),
                0,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(15, "3")),
                Decision(Raise(15, "4")),
                0,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(14, "6")),
                Decision(Raise(15, "6")),
                0,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(30, "3")),
                Decision(Raise(30, "4")),
                0,
                N_INIT_DICES_PER_PLAYER * 2,
            ),
        ],
    )
    def test_process_decisions_equal_num_max_dices_no_error(
        self,
        players: List[Player],
        right_player_name: str,
        left_player_name: str,
        right_player_decision: Decision,
        left_player_decision: Decision,
        hand_nb: int,
        n_init_dices: int,
    ) -> None:
        game = Game(players=players, n_init_dices=n_init_dices)
        right_player, left_player = game.players.get(
            right_player_name
        ), game.players.get(left_player_name)

        decisions_outcome = game.process_decisions(
            (right_player, right_player_decision),
            (left_player, left_player_decision),
            hand_nb,
        )

    @pytest.mark.parametrize(
        "players, right_player_name, left_player_name, right_player_decision, left_player_decision, hand_nb, n_init_dices",
        [
            (
                [Player("Marc"), Player("Luc")],
                "Marc",
                "Luc",
                Decision(Raise(11, "2")),
                Decision(Raise(11, "3")),
                0,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(16, "3")),
                Decision(Raise(14, "4")),
                0,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(14, "3")),
                Decision(Raise(16, "4")),
                0,
                N_INIT_DICES_PER_PLAYER,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(31, "3")),
                Decision(Raise(31, "4")),
                0,
                N_INIT_DICES_PER_PLAYER * 2,
            ),
        ],
    )
    def test_process_decisions_invalid_raise_more_dices_than_left(
        self,
        players: List[Player],
        right_player_name: str,
        left_player_name: str,
        right_player_decision: Decision,
        left_player_decision: Decision,
        hand_nb: int,
        n_init_dices: int,
    ) -> None:
        game = Game(players=players, n_init_dices=n_init_dices)
        right_player, left_player = game.players.get(
            right_player_name
        ), game.players.get(left_player_name)
        with pytest.raises(InvalidGameInput) as e:
            decisions_outcome = game.process_decisions(
                (right_player, right_player_decision),
                (left_player, left_player_decision),
                hand_nb,
            )
        assert GameErrorMessage.RAISE_EXCEED_TOTAL_NB_DICES_LEFT in str(e.value)

    @pytest.mark.parametrize(
        "players, right_player_name, left_player_name, right_player_decision, left_player_decision, hand_nb",
        [
            (
                [Player("Marc"), Player("Luc")],
                "Marc",
                "Luc",
                Decision(Raise(5, "PACO")),
                Decision(Raise(5, "3")),
                0,
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(6, "PACO")),
                Decision(Raise(6, "4")),
                0,
            ),
        ],
    )
    def test_process_decisions_invalid_raise_paco_first_round(
        self,
        players: List[Player],
        right_player_name: str,
        left_player_name: str,
        right_player_decision: Decision,
        left_player_decision: Decision,
        hand_nb: int,
    ) -> None:
        game = Game(players=players)
        right_player, left_player = game.players.get(
            right_player_name
        ), game.players.get(left_player_name)
        with pytest.raises(InvalidGameInput) as e:
            decisions_outcome = game.process_decisions(
                (right_player, right_player_decision),
                (left_player, left_player_decision),
                hand_nb,
            )
        assert GameErrorMessage.NO_PACO_WHEN_STARTING_ROUND in str(e.value)

    @pytest.mark.parametrize(
        "players, right_player_name, left_player_name, right_player_decision, left_player_decision",
        [
            (
                [Player("Marc"), Player("Luc")],
                "Marc",
                "Luc",
                Decision(Raise(5, "2")),
                Decision(Raise(5, "3")),
            ),
            (
                [Player("Marc"), Player("Luc"), Player("Louis")],
                "Marc",
                "Louis",
                Decision(Raise(6, "3")),
                Decision(Raise(6, "4")),
            ),
        ],
    )
    def test_process_decisions_raise(
        self,
        players: List[Player],
        right_player_name: str,
        left_player_name: str,
        right_player_decision: Decision,
        left_player_decision: Decision,
    ) -> None:

        hand_nb = 0
        game = Game(players=players)
        right_player, left_player = game.players.get(
            right_player_name
        ), game.players.get(left_player_name)
        decisions_outcome = game.process_decisions(
            (right_player, right_player_decision),
            (left_player, left_player_decision),
            hand_nb,
        )
        assert isinstance(decisions_outcome, dict)
        assert decisions_outcome.get("right_player_decision") == right_player_decision
        assert decisions_outcome.get("left_player_decision") == left_player_decision
        assert decisions_outcome.get("right_player_name") == right_player.name
        assert decisions_outcome.get("left_player_name") == left_player.name
        assert (
            decisions_outcome.get("decision_outcome")
            == f"{left_player.left_player.name} to talk"
        )
        assert decisions_outcome.get("is_round_finished") == False
        assert decisions_outcome.get("hand_nb") == hand_nb
        assert decisions_outcome.get("dices_details") == None
        assert decisions_outcome.get("total_dices") == None

    @pytest.mark.parametrize(
        "n_players, n_init_dices",
        [
            (-N_PLAYERS, -N_INIT_DICES_PER_PLAYER),
            (-10, N_INIT_DICES_PER_PLAYER),
            (8, -N_INIT_DICES_PER_PLAYER),
            (1, N_INIT_DICES_PER_PLAYER),
            (2, 0),
            (0, 0),
            (-1, -1),
        ],
    )
    def test_init_dices_game_invalid_input_error(
        self, n_players: int, n_init_dices: int
    ) -> None:
        with pytest.raises((TypeError, ValueError, InvalidGameInput)) as e:
            Game(players=n_players, n_init_dices=n_init_dices)

        assert (
            GameErrorMessage.INVALID_GAME_INPUT in str(e.value)
            or GameErrorMessage.INVALID_PLAYER_INPUT in str(e.value)
            or GameErrorMessage.LESS_THAN_TWO_PLAYERS in str(e.value)
        )

    @pytest.mark.parametrize(
        "game, n_players, n_init_dices",
        [
            (Game(), N_PLAYERS, N_INIT_DICES_PER_PLAYER),
            (Game(players=10), 10, N_INIT_DICES_PER_PLAYER),
            (Game(players=8), 8, N_INIT_DICES_PER_PLAYER),
            (Game(players=2, n_init_dices=1), 2, 1),
        ],
    )
    def test_n_max_dices_in_game(
        self, game: Game, n_players: int, n_init_dices: int
    ) -> None:
        assert len(list(game.players.values())[0].dices) == n_init_dices, "1"
        assert list(game.players.values())[0].n_dices_left == n_init_dices, "2"
        assert game.n_max_dices == n_init_dices * n_players, "3"

    def test_everyone_has_neighboor(self):
        game = Game(players=[Player("Marc"), Player("Luc"), Player("Paul")])
        assert game.players.get("Marc").left_player.name == "Paul"
        assert game.players.get("Luc").left_player.name == "Marc"
        assert game.players.get("Paul").left_player.name == "Luc"

    @pytest.mark.parametrize(
        "players, n_dices",
        [
            ([Player() for player in range(8)], 8 * N_INIT_DICES_PER_PLAYER),
            ([Player() for player in range(10)], 10 * N_INIT_DICES_PER_PLAYER),
            ([Player() for player in range(100)], 100 * N_INIT_DICES_PER_PLAYER),
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
        with pytest.raises((ValueError, InvalidGameInput)) as e:
            Game(players)
        assert GameErrorMessage.UNIQUE_PLAYERS_NAME in str(e.value)

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
        with pytest.raises((TypeError, InvalidGameInput)) as e:
            Game(players)
        assert GameErrorMessage.INVALID_PLAYERS_TYPE in str(e.value)

    @pytest.mark.parametrize("players", [(1), (0), -(1), ([Player()])])
    def test_initiate_game_with_less_than_two_players(
        self, players: Union[int, List[Player]]
    ) -> None:
        with pytest.raises((ValueError, InvalidGameInput)) as e:
            Game(players)

        assert GameErrorMessage.LESS_THAN_TWO_PLAYERS in str(e.value)
