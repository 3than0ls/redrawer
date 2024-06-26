"""
The "math" of the image processing.

The input is an image file and Palette class (that was generated from the image file), and the output is a NDarray of Palette colors.
Uses create_image function to "do" everything.

To describe the process, we will define some simple terms.
PCOLORS = the number of colors defined in the palette class, or Palette.num_colors
IMAGE_ARR = The numpy array representing the image in RGB, what you get when converting PIL Image to ndarray

The process is as follows:
    1) Create PCOLORS color distance matrices, all contained within one super-matrix. [_color_dist_matrices]
        - For every color in the palette, apply a color distance calculation on IMAGE_ARR, each palette color outputting a matrix representing the distance each IMAGE_ARR pixel's color from itself
    2) Merge the color matrices into one matrix, creating a new image matrix.
        - To merge, find the minimum distance value in each matrix
        - For each corresponding pixel in the super-matrix, find the minimum value (distance), then set the pixel position to the palette color associated with that minimum.

NOTE: The output is NOT in RGB. The output is a number that is 0 to PCOLORS that serves as an index to the appropriate color in Palette's color list.

The functions are written as function because they make use of numba JIT compiling, which requires basic Python or numpy types. 
Otherwise I would've created a RedrawerImage class and put all these functions as methods and conceal it all :(
"""


from datetime import datetime
import numpy as np
from numba import njit
from image_processing.palette.palette import Palette
from image_processing.palette.color_distance import color_distance
from logger import PROGRESS_LOG


def _color_dist_matrices(image_array: np.ndarray, palette_array: np.ndarray) -> np.ndarray:
    """
    Return the color distance matrices, one for all 30 palette color numbers
    Final matrix will be of shape (Image Px Rows x Image Px Cols x Palette's Num Colors)
    """

    _color_dists = np.zeros(
        shape=(
            *image_array.shape[:2],  # for every pixel
            palette_array.shape[0],  # for every color
        ),
        dtype=np.uint32
    )

    for color_num, source_rgb in enumerate(palette_array):
        result = _color_dist_matrix(
            image_array, palette_array, color_num, source_rgb)
        _color_dists += result
        PROGRESS_LOG.log(f"Generated color distance matrix for color number {
                         color_num+1}/30")

    return _color_dists


@njit(fastmath=True)
def _color_dist_matrix(image_array: np.ndarray, palette_array: np.ndarray, color_num: int, source_rgb: np.ndarray) -> np.ndarray:
    """
    Return the color distance matrix (a singular part of the color distance matrices in the above function)
    Eventually to be all merged into one new image matrix in transform_image_colors
    """

    _color_dist = np.zeros(
        shape=(
            *image_array.shape[:2],  # for every pixel
            palette_array.shape[0],  # for every color
        ),
        dtype=np.uint32
    )

    for row, pixel_row in enumerate(image_array):
        for col, pixel_rgb in enumerate(pixel_row):
            _color_dist[row, col, color_num] = color_distance(
                source_rgb, pixel_rgb)

    return _color_dist


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

    return image_matrix


def create_processed_image(image_array: np.ndarray, palette: Palette) -> np.ndarray:
    """Create a new image from an original image array based off of color palette colors."""
    PROGRESS_LOG.log(
        "GENERATING COLOR DISTANCE MATRICES TO DETERMINE MINIUMUM COLOR DISTANCE")
    color_dist_matrices = _color_dist_matrices(image_array, palette.asarray())
    PROGRESS_LOG.log(
        "MERGING COLOR DISTANCE MATRICES TO DETERMINE MINIMUM COLOR DISTANCE")
    palette_color_array = _merge_color_matrices(
        image_array, color_dist_matrices)

    return palette_color_array
