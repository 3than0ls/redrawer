from interactions.cursor import Point
from image_processing import Palette
from interactions.universals import UniversalInteractionsHeader
from dataclasses import dataclass
import interactions.constants as C
from interactions.window import BoundingRect
from pynput.keyboard import Key


class ResizeNotFitWindowError(Exception):
    """Raised when the canvas is attempted to be resized a size that exceeds canvas dimensions."""

    def __init__(self, width: int, height: int, window_size: BoundingRect):
        canvas_width = window_size.width - \
            C.CANVAS_TOP_LEFT[0] - C.CANVAS_RIGHT_PADDING
        canvas_height = window_size.height - \
            C.CANVAS_TOP_LEFT[1] - C.CANVAS_BOTTOM_PADDING
        super().__init__(f"""Cannot resize canvas to size of {width}x{
            height} without requiring scrollbar. Maximum possible size for canvas is {canvas_width}x{canvas_height}.""")


@dataclass
class _ColorSelected:
    """Represents the row, column selected in the color palette. ColorSelected is unaware of what actual color has been chosen. Default values are row 0 and column 0 (black color), because default color is black."""
    row: int = 0
    col: int = 0

    def __post_init__(self) -> None:
        """Ensure column is less than equal 9, and row is less than equal 2."""
        if self.row > 2:
            raise ValueError(f"ColorSelected row of {
                             self.row} is invalid, must be less than or equal to 3.")

        if self.col > 9:
            raise ValueError(f"ColorSelected column of {
                             self.col} is invalid, must be less than or equal to 9.")

    def cursor_position(self) -> Point:
        """Return the cursor position of the selected color (always relative to top-left of window)."""
        x = C.COLOR_OPTIONS_TOP_LEFT[0] + self.col * C.COLOR_OPTIONS_OFFSET
        y = C.COLOR_OPTIONS_TOP_LEFT[1] + self.row * C.COLOR_OPTIONS_OFFSET
        return Point(x, y)


class ToolbarInteractions(UniversalInteractionsHeader):
    def __init__(self) -> None:
        super().__init__()

        # tracks what color is selected from the palette
        self._color_selected = _ColorSelected()

    def _set_color(self, row: int, col: int) -> None:
        self._color_selected = _ColorSelected(row, col)
        self._click(self._color_selected.cursor_position())

    def set_palette(self, palette: Palette) -> None:
        # TODO: Set palette
        pass

    def _ensure_resize_fits(self, width: int, height: int) -> bool:
        """Ensure resize is not greater than the size of the screen, or _window_rect. For this, we'll use constant paddings. 
        A more accurate solutions would be to use paddings based off of the actual available canvas size, 
        which ends above the bottom information bar. Perhaps in future do this."""
        return \
            width <= self._bounding_rect.width - C.CANVAS_TOP_LEFT[0] - C.CANVAS_RIGHT_PADDING \
            and \
            height <= self._bounding_rect.height - \
            C.CANVAS_TOP_LEFT[1] - C.CANVAS_BOTTOM_PADDING

    def resize(self, width: int, height: int) -> None:
        """Resize the canvas to a given `width` and `height`. Both dimensions must be small enough so that no scrollbar effect appears."""
        if not self._ensure_resize_fits(width, height):
            raise ResizeNotFitWindowError(width, height, self._bounding_rect)

        self._click(C.RESIZE_BUTTON, pre_delay=C.TOOLBAR_DROPDOWN_DELAY)
        self._click(C.RESIZE_MENU_PIXELS)
        self._click(C.RESIZE_MENU_MAINTAIN_ASPECT)
        self._click(C.RESIZE_MENU_H, num_clicks=2)
        self._keyboard.tap(Key.delete)
        self._keyboard.type(str(width))
        self._click(C.RESIZE_MENU_V, num_clicks=2)
        self._keyboard.tap(Key.delete)
        self._keyboard.type(str(height))
        self._keyboard.tap(Key.enter)
        # self._click(C.RESIZE_MENU_OK, post_delay=C.TOOLBAR_DROPDOWN_DELAY)

    def click_bucket(self) -> None:
        """Click the bucket button."""
        self._click(C.BUCKET_BUTTON)

    def click_brush(self) -> None:
        """Click the brush button."""
        self._click(C.BRUSH_BUTTON)

    def click_color_one(self) -> None:
        """Click the first color."""
        self._click(C.COLOR_1_BUTTON)

    def click_color_two(self) -> None:
        """Click the second color."""
        self._click(C.COLOR_2_BUTTON)

    def set_brush(self, brush_type: str) -> None:
        """
        Set the brush type. Brush type can be: 
        `brush`, 
        `calligraphy_brush_1`,
        `calligraphy_brush_2`,
        `airbrush`,
        `oil_brush`,
        `crayon`,
        `marker`,
        `natural_pencil`, or
        `watercolor_brush`.
        """
        if brush_type not in C.BRUSH_TYPES.keys():
            raise ValueError(
                f"Brush type {brush_type} is not a valid brush type.")

        self._click(C.BRUSH_TYPE_BUTTON, pre_delay=C.TOOLBAR_DROPDOWN_DELAY)
        self._click(C.BRUSH_TYPES[brush_type],
                    pre_delay=C.TOOLBAR_DROPDOWN_DELAY)

    def set_stroke_size(self, size_number: int) -> None:
        """Set stroke size to size `size_number`, where `size_number` is the size between 1 and 4 in the dropdown menu when clicking the Size button."""
        if size_number < 1 or size_number > 4:
            raise ValueError(
                f"Stroke size {size_number} is not a valid. Must be between 1 and 4 (inclusive).")

        self._click(C.STROKE_SIZE_BUTTON, pre_delay=C.TOOLBAR_DROPDOWN_DELAY)
        self._click(C.STROKE_SIZES[str(size_number)],
                    pre_delay=C.TOOLBAR_DROPDOWN_DELAY)
