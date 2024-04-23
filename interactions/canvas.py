from cursor import Point
from interactions.universals import UniversalInteractionsHeader
from dataclasses import dataclass


class CanvasInteractions(UniversalInteractionsHeader):
    def __init__(self) -> None:
        super().__init__()

    # def draw stuff and whatnot

    # TODO: add a get max canvas size function, based on bottom and right padding constants
    # perhaps make it a part of the manager?
