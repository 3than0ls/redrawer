from math import sqrt
from image_processing.palette.palette import RGB, DEFAULT_PALETTE
import numpy as np


# All functions having to do with color distance, whether the colors are near each other, or if colors are distinct


def color_distance(source: RGB, compare: RGB) -> int:
    """Utilizes the low-cost approximation algorithm found here:
    https://www.compuphase.com/cmetric.htm

    This algorithm will run for every pixel in the image, for every palette color (20 or 30). 
    Since the palette color is a constant... technically the whole process is only O(n) where n is the number of pixels...
    Yeah... funny... in reality there's a HUGE amount of pixels (width x height).
    We're iterating over every row, and then over every column, and then over every column, and then, applying this algorithm to every color pixel.
    Looking to optimize with Numba
    """
    mean_red = (source.red + compare.red) / 2
    red_diff = source.red - compare.red
    green_diff = source.green - compare.green
    blue_diff = source.blue - compare.blue
    return int(sqrt(
        (512 + mean_red) * red_diff * red_diff +
        4 * green_diff * green_diff +
        (767-red_diff) * blue_diff * blue_diff
    ))


def is_near_color(source: RGB, compare: RGB, max_distance=50) -> bool:
    return color_distance(source, compare) < max_distance


# How distinct the colors generated need to be. Default value should be 50.
# Decreasing generally produces more similar colors
# Increasing generally produces more different colors
DISTINCTIVENESS_VALUE = 250

# Search through only PARTITION_KTH of the most frequent colors to find distinct colors to add to the palette.
PARTITION_KTH = 250


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
