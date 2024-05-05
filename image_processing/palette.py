from collections import namedtuple
import json
from pathlib import Path
from PIL import Image


RGB = namedtuple("RGB", ["red", "green", "blue"], defaults=[0, 0, 0])


with open(Path('./image_processing/default_palette.json')) as f:
    # all colors in RGB tuple
    _default_palette = []

    for i, row in enumerate(json.load(f)["palette"]):
        _default_palette.append([])
        for rgb in row:
            _default_palette[i].append(RGB(*rgb))


print(_default_palette)
# flattened version of _default_palette
DEFAULT_PALETTE = [rgb for row in _default_palette for rgb in row]


class Palette:
    """
    Palette may vary from image to image, but always have a base of the default palette. Hence this class.
    Palette property is structured like this: 
    A 3x10 2D list where it's seperated into 2 or 3 rows (depending on if the full palette has been initialized) and 10 columns
    """

    def __init__(self, extra_colors: list[RGB] | None = None) -> None:
        if extra_colors is not None and len(extra_colors) > 10:
            raise ValueError(f"Cannot add {len(
                extra_colors)} extra colors. Max extra colors to add to the palette is 10.")

        self._palette: list[list[RGB]] = list(_default_palette)
        if extra_colors:
            self._palette.append([rgb_color for rgb_color in extra_colors])

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self._palette[0]), len(self._palette))

    @property
    def palette(self) -> list[list[RGB]]:
        return self._palette

    def show_in_image(self) -> None:
        """Creates a temporary image that shows the color palette. Typically used for testing purposes"""
        scale = 100

        shape = self.shape
        img = Image.new(mode="RGB", size=(shape[0]*scale, shape[1]*scale))
        img.load()
        for i, row in enumerate(self.palette):
            for j, color in enumerate(row):
                for x in range(0, scale):
                    for y in range(0, scale):
                        img.putpixel(
                            (j*scale+x, i*scale+y), (color.red, color.green, color.blue))
        img.show()

    def __repr__(self) -> str:
        out = ""
        for row in self._palette:
            for rgb in row:
                out += f"|RGB({rgb.red}, {rgb.green}, {rgb.blue})|"
            out += "\n\n"
        # out.replace(".", "\n\n\n")
        # out.replace(".", "")
        return out
