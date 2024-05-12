
from image_processing.palette.palette import RGB, Palette
import numpy as np
from PIL import Image
from numba import njit


@njit
def _translate_palette_indices_to_rgb(palette_image_array: np.ndarray, palette_array: np.ndarray) -> np.ndarray:
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


def show_image_from_palette_array(palette_image_array: np.ndarray, palette: Palette) -> None:
    img_arr = _translate_palette_indices_to_rgb(
        palette_image_array, palette.asarray())

    img = Image.fromarray(img_arr, 'RGB')
    img.show()
