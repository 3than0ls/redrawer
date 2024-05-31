"""
This technically doesn't need to be a part of the Redrawer program, but is rather used to inspect the outputs from image processing without the lengthy task of drawing it out on ms-paint.

The process is as follows:
    1) [all of from_image process]
    2) Translate the output matrix of palette indices to RGB
    3) (if called) show the image

"""


from image_processing.palette.palette import RGB, Palette
import numpy as np
from PIL import Image
from numba import njit


@njit
def _translate_palette_indices_to_rgb(palette_image_array: np.ndarray, palette_array: np.ndarray) -> np.ndarray:
    """Translates an Numpy array of palette indices (used for drawing directions) to an RGB image array."""
    image_matrix = np.ones(
        shape=(
            # row , col of the pixel in the image
            *palette_image_array.shape[:2],
            3    # row, col of the color in palette
        ), dtype=np.uint8
    )

    for row, indices_row in enumerate(palette_image_array):
        for col, palette_index in enumerate(indices_row):
            # convert [row][col] index to dim1 index
            index = palette_index[0] * 10 + palette_index[1]
            rgb = np.asarray(palette_array[index])

            image_matrix[row, col] = rgb

    return image_matrix


def show_image(palette_image_array: np.ndarray, palette: Palette) -> None:
    """Translates a numpy array of palette indices (used for drawing directions) to an RGB image array, then converts it to an actual image using PIL and shows it. 
    Used only for seeing what the drawing directions should draw, without having it done."""
    img_arr = _translate_palette_indices_to_rgb(
        palette_image_array, palette.asarray())

    img = Image.fromarray(img_arr, 'RGB')
    img.show()
