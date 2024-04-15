from cursor import Point
from interactions.universals import UniversalInteractionsHeader, INTERACTION_POINTS
from dataclasses import dataclass


_CANVAS = INTERACTION_POINTS["Canvas"]
_TOP_LEFT = _CANVAS["top-left"]


class CanvasInteractions(UniversalInteractionsHeader):
    def __init__(self) -> None:
        super().__init__()

    # def draw stuff and whatnot
