__all__ = [
    "Constants",
    "params",
    "N_INIT_DICES_PER_PLAYER",
    "POSSIBLE_VALUES",
    "DEV_MODE",
    "N_PLAYERS",
    "PACO",
    "IS_DEBUG_MODE",
]


class Constants:
    POSSIBLE_VALUES = "POSSIBLE_VALUES"
    N_INIT_DICES_PER_PLAYER = "N_INIT_DICES"
    DEV_MODE = "DEV_MODE"
    N_PLAYERS = "N_PLAYERS"
    PACO = "PACO"
    IS_DEBUG_MODE = "IS_DEBUG_MODE"


params = {
    Constants.POSSIBLE_VALUES: ["2", "3", "4", "5", "6", Constants.PACO],
    Constants.N_INIT_DICES_PER_PLAYER: 5,
    Constants.DEV_MODE: True,
    Constants.N_PLAYERS: 3,
    Constants.PACO: "PACO",
    Constants.IS_DEBUG_MODE: True,
}

POSSIBLE_VALUES = params.get(Constants.POSSIBLE_VALUES)
N_INIT_DICES_PER_PLAYER = params.get(Constants.N_INIT_DICES_PER_PLAYER)
DEV_MODE = params.get(Constants.DEV_MODE)
N_PLAYERS = params.get(Constants.N_PLAYERS)
PACO = params.get(Constants.PACO)
IS_DEBUG_MODE = params.get(Constants.IS_DEBUG_MODE)
