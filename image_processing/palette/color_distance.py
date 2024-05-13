from math import sqrt
from image_processing.palette.palette import RGB, DEFAULT_PALETTE
import numpy as np
from numba import njit


# Different ways of calculating distinctiveness value:
# Calculate the color distance between every single pixel, and average that
# Optimize this by reducing the resolution to a low amount


# What kind of color distance method to use, either "redmean", "euclidean", or others soon to be added. Different methods produce different results.
COLOR_DISTANCE_METHOD = "redmean"

# How distinct the colors generated need to be. Default value should be 500.
# Decreasing generally produces more similar colors
# Increasing generally produces more different colors
DISTINCTIVENESS_VALUE = {
    "redmean": 500,
    "euclidean": 10
}[COLOR_DISTANCE_METHOD]

# Search through only PARTITION_KTH of the most frequent colors to find distinct colors to add to the palette.
# Smaller the number, faster the distinct colors are found.
# Best not to touch
PARTITION_KTH = 5000


# All functions having to do with color distance, whether the colors are near each other, or if colors are distinct

@njit(fastmath=True)
def _redmean_color_distance(source: np.ndarray, compare: np.ndarray) -> int:
    """Utilizes the low-cost approximation algorithm found here:
    https://www.compuphase.com/cmetric.htm
    https://en.wikipedia.org/wiki/Color_difference -> "redmean"

    This algorithm will run for every pixel in the image, for every palette color (20 or 30). 
    Since the palette color is a constant... technically the whole process is only O(n) where n is the number of pixels...
    Yeah... funny... in reality there's a HUGE amount of pixels (width x height).
    We're iterating over every row, and then over every column, and then over every column, and then, applying this algorithm to every color pixel.
    Looking to optimize with Numba
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
    """Basic Euclidean color distance using a standard distance formula."""
    red_diff = source[0] - compare[0]
    green_diff = source[1] - compare[1]
    blue_diff = source[2] - compare[2]
    return int(sqrt(red_diff * red_diff + green_diff * green_diff + blue_diff * blue_diff))


@njit(fastmath=True)
def color_distance(source: np.ndarray, compare: np.ndarray) -> int:
    """Returns the color distance between RGB ndarray source and RGB ndarray compare. Uses the color distance method given."""
    match COLOR_DISTANCE_METHOD:
        case "redmean":
            c_dist_func = _redmean_color_distance
        case "euclidean":
            c_dist_func = _euclid_color_distance
        case _:
            raise TypeError(
                "Invalid COLOR_DISTANCE_METHOD for is_near_color function. Please provide a correct color distance function.")
    return c_dist_func(np.asarray(source), np.asarray(compare))


def is_near_color(source: RGB, compare: RGB, max_distance) -> bool:
    """Returns true if the source RGB and compare RGB are less than a certain `max_distance` away from each other using `color_distance`."""
    return color_distance(np.asarray(source), np.asarray(compare)) < max_distance


def most_frequent_distinct_RGB(image_array: np.ndarray, num_colors: int = 10) -> list[RGB]:
    """A multi-step process that flattens the image array, identifies the most frequent colors, filters through them using `is_color_near` to ensure the colors are distinct enough, then returns that filtered list of RGB values."""
    # first, flatten the 2D array of pixel data to a 1D array of pixel data
    # see: https://stackoverflow.com/a/26553855
    flattened = image_array.reshape(-1, image_array.shape[-1])

    # next, find the 20 most frequent unique values (with their counts) on axis 0 (prevents flattening the last dimension)
    values, counts = np.unique(flattened, return_counts=True, axis=0)
    ind = np.argpartition(-counts, kth=PARTITION_KTH)[:PARTITION_KTH]

    # seperate out colors that are non-distinct. Since the default palette is guaranteed to be there, make them all distinctive colors.
    distinctive_colors_filter = [*DEFAULT_PALETTE]  # colors to filter by
    extra_palette_colors = []  # colors actually outputted and to be added to palette

    # I most definitely should move this into it's own function, but I am frankly tired. No thanks!
    cur_color = 0
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
