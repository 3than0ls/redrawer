from cursor import Point
from interactions.universals import UniversalInteractionsHeader
from dataclasses import dataclass
import interactions.constants as C
import time


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

    def set_palette(self, palette: "Palette") -> None:
        pass

    def resize(self, width: int, height: int) -> None:
        """Ensure resize is not greater than the size of the screen, or _window_rect"""
        pass

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
