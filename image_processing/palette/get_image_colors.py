from pathlib import Path
from PIL import Image
from dotenv import dotenv_values
import numpy as np
from image_processing.palette.color_distance import most_frequent_distinct_RGB
from image_processing.palette.palette import Palette
from image_processing.image.resize import resize_to_monitor


def open_image(path: Path, resize=True) -> np.ndarray:
    """Open an image and convert it into a Numpy array of shape width x height x RGB. If `resize` is set to true, then also resize it to be smaller than the active monitor."""
    img = Image.open(path, formats=["PNG", "JPEG"]).convert('RGB')
    if resize:
        img = resize_to_monitor(img)

    array = np.asarray(img, dtype=np.uint8)
    # array = np.asarray(img, dtype=np.int32)
    return array


def create_palette(image_array: np.ndarray) -> Palette:
    """Create a full palette from an numpy image array. Does this by determining all distinct colors from the numpy array."""
    extra_colors = most_frequent_distinct_RGB(image_array)
    palette = Palette(extra_colors)
    return palette
