import numpy as np
from numba import njit

from image_processing.palette.palette import Palette
from image_processing.palette.color_distance import color_distance


@njit(fastmath=True)
def _color_dist_matrices(image_array: np.ndarray, palette_array: np.ndarray) -> np.ndarray:
    """
    Return the color distance matrices
    Final matrix will be of shape (Image Rows x Image Cols x Palette's Num Colors)   <-- DO THIS
    Eventually to be all merged into one new image matrix in transform_image_colors
    """

    _color_dists = np.zeros(
        shape=(
            *image_array.shape[:2],  # for every pixel
            palette_array.shape[0],  # for every color
        ),
        dtype=np.uint32
    )

    for color_num, source_rgb in enumerate(palette_array):
        for row, pixel_row in enumerate(image_array):
            for col, pixel_rgb in enumerate(pixel_row):
                _color_dists[row, col, color_num] = color_distance(
                    source_rgb, pixel_rgb)
        # print('finished color', color_num)

    return _color_dists


@njit(fastmath=True)
def _merge_color_matrices(image_array: np.ndarray, color_dists: np.ndarray) -> np.ndarray:
    """
    Merge all the color distance matrices into one image matrix.
    Do this by for each pixel, find the least color distance, and the color with the least color distance, assign that palette color's ROW and COLUMN to the position of the pixel in the image.
    """
    image_matrix = np.zeros(
        shape=(
            *image_array.shape[:2],   # row , col of the pixel in the image
            2   # row, col of the palette
        ), dtype=np.uint8
    )

    for row, color_dists_row in enumerate(color_dists):
        for col, color_dists in enumerate(color_dists_row):
            ind = np.argmin(color_dists)
            # set to the row and column, calculated mathematically
            image_matrix[row, col] = np.asarray((ind // 10, ind % 10))
            # image_matrix[row][col] = ind

    # print(image_matrix)
    # print('finished merging color distance matrices')
    return image_matrix


def create_image(image_array: np.ndarray, palette: Palette) -> np.ndarray:
    """Create a new image from an original image array based off of color palette colors."""
    color_dist_matrices = _color_dist_matrices(image_array, palette.asarray())

    palette_color_array = _merge_color_matrices(
        image_array, color_dist_matrices)

    return palette_color_array
