from window import PaintWindow, BoundingRect
from cursor import Cursor, Point
from pynput import keyboard
from pathlib import Path
import json

with open(Path('./interactions/interaction_points.json')) as f:
    # all units in pixels
    INTERACTION_POINTS = IP = json.load(f)


class UniversalInteractionsHeader:
    """Declares universally used properties and methods for the Toolbar and Canvas interaction subclasses, but are not defined until InteractionManager is created. 
            View InteractionsManager in manager.py for full explanation."""

    def __init__(self) -> None:
        """Declares universally used properties and methods for the Toolbar and Canvas interaction subclasses, but are not defined until InteractionManager is created. 
            View InteractionsManager in manager.py for full explanation."""
        self._window: PaintWindow
        self._bounding_rect: BoundingRect

        # "forward type define" the pynput keyboard and mouse controller for type annotation ease
        self._mouse: Cursor
        self._keyboard: keyboard.Controller

    def _click(self, point: Point) -> None:
        """Move a mouse to a Point position, and left-click once."""
        pass

    def _move_cursor(self, point: Point) -> None:
        """Move a mouse to a Point position."""
        pass
