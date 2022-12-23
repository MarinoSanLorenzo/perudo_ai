from perudo_ai.player import Player
from perudo_ai.decision import Decision, Raise
from constants import *
from typing import *
from perudo_ai.proba_calculator import calculate_probas_of_all_decisions


class PerudoAI(Player):
    def __init__(
        self,
        name: Union[str, None] = None,
        n_players: int = N_PLAYERS,
        n_init_dices_per_player: int = N_INIT_DICES_PER_PLAYER,
    ) -> None:
        super().__init__(name, n_players, n_init_dices_per_player)

    def take_optimal_decision(
        self,
        hand_nb: int,
        total_nb_dices_left_in_game: int,
        right_player_decison: Union[None, Decision] = None,
    ) -> Decision:
        df_probas_raise, df_probas_bluff, probas = calculate_probas_of_all_decisions(
            total_nb_dices_left_in_game, self.dices
        )
        if (hand_nb == 0) and (right_player_decison is None):
            best_n_dices, best_dice_face = max(
                df_probas_raise[df_probas_raise == max(df_probas_raise)].index
            )
            return Decision(Raise(n_dices=best_n_dices, dice_face=best_dice_face))
