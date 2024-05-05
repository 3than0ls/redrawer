from pathlib import Path
from PIL import Image
import numpy as np
from pixel_comparison import is_near_color
from palette import DEFAULT_PALETTE, Palette, RGB

# How distinct the colors generated need to be. Default value should be 50.
# Decreasing generally produces more similar colors
# Increasing generally produces more different colors
DISTINCTIVENESS_VALUE = 250

# Search through only PARTITION_KTH of the most frequent colors to find distinct colors to add to the palette.
PARTITION_KTH = 250


def open_image(path: Path) -> np.ndarray:
    """Open an image and convert it into a Numpy array."""
    img = Image.open(path, formats=["PNG", "JPEG"]).convert('RGB')
    array = np.asarray(img, dtype=np.uint8)
    # array = np.asarray(img, dtype=np.int32)
    return array


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

    # Old method
    # for array_color in values[ind]:
    #     rgb = RGB(
    #         int(array_color[0]),
    #         int(array_color[1]),
    #         int(array_color[2])
    #     )
    #     for color in distinctive_colors_filter:
    #         # if the array_color is distinct from all other colors in distinct_colors, add it
    #         if is_near_color(rgb, color, DISTINCTIVENESS_VALUE):
    #             # it isn't distinct, so don't bother adding it
    #             break
    #     else:
    #         distinctive_colors_filter.append(rgb)
    #         extra_palette_colors.append(rgb)
    # return extra_palette_colors[:num_colors]


if __name__ == '__main__':
    # A PNG that is 617x356 in dimension
    images = [r"images\test1.PNG", r"images\test2.jpg",
              r"images\test3.jpg", r"images\test4.jpg"]
    temp = Path(images[3])
    array = open_image(temp)
    # print(array)
    print(array.shape)
    print(array.size)
    extra_colors = most_frequent_distinct_RGB(array)
    palette = Palette(extra_colors[:10])
    print(palette)
    palette.show_in_image()
