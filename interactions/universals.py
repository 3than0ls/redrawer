from window import PaintWindow, BoundingRect
from cursor import Cursor, Point
from pynput import keyboard
import interactions.constants as C
import time


class UniversalInteractionsHeader:
    """Declares universally used properties and methods for the Toolbar and Canvas interaction subclasses, but are not defined until InteractionManager is created. 
            View InteractionsManager in manager.py for full explanation."""

    def __init__(self) -> None:
        """Declares universally used properties and methods for the Toolbar and Canvas interaction subclasses, but are not defined until InteractionManager is created. 
            View InteractionsManager in manager.py for full explanation. The properties here are to be 'filled in' in manager.py's Manager class."""
        self._window: PaintWindow
        self._bounding_rect: BoundingRect

        # "forward type define" the pynput keyboard and mouse controller for type annotation ease
        self._mouse: Cursor
        self._keyboard: keyboard.Controller

    def _click(self, point: Point | tuple[int, int], *, num_clicks: int = 1, pre_delay: int | float = 0, post_delay: int | float = 0.005) -> None:
        """Move a mouse to a Point position, and left-click once. If tuple of length 2 is passed in, automatically convert it into a Point object. 
        Then, sleep for at least `post_delay` seconds, depending on how slow the system may be.
        Optionally also specify `pre_delay` in seconds, to delay a certain amount of time before clicking.
        Optinally pass `num_clicks` to click more than once."""
        # execute pre-delay
        time.sleep(pre_delay)

        if type(point) is not Point:
            point = Point(*point)

        self._move(point)
        self._mouse.click(num_clicks)

        # execute post-delay
        time.sleep(post_delay)

    def _move(self, point: Point) -> None:
        """Move a mouse to a Point position. See Cursor.position in cursor.py."""
        self._mouse.position = point

    def _canvas_rect(self) -> BoundingRect:
        """Returns a BoundingRect detailing where exactly the canvas is. Useful for specifying canvas dimensions."""
        width = self._bounding_rect.width - \
            C.CANVAS_TOP_LEFT[0] - C.CANVAS_RIGHT_PADDING
        height = self._bounding_rect.height - \
            C.CANVAS_TOP_LEFT[1] - C.CANVAS_BOTTOM_PADDING
        return BoundingRect(C.CANVAS_TOP_LEFT[0], C.CANVAS_TOP_LEFT[1], width, height)
