from pathlib import Path
from PIL import Image
import numpy as np
from image_processing.palette.color_distance import most_frequent_distinct_RGB
from image_processing.palette.palette import Palette


def open_image(path: Path) -> np.ndarray:
    """Open an image and convert it into a Numpy array of shape width x height x RGB."""
    img = Image.open(path, formats=["PNG", "JPEG"]).convert('RGB')
    array = np.asarray(img, dtype=np.uint8)
    # array = np.asarray(img, dtype=np.int32)
    return array


def create_palette(image_array: np.ndarray) -> Palette:
    """Create a full palette from an numpy image array. Does this by determining all distinct colors from the numpy array."""
    extra_colors = most_frequent_distinct_RGB(image_array)
    return Palette(extra_colors)
