from math import sqrt
from image_processing.palette.palette import RGB, DEFAULT_PALETTE
import numpy as np
from numba import njit
from dotenv import dotenv_values

from logger import PROGRESS_LOG

# Different ways of calculating distinctiveness value:
# Calculate the color distance between every single pixel, and average that
# Optimize this by reducing the resolution to a low amount


# What kind of color distance method to use, either "redmean", "euclidean", "deltaE", and potentially others. Different methods produce different results.
# See below functions to view exactly how different methods are implemented and what they're based off of.
# deltaE takes the longest (complex calculations) but produces best results
COLOR_DISTANCE_METHOD = dotenv_values("settings.env")["COLOR_DISTANCE_METHOD"]


# constant constants, aka don't touch
# How distinct the colors generated need to be. Default value should be 500.
# Decreasing generally produces more similar colors
# Increasing generally produces more different colors
DISTINCTIVENESS_VALUE = {
    "redmean": 500,    # default around 500
    "euclidean": 10,   # default around 10
    "deltaE": 10       # default around 10
}[COLOR_DISTANCE_METHOD]  # type: ignore

# Search through only PARTITION_KTH of the most frequent colors to find distinct colors to add to the palette.
# Smaller the number, faster the distinct colors are found.
# But after using NJIT, searching for distinct colors isn't terribly time consuming, at least compared to the color matrices
# Best not to touch
PARTITION_KTH = 7000


# All functions having to do with color distance, whether the colors are near each other, or if colors are distinct

@njit(fastmath=True)
def _redmean_color_distance(source: np.ndarray, compare: np.ndarray) -> int:
    """Utilizes the low-cost approximation algorithm found here:
    https://www.compuphase.com/cmetric.htm
    https://en.wikipedia.org/wiki/Color_difference -> "redmean"

    Weighted values to compensate for how humans see colorn differently, but doesn't really work appropriately most times on computers...
    """
    mean_red = (source[0] + compare[0]) / 2
    red_diff = source[0] - compare[0]
    green_diff = source[1] - compare[1]
    blue_diff = source[2] - compare[2]
    return int(sqrt(
        (512 + mean_red) * red_diff * red_diff +
        4 * green_diff * green_diff +
        (767-red_diff) * blue_diff * blue_diff
    ))


@njit(fastmath=True)
def _euclid_color_distance(source: np.ndarray, compare: np.ndarray) -> int:
    """Basic Euclidean color distance using a standard distance formula. A non-weighted version of redmean."""
    red_diff = source[0] - compare[0]
    green_diff = source[1] - compare[1]
    blue_diff = source[2] - compare[2]
    return int(sqrt(red_diff * red_diff + green_diff * green_diff + blue_diff * blue_diff))


@njit(fastmath=True)
def _delta_e_distance(source: np.ndarray, compare: np.ndarray) -> int:
    """
    Calculate Delta E variance from source color to compare color, using the CIE L*ab color space.
    Numba can't use external functions (otherwise we'd use skimage.color.rgb2lab), so manually do the calculations/conversions ourselves.
    To calculate Delta-E, we first must convert RGB to XYZ, then XYZ to L*ab, then euclidean distance of L*ab source and compare
    Equations found here: https://www.easyrgb.com/en/math.php
    """
    # casts to float32 and creates a copy
    new_source = source.astype(np.float32)
    new_compare = compare.astype(np.float32)

    # RGB to XYZ
    for color in [new_source, new_compare]:
        color /= 255
        mask = color > 0.04045
        color[mask] = np.power((color[mask] + 0.055) / 1.055, 2.4)
        color[~mask] /= 12.92
        color *= 100
        x = color[0] * 0.4124 + color[1] * 0.3576 + color[2] * 0.1805
        y = color[0] * 0.2126 + color[1] * 0.7152 + color[2] * 0.0722
        z = color[0] * 0.0193 + color[1] * 0.1192 + color[2] * 0.9505
        color[:] = [x, y, z]

    # XYZ to CIE L*ab
    # default: x_ref=95.047, y_ref=100., z_ref=108.883
    for color in [new_source, new_compare]:
        color[0] /= 95.047
        color[1] /= 100
        color[2] /= 108.883

        mask = color > 0.008856
        color[mask] = np.cbrt(color[mask])
        color[~mask] = (7.787 * color[~mask]) + (16/116)
        # color *= 100
        L = 116 * color[1] - 16
        a = 500 * (color[0] - color[1])
        b = 200 * (color[1] - color[2])
        color[:] = [L, a, b]

    # can use euclidean color distance since it implements same algorithm anyway
    return _euclid_color_distance(new_source, new_compare)


@njit(fastmath=True)
def color_distance(source: np.ndarray, compare: np.ndarray) -> int:
    """Returns the color distance between RGB ndarray source and RGB ndarray compare. Uses the color distance method given."""
    match COLOR_DISTANCE_METHOD:
        case "redmean":
            c_dist_func = _redmean_color_distance
        case "euclidean":
            c_dist_func = _euclid_color_distance
        case "deltaE":
            c_dist_func = _delta_e_distance
        case _:
            raise TypeError(
                "Invalid COLOR_DISTANCE_METHOD for is_near_color function. Please provide a correct color distance function.")
    return c_dist_func(np.asarray(source), np.asarray(compare))


def is_near_color(source: RGB, compare: RGB, max_distance) -> bool:
    """Returns true if the source RGB and compare RGB are less than a certain `max_distance` away from each other using `color_distance`."""
    return color_distance(np.asarray(source), np.asarray(compare)) < max_distance


def most_frequent_distinct_RGB(image_array: np.ndarray, num_colors: int = 10) -> list[RGB]:
    """A multi-step process that flattens the image array, identifies the most frequent colors, filters through them using `is_color_near` to ensure the colors are distinct enough, then returns that filtered list of RGB values."""
    PROGRESS_LOG.log(
        "GETTING INPUT IMAGE'S MOST FREQUENT COLORS TO CREATE PALETTE (may take a minute)")

    # first, flatten the 2D array of pixel data to a 1D array of pixel data
    # see: https://stackoverflow.com/a/26553855
    flattened = image_array.reshape(-1, image_array.shape[-1])

    # next, find the 20 most frequent unique values (with their counts) on axis 0 (prevents flattening the last dimension)
    values, counts = np.unique(flattened, return_counts=True, axis=0)
    ind = np.argpartition(-counts, kth=min(len(counts)-1,  # set max partitions to the settings.env specified or the maximum supported by the image
                          PARTITION_KTH))[:PARTITION_KTH]

    # seperate out colors that are non-distinct. Since the default palette is guaranteed to be there, make them all distinctive colors.
    # segregate default palette colors and custom distinctive colors, and apply different weights

    most_freq_color = RGB(
        int(values[ind[0]][0]),
        int(values[ind[0]][1]),
        int(values[ind[0]][2])
    )

    distinctive_colors_filter = [*DEFAULT_PALETTE, most_freq_color]
    extra_palette_colors = []  # colors actually outputted and to be added to palette

    # I most definitely should move this into it's own function, but I am frankly tired. No thanks!
    cur_color = 1
    while len(extra_palette_colors) < num_colors and cur_color < len(ind):
        array_color = values[ind[cur_color]]
        rgb = RGB(
            int(array_color[0]),
            int(array_color[1]),
            int(array_color[2])
        )
        for color in distinctive_colors_filter:
            # if the array_color is distinct from all other colors in distinct_colors, add it

            if is_near_color(rgb, color, DISTINCTIVENESS_VALUE):
                # it isn't distinct, so don't bother adding it
                break
        else:
            distinctive_colors_filter.append(rgb)
            extra_palette_colors.append(rgb)
        # increment
        cur_color += 1
    return extra_palette_colors
