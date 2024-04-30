from cursor import Point
from interactions.universals import UniversalInteractionsHeader
from interactions.constants import CANVAS_TOP_LEFT


class CanvasInteractions(UniversalInteractionsHeader):
    def __init__(self) -> None:
        super().__init__()

    def _transform_point_to_canvas(self, point: Point) -> Point:
        """Transforms point so that it is relative to the canvas top left. Essentially adds the canvas top-left to the point."""
        return Point(CANVAS_TOP_LEFT[0] + point.x, CANVAS_TOP_LEFT[1] + point.y)

    def canvas_click(self, point: Point) -> None:
        """Click on the canvas relative to the top left of the canvas section of the window."""
        self._click(self._transform_point_to_canvas(point))

    def canvas_drag(self, point1: Point, point2: Point) -> None:
        """Hold and drag the cursor from `point1` to `point2` on the canvas."""
        self._mouse.hold(
            initial_position=self._transform_point_to_canvas(point1))
        self._mouse.release(
            initial_position=self._transform_point_to_canvas(point2))

    # TODO: add a get max canvas size function, based on bottom and right padding constants
    # perhaps make it a part of the manager?
