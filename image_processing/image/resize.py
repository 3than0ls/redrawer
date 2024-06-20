from screeninfo import get_monitors
from PIL.Image import Image
# Resizes images that are too large to fit the size of the current monitor, since it'll be re-drawn in paint anyway


def resize_to_monitor(image: Image) -> Image:
    """Resize the image to fit in the smallest monitor on the system."""
    min_size = sorted(get_monitors(), key=lambda m: m.width * m.height)[0]

    image.thumbnail((min_size.width * 0.75, min_size.height * 0.75))
    return image
