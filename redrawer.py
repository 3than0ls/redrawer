

import dbm
from pathlib import Path

from image_processing import create_palette, open_image, create_processed_image, show_image
from instructions import from_processed_image

from interactions import PaintWindow, InteractionsManager, Point
from dotenv import dotenv_values

from logger import PROGRESS_LOG


_settings = dotenv_values("settings.env")
INSTRUCTION_TYPE = _settings["INSTRUCTION_TYPE"]
SHOW_PALETTE = _settings["SHOW_PALETTE"] == "true"
SHOW_PROCESSED_IMAGE = _settings["SHOW_PROCESSED_IMAGE"] == "true"
BRUSH_TYPE = _settings["BRUSH_TYPE"]
STROKE_SIZE = _settings["STROKE_SIZE"]


class ImagePathError(Exception):
    def __init__(self, source_image_path: Path):
        super().__init__(f"The path \"{
            source_image_path}\" either does not exist or is not a valid image type (PNG, JPG)")


# as different redrawer types are created, it should most definitely be split up into seperate files and it's own module
class _BasicRedrawer:
    def __init__(self, interactions_manager: InteractionsManager, instruc_path: Path):
        """Redrawing process for basic redrawing method. To be "injected" into the main Redrawer."""
        self._interactions_manager = interactions_manager
        self._instruc_path = instruc_path

    def _redraw_first_color(self) -> None:
        """A special redrawing method for the most frequent color, rather than drag drawing, buckets the canvas. Assumes correct color is selected"""
        self._interactions_manager.click_bucket()
        self._interactions_manager.canvas_click(Point(5, 5))
        self._interactions_manager.set_brush("brush")

    def _redraw_one_color(self, color_instrucs: str) -> None:
        """The redrawing of exactly one color, meaning a bunch of clicks and drags."""
        # note the splice [:-1] to get rid of the last "empty" element
        for instruc in color_instrucs.split(";")[:-1]:
            # remove the surrounding braces and split by delimeter
            x, y, length = instruc[1:-1].split(",")
            x = int(x)
            y = int(y)
            length = int(length)
            # if smallest stroke size, clicking simply will not draw anything for some odd reason. Thus, we have to drag at least one px, thus add one in length
            length += 1 if STROKE_SIZE == 1 else 0
            if length == 1:
                self._interactions_manager.canvas_click(Point(x, y))
            else:
                self._interactions_manager.canvas_drag(
                    Point(x, y), Point(x+length, y))

    def redraw(self, ordered_drawing_keys: list["dbm._KeyType"]) -> None:
        """Basic redrawing function for basic redrawing"""
        with dbm.open(self._instruc_path, 'r') as instrucs:
            for cur_color_num, key in enumerate(ordered_drawing_keys):
                row, col = key.decode().split(',')  # type: ignore
                self._interactions_manager.set_color(int(row), int(col))

                if cur_color_num == 0:  # first color, assuming ordered correctly, should be the most frequent, thus we can just bucket it
                    self._redraw_first_color()
                    continue

                PROGRESS_LOG.log(f"Selecting color at {row}, {col} to execute ~{len(
                    instrucs[key])} worth of redrawing instructions ({cur_color_num+1}/{len(ordered_drawing_keys)})")

                if instrucs[key].decode():  # skips any colors that have no instructions
                    self._redraw_one_color(instrucs[key].decode())


class Redrawer:
    def __init__(self, source_image_path: Path):
        """The main class of the entire program, responsible for wrapping all the different components together and redrawing the output.
        `source_image_path` is the path of your input image.
        Draws it in ms-paint (a length process), then saves the file in the same location as the input with '_redrawer' appended onto input image name as it's file name.
        """
        self._validate_image_path(source_image_path)
        self._source_path = source_image_path
        output_name = self._source_path.name + "_redrawer"
        self._output_path = self._source_path.parent / (output_name + ".png")

        self._compute_instructions()

        if SHOW_PALETTE:
            self._palette.show_in_image()
        if SHOW_PROCESSED_IMAGE:
            show_image(self._processed_img, self._palette)

        self._initialize_drawer()

    def _compute_instructions(self):
        """Set up and initialize components that support/calculate the instructions. Needs to be called before _initialize_drawer. 
        Outputs instructions to be used in the DBM found at `self._instruc_path`"""
        self._img = open_image(self._source_path)
        self._palette = create_palette(self._img)
        self._processed_img = create_processed_image(self._img, self._palette)
        # will be the same as the combined path found in settings.env
        self._instruc_path = from_processed_image(
            self._processed_img, self._palette)

    def _initialize_drawer(self):
        """Set up and initialize copmonents supporting the drawer (what interacts with the canvas). Needs to be called after _compute_instructions.
         Required `self._instruc_path` and corresponding DBM is created correctly."""
        PROGRESS_LOG.log("INITIALIZING PAINT WINDOW")
        self._window = PaintWindow()
        self._window.initialize_window()
        self._interactions_manager = InteractionsManager(self._window)
        self._drawer = _BasicRedrawer(
            self._interactions_manager, self._instruc_path)

        # set up some canvas settings
        self._interactions_manager.set_brush(BRUSH_TYPE)  # type: ignore
        self._interactions_manager.set_stroke_size(
            int(STROKE_SIZE))  # type: ignore

    def _validate_image_path(self, path: Path):
        """Validate the image path, raise an error otherwise."""
        if not path.exists or not path.is_file() or path.suffix.lower() not in [".png", ".jpeg", ".jpg"]:
            raise ImagePathError(path)

    def _order_drawing_keys(self) -> list:
        """Returns the sorted instruction keys by length of their corresponding instructions. 
        Intended to produce a drawing order where the most frequent colors are drawn first, without having to parse THEN count instructions."""
        data = []
        with dbm.open(self._instruc_path, 'r') as instrucs:
            for key in instrucs.keys():
                data.append((key, len(instrucs[key].split(b";"))))

        # sort by length of instructions
        return [key for (key, _) in sorted(data, key=lambda d: d[1], reverse=True)]

    def _setup(self) -> None:
        """Set up the the toolbar and canvas so redrawing goes without issues."""
        self._interactions_manager.resize(
            self._processed_img.shape[1],
            self._processed_img.shape[0]
        )
        self._interactions_manager.set_stroke_size(2)
        self._interactions_manager.set_palette(self._palette)

    def redraw(self) -> None:
        """The core function that executes everything."""
        PROGRESS_LOG.log("SETTING UP PAINT WINDOW AND CANVAS")
        self._setup()
        self._drawer.redraw(self._order_drawing_keys())
