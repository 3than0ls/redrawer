
from image_processing.palette.palette import RGB, Palette
import numpy as np
from PIL import Image


def _translate_palette_indices_to_rgb(palette_image_array: np.ndarray, palette: Palette) -> np.ndarray:
    def _translate(palette_index_arr: np.ndarray):
        # rgb = np.ndarray([*palette.palette[palette_index_arr[0]]
        #                  [palette_index_arr[1]]], dtype=np.uint8)
        rgb = np.asarray(
            palette.palette[palette_index_arr[0]][palette_index_arr[1]], dtype=np.uint8)
        # print(rgb)
        return rgb

    return np.apply_along_axis(_translate, 2, palette_image_array)


def show_image_from_palette_array(palette_image_array: np.ndarray, palette: Palette) -> None:
    img_array = _translate_palette_indices_to_rgb(
        palette_image_array, palette)
    print(img_array)
    print(img_array.shape)
    img = Image.fromarray(_translate_palette_indices_to_rgb(
        palette_image_array, palette), 'RGB')
    img.show()
