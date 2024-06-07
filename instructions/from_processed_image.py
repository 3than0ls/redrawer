"""
Creates the "instructions" from an NDarray representing the processed image, created from the image_processing module.

Produces a string containing an ordered "instructions" (with syntax I define) telling exactly how the interactions module will draw.
The string can be optionally outputted into a file, and loaded up later.

Uses the following to compute instructions:
multiprocessing (https://docs.python.org/3/library/multiprocessing.html) where different colors are split into different processes
dbm (https://docs.python.org/3/library/dbm.html#module-dbm) where instructions are written to, and used later.



Functional programming because numba will greatly increase the speed it takes to create it.

INSTRUCTION SYNTAX:
Key: [PaletteColorRow,PaletteColorCol]
Value: (the instructions with the following syntax)
    (x1,y1,length1)|(x2,y2,length2)|...|(xX,yX,lengthX)

"""

import numpy as np
from numba import njit
import dbm
import concurrent.futures
import time
from image_processing.palette.palette import Palette
from pathlib import Path


_PRINT_PROGRESS = True


INSTRUCTION_TYPE = "BASIC"

INSTRUC_MARKER = {
    "BASIC": "redrawer-basic-instruction"
}[INSTRUCTION_TYPE]


TEMP_DIR = Path.cwd() / "temp"
TEMP_FPATH = TEMP_DIR / "redrawer_instruction"


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


# njit something
def _compute_instructions_for_palette_color(processed_image: np.ndarray, palette_color: tuple):
    """Like the name says, compute the instructions for a palette color.
    Just to remember: the processed_image doesn't consist of colors, but rather the [row, column] positions of colors in palette_color. We're searching for palette_color in processed_image
    """
    key = f"{palette_color[0]}, {palette_color[1]}"
    instruc = "SOMETHING SOMETHING"
    time.sleep(1)

    return (key, instruc)


if __name__ == '__main__':
    with dbm.open(str(TEMP_FPATH), 'r') as db:
        print(db.keys())
