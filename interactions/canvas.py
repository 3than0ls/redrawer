import time
from interactions.cursor import Point
from interactions.universals import UniversalInteractionsHeader
from interactions.constants import CANVAS_TOP_LEFT, DEFAULT_DELAY


class CanvasInteractions(UniversalInteractionsHeader):
    def __init__(self) -> None:
        super().__init__()

    def _transform_point_to_canvas(self, point: Point) -> Point:
        """Transforms point so that it is relative to the canvas top left. Essentially adds the canvas top-left to the point."""
        return Point(CANVAS_TOP_LEFT[0] + point.x, CANVAS_TOP_LEFT[1] + point.y)

    def canvas_click(self, point: Point) -> None:
        """Click on the canvas relative to the top left of the canvas section of the window."""
        self._click(self._transform_point_to_canvas(point))

    def canvas_drag(self, start_point: Point, end_point: Point) -> None:
        """Hold and drag the cursor from `start_point` to `end_point` on the canvas."""
        self._mouse.hold(
            initial_position=self._transform_point_to_canvas(start_point))
        time.sleep(DEFAULT_DELAY)
        self._mouse.release(
            initial_position=self._transform_point_to_canvas(end_point))
        time.sleep(DEFAULT_DELAY)

    def canvas_drag_to(self, end_point: Point) -> None:
        """Hold and drag the cursor from last cursor location to `end_point` on the canvas."""
        self._mouse.hold()
        self._mouse.release(
            initial_position=self._transform_point_to_canvas(end_point))
        time.sleep(DEFAULT_DELAY)

    # TODO: add a get max canvas size function, based on bottom and right padding constants
    # perhaps make it a part of the manager?
