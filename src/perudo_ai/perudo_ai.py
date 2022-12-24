from perudo_ai.player import Player
from perudo_ai.decision import Decision, Raise
from constants import *
from typing import *
from perudo_ai.proba_calculator import calculate_probas_of_all_decisions


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
