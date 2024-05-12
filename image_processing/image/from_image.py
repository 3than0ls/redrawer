import numpy as np

from image_processing.palette.palette import RGB, Palette
from image_processing.palette.color_distance import color_distance


# https://numba.pydata.org/


def _partial_call_color_distance(source_color: RGB):
    """A partial call function for color distance."""
    def col_dist(compare_color_rgb: np.ndarray) -> int:
        # print(type(compare_color_rgb))
        return color_distance(source_color, RGB(*compare_color_rgb))

    return col_dist  # , otypes=[np.uint32])


def _color_dist_matrices(image_array: np.ndarray, palette: Palette) -> np.ndarray:
    """
    Return the color distance matrices
    Final matrix will be of shape (Image Rows x Image Cols x Palette's Num Colors)   <-- DO THIS
    Eventually to be all merged into one new image matrix in transform_image_colors
    """

    _color_dists = np.zeros(
        shape=(
            *image_array.shape[:2],  # for every pixel
            palette.num_colors,  # for every color
        ),
        dtype=np.uint32
    )

    for color_num, rgb in enumerate(palette.flattened_palette):
        func = _partial_call_color_distance(rgb)
        for row, pixel_row in enumerate(image_array):
            for col, pixel_rgb in enumerate(pixel_row):
                _color_dists[row, col, color_num] = func(pixel_rgb)
        print('finished color', color_num)

    print(_color_dists)
    print(_color_dists.shape)
    return _color_dists


def _merge_color_matrices(image_array: np.ndarray, color_dists: np.ndarray) -> np.ndarray:
    """
    Merge all the color distance matrices into one image matrix.
    Do this by for each pixel, find the least color distance, and the color with the least color distance, assign that palette color's ROW and COLUMN to the position of the pixel in the image.
    """
    image_matrix = np.zeros(
        shape=(
            *image_array.shape,   # row , col of the pixel in the image
            2    # row, col of the color in palette
        )
    )

    def _get_index(col_dist_arr: np.ndarray):
        ind = np.argmin(col_dist_arr)
        # return the row and column, calculated mathematically
        return np.array((ind // 10, ind % 10), dtype=np.uint8)

    image_matrix = np.apply_along_axis(_get_index, 2, color_dists)
    print(image_matrix)
    print(image_matrix.shape)
    return image_matrix


def create_image(image_array: np.ndarray, palette: Palette) -> np.ndarray:
    color_matrices = _color_dist_matrices(image_array, palette)
    np.save('temp', color_matrices)

    # color_matrices = np.load('temp.npy')
    palette_color_array = _merge_color_matrices(image_array, color_matrices)

    return palette_color_array
