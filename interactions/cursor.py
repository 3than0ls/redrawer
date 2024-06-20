import os
import time
from interactions.window import PaintWindow, BoundingRect
import pynput.mouse as pynmouse
import pynput.keyboard as keyboard
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class CursorOutOfWindowError(Exception):
    """Raised when the cursor is assigned to be out of bounds of the Paint window,"""

    def __init__(self, dimension: str, cursor: Point):
        super().__init__(f"""Cursor set to position {cursor} (relative to screen), but the {
            dimension} value of cursor was is outside the bounds of the Paint window.""")


class Cursor:
    """Directly interacts with the mouse/cursor position. Wraps the behavior of pynput.mouse.Controller()"""

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

        self._held = False

        # add a failsafe to allow control if needed to stop; triggers when 'Esc' is pressed
        def failsafe(key):
            if key == keyboard.Key.esc:
                print('HARD QUITTING')
                os._exit(1)
        listener = keyboard.Listener(on_press=failsafe)
        listener.start()

    @property
    def position(self) -> Point:
        """Returns mouse cursor position relative to paint window."""
        return Point(self._cursor_pos.x - self._win_rect.x, self._cursor_pos.y - self._win_rect.y)

    @position.setter
    def position(self, new_position: Point) -> None:
        """Move the mouse to a valid point Point(x, y) relative to the top left of the paint window."""
        new_x = self._win_rect.x + new_position.x
        if not self._win_rect.x < new_x < self._win_rect.x + self._win_rect.width:
            raise CursorOutOfWindowError("X", new_position)

        new_y = self._win_rect.y + new_position.y
        if not self._win_rect.y < new_y < self._win_rect.y + self._win_rect.height:
            raise CursorOutOfWindowError("Y", new_position)

        self._cursor_pos = Point(new_x, new_y)
        self._mouse.position = self._cursor_pos

    def click(self, num_clicks: int = 1) -> None:
        """Click the left mouse button once. Optionally specify number of clicks, defaults to one."""
        self._mouse.click(pynmouse.Button.left, num_clicks)

    def hold(self, *, initial_position: None | Point = None) -> None:
        """Hold left click button until .release() is called. Does nothing if already being held."""
        if self._held:
            return
        else:
            self._held = True
            if initial_position is not None:
                self.position = initial_position
            self._mouse.press(pynmouse.Button.left)

    def release(self, *, initial_position: None | Point = None) -> None:
        """Release left click button, assuming hold() has already been called. Does nothing if mouse is already released."""
        if not self._held:
            return
        else:
            self._held = False
            if initial_position is not None:
                self.position = initial_position
            self._mouse.release(pynmouse.Button.left)


if __name__ == '__main__':
    p = PaintWindow()
    p.initialize_window()
    i = Cursor(p)
    time.sleep(0.7)

    i.position = Point(800, 100)
