"""
Creates the "instructions" from an NDarray representing the processed image, created from the image_processing module.

Produces a string containing an ordered "instructions" (with syntax I define) telling exactly how the interactions module will draw.
The string can be optionally outputted into a file, and loaded up later.

Uses the following to compute instructions:
multiprocessing (https://docs.python.org/3/library/multiprocessing.html) where different colors are split into different processes
dbm (https://docs.python.org/3/library/dbm.html#module-dbm) where instructions are written to, and used later.



Functional programming because numba will greatly increase the speed it takes to create it.

INSTRUCTION SYNTAX:
....

"""

import numpy as np
import dbm
import concurrent.futures
from image_processing.palette import Palette
from pathlib import Path
from dotenv import dotenv_values

_settings = dotenv_values("settings.env")
_PRINT_PROGRESS = _settings["PRINT_ALL_PROGRESS"] == "true"


INSTRUCTION_TYPE = _settings["INSTRUCTION_TYPE"]

INSTRUC_MARKER = {
    "basic": "redrawer-basic-instruction"
}[INSTRUCTION_TYPE]  # type: ignore


TEMP_DIR: Path = Path.cwd() / _settings["TEMP_DIR"]  # type: ignore
TEMP_FPATH: Path = TEMP_DIR / _settings["TEMP_FNAME"]  # type: ignore


def from_processed_image(processed_image: np.ndarray, palette: Palette):
    """
    Turn a processed image into a DBM file with string instructions the `TEMP_INSTRUC_FNAME` name to be used later. See file docstring for the syntax of these "instructions"
    """

    if _PRINT_PROGRESS:
        print(f'--- PROCESSING IMAGE TO INSTRUCTIONS ---')

    TEMP_DIR.mkdir(exist_ok=True)
    with dbm.open(str(TEMP_FPATH), 'n') as _:
        # create a new empty DB to get rid of old one (if existing)
        pass

    def add_to_dbm(future: concurrent.futures.Future) -> None:
        key, instruc_value = future.result()

        if _PRINT_PROGRESS:
            print(f'-- FINISHED PROCESSING PALETTE COLOR AT ({key}) --')

        with dbm.open(str(TEMP_FPATH), 'w') as db:
            db[key] = instruc_value

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                _compute_instructions_for_palette_color, processed_image, (row, col))
            for row in range(palette.shape[1]) for col in range(palette.shape[0])
        ]

        for future in futures:
            future.add_done_callback(add_to_dbm)


def _compute_instructions_for_palette_color(processed_image: np.ndarray, palette_color: tuple):
    """Like the name says, compute the instructions for a palette color.
    Just to remember: the processed_image doesn't consist of colors, but rather the [row, column] positions of colors in palette_color. We're searching for palette_color in processed_image

    Instruction syntax: [x,y,length];[x2,y2,length2]

    """
    key = f"{palette_color[0]},{palette_color[1]}"
    instruc = ""

    for x, row in enumerate(processed_image):
        tracking = False
        cur_pos = tuple()
        cur_length = 1

        for y, color in enumerate(row):
            is_correct_color = color[0] == palette_color[0] and color[1] == palette_color[1]
            if is_correct_color and not tracking:
                cur_pos = (x, y)
                tracking = True
            elif is_correct_color and tracking:
                cur_length += 1
            elif not is_correct_color and tracking:
                tracking = False
                instruc += f"[{cur_pos[0]},{cur_pos[1]},{cur_length}];"
                # reset
                cur_pos = tuple()
                cur_length = 1

        # there might be some leftover buffered, add it
        if tracking:
            instruc += f"[{cur_pos[0]}.{cur_pos[1]},{cur_length}];"

    return (key, instruc)


if __name__ == '__main__':
    with dbm.open(str(TEMP_FPATH), 'r') as db:
        print(db.keys())
