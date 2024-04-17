import json
from pathlib import Path

with open(Path('./interactions/interaction_points.json')) as f:
    # all units in pixels
    INTERACTION_POINTS = IP = json.load(f)

# ----- Delays -----
TOOLBAR_DROPDOWN_DELAY = 0.4


# ----- Toolbar related constants -----
TOOLBAR = IP["Toolbar"]
# --- Color palette and custom options
COLOR_OPTIONS_TOP_LEFT: tuple[int, int] = TOOLBAR["colors_option"]["top-left"]
COLOR_OPTIONS_OFFSET: int = TOOLBAR["colors_option"]["offset"]
# --- Bucket
BUCKET_BUTTON: tuple[int, int] = TOOLBAR["bucket"]
# --- Brush
BRUSH_BUTTON: tuple[int, int] = TOOLBAR["brush"]
# --- Color 1
COLOR_1_BUTTON: tuple[int, int] = TOOLBAR["color_1"]
# --- Color 2
COLOR_2_BUTTON: tuple[int, int] = TOOLBAR["color_2"]
# --- Brush type
BRUSH_TYPE_BUTTON: tuple[int, int] = TOOLBAR["brushes"]["button"]
BRUSH_TYPES: dict[str, tuple[int, int]] = TOOLBAR["brushes"]["menu"]
# BRUSH_TYPE_DICT = {
#     1: "brush",
#     2: "calligraphy_brush_1",
#     3: "calligraphy_brush_2",
#     4: "airbrush",
#     5: "oil_brush",
#     6: "crayon",
#     7: "marker",
#     8: "natural_pencil",
#     9: "watercolor_brush"
# }
# --- Stroke
STROKE_SIZE_BUTTON: tuple[int, int] = TOOLBAR["stroke_size"]["button"]
STROKE_SIZES: dict[str, tuple[int, int]] = TOOLBAR["stroke_size"]["menu"]


# ----- Canvas related constants -----
CANVAS = INTERACTION_POINTS["Canvas"]
CANVAS_TOP_LEFT = CANVAS["top-left"]
