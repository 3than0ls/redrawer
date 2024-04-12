import time
from window import PaintWindow, BoundingRect
import pynput.mouse as pynmouse
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class CursorOutOfWindowError(Exception):
    """Raised when the cursor is assigned to be out of bounds of the Paint window,"""

    def __init__(self, dimension: str, cursor: Point):
        super().__init__(f"""Cursor set to position {cursor} (relative to screen), but the {
            dimension} value of cursor was is outside the bounds of the Paint window.""")


class Interactions:
    """Directly interacts with the mouse."""

    def __init__(self, window: PaintWindow) -> None:
        naive_win_rect = window.window_rect()
        monitor_rect = window.monitor_rect()

        self._win_rect = BoundingRect(monitor_rect.x + naive_win_rect.x,
                                      monitor_rect.y + naive_win_rect.y,
                                      naive_win_rect.width,
                                      naive_win_rect.height)

        self._mouse = pynmouse.Controller()

        # _cursor_pos monitors the exact position of the cursor on the screen
        # but the class utilizes @property so the user will only know relative cursor position (relative to window)
        self._cursor_pos: Point

    @property
    def cursor(self) -> Point:
        """Returns mouse cursor position relative to paint window."""
        return Point(self._cursor_pos.x - self._win_rect.x, self._cursor_pos.y - self._win_rect.y)

    @cursor.setter
    def cursor(self, new_cursor: Point) -> None:
        """Move the mouse to a valid point Point(x, y) relative to the top left of the paint window."""
        new_x = self._win_rect.x + new_cursor.x
        if not self._win_rect.x < new_x < self._win_rect.x + self._win_rect.width:
            raise CursorOutOfWindowError("X", new_cursor)

        new_y = self._win_rect.y + new_cursor.y
        if not self._win_rect.y < new_y < self._win_rect.y + self._win_rect.height:
            raise CursorOutOfWindowError("Y", new_cursor)

        # print('window position', self._win_rect.x, self._win_rect.y)
        # print('new position', new_x, new_y)
        # self._mouse.move(new_x, new_y)
        self._cursor_pos = Point(new_x, new_y)
        self._mouse.position = self._cursor_pos


if __name__ == '__main__':
    p = PaintWindow()
    p.initialize_window()
    i = Interactions(p)
    time.sleep(2)

    i.cursor = Point(100, 400)
