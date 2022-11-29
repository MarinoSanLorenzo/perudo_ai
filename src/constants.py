__all__ = ["Constants", "params", "N_INIT_DICES", "POSSIBLE_VALUES", "DEV_MODE"]


class Constants:
    POSSIBLE_VALUES = "POSSIBLE_VALUES"
    N_INIT_DICES = "N_INIT_DICES"
    DEV_MODE = "DEV_MODE"


params = {
    Constants.POSSIBLE_VALUES: ["PACO", "2", "3", "4", "5", "6"],
    Constants.N_INIT_DICES: 5,
    Constants.DEV_MODE: True,
}

POSSIBLE_VALUES = params.get(Constants.POSSIBLE_VALUES)
N_INIT_DICES = params.get(Constants.N_INIT_DICES)
DEV_MODE = params.get(Constants.DEV_MODE)
