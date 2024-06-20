from pathlib import Path
import pynput.keyboard as keyboard
import os

from logger import PROGRESS_LOG
from redrawer import Redrawer


def main():
    """DURING ANY POINT OF THE PROGRAM YOU WISH TO HARD STOP (non gracefully!), PRESS ESC KEY."""
    def failsafe(key):
        if key == keyboard.Key.esc:
            PROGRESS_LOG.log("ESC PRESSED, EXITING PROGRAM.")
            os._exit(1)

    listener = keyboard.Listener(on_press=failsafe)
    listener.start()

    images = [r"images\test1.PNG", r"images\test2.jpg",
              r"images\test3.jpg", r"images\test4.jpg", r"images\test5.jpg", r"images\test6.png"]

    PROGRESS_LOG.log(
        "Beginning program - press ESC whenever to immediately exit.")

    rd = Redrawer(Path(images[0]))
    rd.redraw()


if __name__ == '__main__':
    main()
