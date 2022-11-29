import pytest
from perudo_ai.decision import Decision, Raise
from perudo_ai.player import Player
from typing import *


class TestDecision:
    def test_decision_raise(self) -> None:
        decision = Decision(raise_=Raise(6, "PACO"))
        assert isinstance(decision.raise_, Raise)
        assert decision.equal is False
        assert decision.bluff is False

    def test_decision_equal(self) -> None:
        decision = Decision(equal=True)
        assert decision.raise_ is None
        assert decision.equal is True
        assert decision.bluff is False

    def test_decision_bluff(self) -> None:
        decision = Decision(bluff=True)
        assert decision.raise_ is None
        assert decision.equal is False
        assert decision.bluff is True
