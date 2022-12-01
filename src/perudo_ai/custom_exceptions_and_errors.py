from typing import *

__all__ = ["GameErrorMessage", "InvalidGameInput", "GameException"]


class GameErrorMessage:
    LESS_THAN_TWO_PLAYERS = "There can not be less than two players!"
    INVALID_PLAYERS_TYPE = (
        "A list of players or a number of players (integer) should be entered!"
    )
    UNIQUE_PLAYERS_NAME = "Can not have two players with same name!"
    INVALID_DICE_TYPE = "An integer should be entered"
    INVALID_GAME_TYPE = "An integer should be entered"
    INVALID_GAME_INPUT = "You entered an invalid game input!"
    INVALID_PLAYER_INPUT = "You entered an invalid player input!"
    NO_PACO_WHEN_STARTING_ROUND = "A Player can not raise, saying PACOS, when starting the first round unless he has only one dice left. Number dices left:"
    RAISE_EXCEED_TOTAL_NB_DICES_LEFT = (
        "The player raised over the total number of dices left in the game!"
    )


class GameException(Exception):
    pass


class InvalidGameInput(GameException):
    def __init__(
        self, game_input: Any = "", message: str = "You entered an invalid game input!"
    ) -> None:
        self.game_input = game_input
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.game_input:
            return f"{self.message} --> {self.game_input}"
        return self.message