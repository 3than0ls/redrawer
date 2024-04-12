from pathlib import Path
import subprocess
import json
import pygetwindow as gw
import time


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


class PaintWindow:
    ACTION_DELAY = 0.25

    def __init__(self, paint_path: Path | None = None):
        if paint_path is None:
            with open(r'settings.json') as f:
                self._paint_path = Path(json.load(f)['paint_path'])

        self._paint_window: gw.Win32Window

    def _get_window(self) -> gw.Win32Window:
        """Return a `pygetwindow.Win32Window object, interacted with later to move/fullscreen.`"""
        results = gw.getWindowsWithTitle("Untitled - Paint")
        print(results)

        if len(results) == 0:
            raise NoPaintWindowsError
        elif len(results) > 2:
            raise MultiplePaintWindowsError(len(results))
        else:
            return results[0]

    def initialize_window(self):
        """Utilize subprocess.Popen to start ms-paint. Opens path found in `settings.json['paint_path']`. Waits 0.25 seconds before attempting to find the Paint window."""
        subprocess.Popen(['cmd', '/c', 'start', '/max', self._paint_path])
        time.sleep(PaintWindow.ACTION_DELAY)
        self._paint_window = self._get_window()

    def modify(self):
        """Maximizes and focuses the Paint window."""
        if self._paint_window is None:
            raise NoPaintWindowsError

        self._paint_window.maximize()
        self._paint_window.activate()


if __name__ == '__main__':
    p = PaintWindow()
    p.initialize_window()
    p.modify()
