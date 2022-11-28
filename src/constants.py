__all__ = ["Constants", "params", 'N_INIT_DICES']


class Constants:
    POSSIBLE_VALUES = "POSSIBLE_VALUES"
    N_INIT_DICES = "N_INIT_DICES"


params = {
    Constants.POSSIBLE_VALUES: ["PACO", "2", "3", "4", "5", "6"],
    Constants.N_INIT_DICES: 5,
}

N_INIT_DICES = params.get(Constants.N_INIT_DICES)