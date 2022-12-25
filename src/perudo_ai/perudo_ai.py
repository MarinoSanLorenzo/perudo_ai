from perudo_ai.player import Player
from perudo_ai.decision import Decision, Raise
from constants import *
from typing import *
from perudo_ai.proba_calculator import calculate_probas_of_all_decisions
from perudo_ai.custom_exceptions_and_errors import InvalidGameInput, GameErrorMessage
import math

__all__ = ["PerudoAI", "is_decision_valid", "check_if_decision_is_valid"]


def check_if_decision_is_valid(
    hand_nb: int,
    right_player_decision_pair: Tuple[Player, Decision],
    left_player_decision_pair: Tuple[Player, Decision],
    total_nb_dices: int,
) -> bool:
    is_decision_valid_output = True
    try:
        is_decision_valid(
            hand_nb,
            right_player_decision_pair,
            left_player_decision_pair,
            total_nb_dices,
        )
    except (InvalidGameInput, AttributeError):
        is_decision_valid_output = False
    return is_decision_valid_output


def is_decision_valid(
    hand_nb: int,
    right_player_decision_pair: Tuple[Player, Decision],
    left_player_decision_pair: Tuple[Player, Decision],
    total_nb_dices: int,
) -> None:
    first_play = hand_nb == 0
    right_player, right_player_decision = right_player_decision_pair
    left_player, left_player_decision = left_player_decision_pair
    right_player_name, left_player_name = right_player.name, left_player.name

    if (
        first_play
        and (right_player_decision.raise_)
        and (right_player.n_dices_left > 1)
    ):
        if right_player_decision.raise_.dice_face == PACO:
            raise InvalidGameInput(
                right_player.n_dices_left,
                GameErrorMessage.NO_PACO_WHEN_STARTING_ROUND,
            )
    if right_player_decision.bluff:
        raise InvalidGameInput("Can not call bluff at the beginning of the hand.")
    if right_player_decision.raise_.n_dices > total_nb_dices:
        raise InvalidGameInput(
            f"raise= {right_player.name}:{right_player_decision.raise_.n_dices}, {left_player.name}:{left_player_decision.raise_.n_dices}  vs total_nb_dices={total_nb_dices}",
            GameErrorMessage.RAISE_EXCEED_TOTAL_NB_DICES_LEFT,
        )
    if left_player_decision.raise_:
        if left_player_decision.raise_.n_dices > total_nb_dices:
            raise InvalidGameInput(
                f"raise= {right_player.name}:{right_player_decision.raise_.n_dices}, {left_player.name}:{left_player_decision.raise_.n_dices}  vs total_nb_dices={total_nb_dices}",
                GameErrorMessage.RAISE_EXCEED_TOTAL_NB_DICES_LEFT,
            )

    if right_player_decision.raise_ and left_player_decision.raise_:  # 1.RAISE
        if (
            left_player_decision.raise_.n_dices == right_player_decision.raise_.n_dices
        ):  # 1.1 same number of dices
            if (
                left_player_decision.raise_.dice_face
                > right_player_decision.raise_.dice_face
            ):  # 1.1.1 higher dice value
                decision_outcome, decision_code = (
                    f"{left_player.left_player.name} to talk",
                    "1.1.1",
                )
                # hand_nb += 1  # TODO:test
            else:  # 1.1.2 NO_LOWER_DICE_VALUE_WHEN_SAME_NUMBER_OF_DICES
                raise InvalidGameInput(
                    f"left_player={left_player_name}-{left_player_decision} vs right_player={right_player_name}-{right_player_decision}",
                    GameErrorMessage.NO_LOWER_DICE_VALUE_WHEN_SAME_NUMBER_OF_DICES,
                )
        elif (
            left_player_decision.raise_.n_dices > right_player_decision.raise_.n_dices
        ):  # 1.2 higher number of dices
            if (
                right_player_decision.raise_.dice_face == PACO
            ):  # 1.2.1 Left player higher number of dices but right player played PACOS
                if (
                    left_player_decision.raise_.dice_face == PACO
                ):  # 1.2.1.1 left player played higher number of PACO
                    decision_outcome, decision_code = (
                        f"{left_player.left_player.name} to talk",
                        "1.2.1.1",
                    )
                    # shand_nb += 1
                elif (
                    left_player_decision.raise_.dice_face != PACO
                ):  # 1.2.1.2 left player played higher number of dices but not PACOS
                    if left_player_decision.raise_.n_dices >= (
                        right_player_decision.raise_.n_dices * 2 + 1
                    ):  # 1.2.1.2.1 Left player said more than twice +1
                        decision_outcome, decision_code = (
                            f"{left_player.left_player.name} to talk",
                            "1.2.1.2.1",
                        )
                        # hand_nb += 1
                    elif left_player_decision.raise_.n_dices < (
                        right_player_decision.raise_.n_dices * 2 + 1
                    ):  # 1.2.1.2.2 Left player did not say more than twice +1
                        raise InvalidGameInput(
                            GameErrorMessage.NO_LOWER_NUMBER_OF_DICES_UNLESS_IF_AT_LEAST_THE_HALF_IN_PACOS(
                                "1.2.1.2.2",
                                left_player_name,
                                right_player_name,
                                right_player_decision.raise_.n_dices * 2 + 1,
                                left_player_decision.raise_.n_dices,
                            )
                        )
                else:
                    raise NotImplementedError("1.2.1.3")
            elif (
                right_player_decision.raise_.dice_face != PACO
            ):  # 1.2.2 Left player higher number of dices and right player did not play pacos
                decision_outcome, decision_code = (
                    f"{left_player.left_player.name} to talk",
                    "1.2.2",
                )
                # self.hand_nb += 1
            else:
                raise NotImplementedError("1.2.3")
        elif (
            left_player_decision.raise_.n_dices < right_player_decision.raise_.n_dices
        ):  # 1.3 lower number of dices
            half_nb_dices_pacos_needed = math.ceil(
                right_player_decision.raise_.n_dices / 2
            )
            if (
                left_player_decision.raise_.dice_face != "PACO"
            ):  # 1.3.1 left player did not raise with pacos
                raise InvalidGameInput(
                    GameErrorMessage.NO_LOWER_NUMBER_OF_DICES_UNLESS_IF_AT_LEAST_THE_HALF_IN_PACOS(
                        "1.3.1.1",
                        left_player_name,
                        right_player_name,
                        half_nb_dices_pacos_needed,
                        left_player_decision.raise_.n_dices,
                    )
                )
            elif (
                left_player_decision.raise_.dice_face == "PACO"
            ):  # 1.3.2 left player played with pacos
                if (
                    left_player_decision.raise_.n_dices < half_nb_dices_pacos_needed
                ):  # 1.3.2.1 left player played with pacos but did not raise enough
                    raise InvalidGameInput(
                        GameErrorMessage.NO_LOWER_NUMBER_OF_DICES_UNLESS_IF_AT_LEAST_THE_HALF_IN_PACOS(
                            "1.3.2.1",
                            left_player_name,
                            right_player_name,
                            half_nb_dices_pacos_needed,
                            left_player_decision.raise_.n_dices,
                        )
                    )
                elif (
                    left_player_decision.raise_.n_dices >= half_nb_dices_pacos_needed
                ):  # 1.3.2.1 left player played with pacos  and raise enough
                    decision_outcome, decision_code = (
                        f"{left_player.left_player.name} to talk",
                        "1.3.2.1",
                    )
                    hand_nb += 1
                else:  # 1.3.2.2
                    raise NotImplementedError("1.3.2.2")
            else:  # 1.3.3
                raise NotImplementedError("1.3.3")
        else:  # 1.4
            raise NotImplementedError("1.4")
    elif (
        left_player_decision.bluff is True
    ):  # 2. Left player calls bluff on right player
        all_dices_details = self.get_all_dices_details()
        dices_details_per_player = self.get_dices_details_per_player()
        nb_dices_bet_on_and_present_in_game = (
            all_dices_details.get(right_player_decision.raise_.dice_face, 0)
            + all_dices_details.get(PACO, 0)
            if right_player_decision.raise_.dice_face != PACO
            else all_dices_details.get(PACO, 0)
        )
        if (
            right_player_decision.raise_.n_dices <= nb_dices_bet_on_and_present_in_game
        ):  # 2.1 right player has more dices
            decision_outcome, decision_code = (
                f"Right Player:\t{right_player_name} won.\nLeft Player:\t{left_player_name} lost.",
                "2.1",
            )
            left_player.take_one_dice_out()
            winner, looser = right_player_name, left_player_name
            left_player_to_looser_player = left_player.left_player
            # self.close_round()

        elif (
            right_player_decision.raise_.n_dices > nb_dices_bet_on_and_present_in_game
        ):  # 2.2 right player has not as many dices as he claimed
            decision_outcome, decision_code = (
                f"Right Player:\t{right_player_name} lost.\nLeft Player:\t{left_player_name} won.",
                "2.2",
            )
            right_player.take_one_dice_out()
            winner, looser = left_player_name, right_player_name
            left_player_to_looser_player = right_player.left_player
            # self.close_round()
        else:  # 2.3
            raise NotImplementedError("2.3")
    elif (
        left_player_decision.equal is True
    ):  # 3. Left Player calls equal on right players
        raise NotImplementedError

    else:  # 4. not raising, nor bluffing nor equalling, do not know what it is
        raise NotImplementedError("4")


class PlayerUser(Player):
    pass


class PerudoAI(Player):
    def __init__(
        self,
        name: Union[str, None] = None,
        n_players: int = N_PLAYERS,
        n_init_dices_per_player: int = N_INIT_DICES_PER_PLAYER,
    ) -> None:
        super().__init__(name, n_players, n_init_dices_per_player)

    def take_decision(self, *args, **kwargs) -> Decision:
        return self.take_optimal_decision(*args, **kwargs)

    def take_optimal_decision(
        self,
        hand_nb: int,
        total_nb_dices_left_in_game: int,
        right_player_decision: Union[None, Decision] = None,
    ) -> Decision:
        df_probas_raise, df_probas_bluff, probas = calculate_probas_of_all_decisions(
            total_nb_dices_left_in_game, self.dices
        )
        if (hand_nb == 0) and (right_player_decision is None):
            best_n_dices, best_dice_face = max(
                df_probas_raise[df_probas_raise == max(df_probas_raise)].index
            )
            return Decision(Raise(n_dices=best_n_dices, dice_face=best_dice_face))

        elif right_player_decision is not None:
            proba_bluff = df_probas_bluff[right_player_decision.raise_]
            probas_raise = df_probas_raise[
                df_probas_raise.index > right_player_decision.raise_
            ]
            best_n_dices, best_dice_face = max(
                probas_raise[probas_raise == max(probas_raise)].index
            )
            max_proba_raise = probas_raise[best_n_dices, best_dice_face]
            if max_proba_raise >= proba_bluff:
                return Decision(Raise(n_dices=best_n_dices, dice_face=best_dice_face))
            elif max_proba_raise < proba_bluff:
                return Decision(bluff=True)
            else:
                raise NotImplementedError

        elif right_player_decision is None:
            raise NotImplementedError
        else:
            raise NotImplementedError
