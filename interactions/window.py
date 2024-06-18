from pathlib import Path
import subprocess
import json
import time
import win32gui
import win32con
import win32api
from collections import namedtuple
import ctypes

BoundingRect = namedtuple("BoundingRect", ["x", "y", "width", "height"])


class NoPaintWindowsError(Exception):
    """Raised when the window for ms-paint is not found."""

    def __init__(self):
        super().__init__(
            "No Paint window found. Something went wrong, perhaps it wasn't opened in time?")


class MultiplePaintWindowsError(Exception):
    """Raised when there are multiple ms-paint windows. This is an issue because we are unsure of which to use."""

    def __init__(self, num_found: int):
        super().__init__(
            f"{num_found} Paint windows found. There should only be one Paint window active during the running of this script. Close all Paint windows before running.")


class DPIUnawareError(Exception):
    """Raised when the process DPI awarenesss = 0, or is unaware. This creates potentially innacurate BoundingRect."""

    def __init__(self):
        super().__init__(
            "Process DPI Awareness is set to 0 (Unaware). Set it to Per Monitor DPI Aware (2), done through correct initialization.")


class PaintWindow:
    ACTION_DELAY = 0.5
    WINDOW_TEXT = 'Untitled - Paint'

    _DEV = True

    def __init__(self, paint_path: Path | None = None) -> None:
        if paint_path is None:
            with open(r'settings.json') as f:
                self._paint_path = Path(json.load(f)['paint_path'])

        # self._paint_window: gw.Win32Window
        self._paint_window_hwnd: int

        # DPI aware flag, only need to set DPI awareness once, and only when getting the window
        self._monitor_dpi_aware = False

    def _get_window(self) -> int:
        """Return a hwnd to the ms-paint window. Ensures only one window with `PaintWindow.WINDOW_TEXT` as it's window text is open."""
        # First, find all paint windows with the correct window text of 'Untitled - Paint'
        results = []

        def handler(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                results.append(win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(handler, None)

        results = [result for result in results if result ==
                   PaintWindow.WINDOW_TEXT]

        # Next, ensure there's only 1 active ms-paint window
        # if there's currently no paint window, or more than 2, something went wrong and error out
        if len(results) == 0:
            raise NoPaintWindowsError
        elif len(results) >= 2 and not PaintWindow._DEV:
            raise MultiplePaintWindowsError(len(results))

        # Next, after making it this far, set DPI awareness to per monitor dpi aware (2)
        # without setting this, bounding rects would be off because some monitors have different scaling/zoom settings.
        if not self._monitor_dpi_aware:
            # https://stackoverflow.com/a/44422362
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            self._monitor_dpi_aware = True

        # Finally, find the hwnd of the ms-paint window, and return it
        hwnd = win32gui.FindWindow(None, PaintWindow.WINDOW_TEXT)
        return hwnd

    def _check_window_exists(self) -> None:
        """Checks if window exists, if not, error."""
        if self._paint_window_hwnd is None:
            raise NoPaintWindowsError

    def _check_monitor_dpi_aware(self) -> None:
        """Checks if DPI awareness is correct, if not, error."""
        if self._monitor_dpi_aware is False:
            raise DPIUnawareError

    def _check_valid(self) -> None:
        """Checks if PaintWindow is valid, and can be fully interacted with using subclasses."""
        self._check_window_exists()
        self._check_monitor_dpi_aware()

    def initialize_window(self) -> None:
        """Utilize subprocess.Popen to start ms-paint. Opens path found in `settings.json['paint_path']`. Waits 0.25 seconds before attempting to find the Paint window."""
        subprocess.Popen(['cmd', '/c', 'start', '/max', self._paint_path])
        time.sleep(PaintWindow.ACTION_DELAY)
        self._paint_window_hwnd = self._get_window()

    def modify(self) -> None:
        """Maximizes and focuses the Paint window."""
        self._check_window_exists()

        win32gui.SetForegroundWindow(self._paint_window_hwnd)
        win32gui.ShowWindow(self._paint_window_hwnd, win32con.SW_MAXIMIZE)

    def window_rect(self) -> BoundingRect:
        """Return a rect that represents the window. Window is 'naive', unaware of the monitor it is on and it's position relative to base monitor, only relative to the monitor it is on."""
        self._check_window_exists()
        self._check_monitor_dpi_aware()
        rect = BoundingRect(*win32gui.GetClientRect(self._paint_window_hwnd))
        return rect

    def monitor_rect(self) -> BoundingRect:
        """Return a rect that represents the monitor working area that the window belongs to.."""
        self._check_window_exists()
        self._check_monitor_dpi_aware()

        monitor_handle = win32api.MonitorFromWindow(self._paint_window_hwnd)
        # https://timgolden.me.uk/pywin32-docs/win32api__GetMonitorInfo_meth.html
        # also has a 'Monitor' that might be more suitable
        rect = BoundingRect(
            *win32api.GetMonitorInfo(monitor_handle)['Work'])
        return rect


if __name__ == '__main__':
    p = PaintWindow()
    p.initialize_window()
    p.modify()
    print(p.window_rect())
