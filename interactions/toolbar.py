from cursor import Point
from interactions.universals import UniversalInteractionsHeader, INTERACTION_POINTS
from dataclasses import dataclass


_TOOLBAR = INTERACTION_POINTS["Toolbar"]
_COLOR_OPTIONS_TOP_LEFT = _TOOLBAR["colors_option"]["top-left"]
_COLOR_OPTIONS_OFFSET = _TOOLBAR["colors_option"]["offset"]


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
        x = _COLOR_OPTIONS_TOP_LEFT[0] + self.col * _COLOR_OPTIONS_OFFSET
        y = _COLOR_OPTIONS_TOP_LEFT[1] + self.row * _COLOR_OPTIONS_OFFSET
        return Point(x, y)


class ToolbarInteractions(UniversalInteractionsHeader):
    def __init__(self) -> None:
        super().__init__()

        # tracks what color is selected from the palette
        self._color_selected = _ColorSelected()

    def _set_color(self, row: int, col: int) -> None:
        self._color_selected = _ColorSelected(row, col)
        self._click(self._color_selected.cursor_position())

    def set_palette(self) -> None:
        pass

    def next_color(self) -> None:
        pass
