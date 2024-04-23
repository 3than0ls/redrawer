from window import PaintWindow, BoundingRect
from cursor import Cursor, Point
from interactions.toolbar import ToolbarInteractions
from interactions.canvas import CanvasInteractions
from pynput import keyboard
import time

# Use InteractiosnManager


class InteractionsManager(ToolbarInteractions, CanvasInteractions):
    r"""
    Here, inherit all methods from ToolbarInteractions and CanvasInteractions, whilst also defining methods used by both here.
     Neither individual interaction classes will be used other than for InteractionsManager, so we need not worry about any issues about defining these universal methods may cause.
     Additionally, universal methods will be declared for ease of use and type annotation.
    ```none

                            UniversalInteractionsHeader   <--------------------\
                                       |                                        |
                                       | < provides universal declarations      |
                                       |           that are used by all         |
                 ______________________|_______________                         |
                /                                      \                        |
        ToolbarInteractions                   CanvasInteractions                |
                \______________________________________/                        |  < provides universal definitions 
                                    |                                           |           that are used by ..
                           InteractionsManager                                  |
                                    |                                           |
                      (certain defined properties and methods) ----------------/
    ```
     They are codependent, relying on each other for functionality, and incapable of working without each other. Designed this way so I don't have one mega-class, and I can split them up.
     This is akin to some form of cooperative inheritance.
     Dubious code practices.
     """

    def __init__(self, window: PaintWindow) -> None:
        self._window = window
        self._bounding_rect = window.window_rect()

        self._mouse = Cursor(window)
        self._keyboard = keyboard.Controller()

    def _move(self, point: Point) -> None:
        """Declared in interactions.universals.py"""
        self._mouse.position = point

    def _click(self, point: Point | tuple[int, int], *, num_clicks: int = 1, pre_delay: int | float = 0, post_delay: int | float = 0.005) -> None:
        """Declared in interactions.universals.py"""
        # execute pre-delay
        time.sleep(pre_delay)

        if type(point) is not Point:
            point = Point(*point)

        self._move(point)
        self._mouse.click(num_clicks)

        # execute post-delay
        time.sleep(post_delay)
