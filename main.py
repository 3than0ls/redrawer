from pathlib import Path
import pynput.keyboard as keyboard
import os
from dotenv import dotenv_values

from logger import PROGRESS_LOG
from redrawer import Redrawer

# TODO:
# Eventually add an auto-save feature

INPUT_PATH = dotenv_values("settings.env")["INPUT_PATH"] or "not set"


def main():
    """DURING ANY POINT OF THE PROGRAM YOU WISH TO HARD STOP (non gracefully!), PRESS ESC KEY."""
    def failsafe(key):
        if key == keyboard.Key.esc:
            PROGRESS_LOG.log("ESC PRESSED, EXITING PROGRAM.")
            os._exit(1)

    listener = keyboard.Listener(on_press=failsafe)
    listener.start()

    PROGRESS_LOG.log(
        "Beginning program - press ESC whenever to immediately exit.")

    image_path = Path(INPUT_PATH)

    rd = Redrawer(image_path)
    rd.redraw()


if __name__ == '__main__':
    main()
