from interactions.window import PaintWindow, BoundingRect
from interactions.cursor import Cursor, Point
from interactions.toolbar import ToolbarInteractions
from interactions.canvas import CanvasInteractions
from pynput import keyboard
import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class InteractionsManager(ToolbarInteractions, CanvasInteractions, metaclass=Singleton):
    r"""
    Here, inherit all methods from ToolbarInteractions and CanvasInteractions, whilst also defining methods used by both here.
     Neither individual interaction classes will be used other than for InteractionsManager, so we need not worry about any issues about defining these universal methods may cause.
     Additionally, universal methods will be declared for ease of use and type annotation.
    ```none

                            UniversalInteractionsHeader   <--------------------\
                                       |                                        |
                                       | < provides universal declarations      |
                                       |           that are used by all         |
                 ______________________|_______________                         |
                /                                      \                        |
        ToolbarInteractions                   CanvasInteractions                |
                \______________________________________/                        |  < provides universal definitions 
                                    |                                           |           that are used by ..
                           InteractionsManager                                  |
                                    |                                           |
                      (defined needed instance properties in init) -------------/
    ```
     The idea behind this is that I can write the code for Toolbar and Canvas interactions in seperate classes, even though they rely on attributes that are only defined in InteractionsManager
     I also need one single class/point to access all of it from.


     NEW IDEA:

     Perhaps only have GrandSuperClass (currently UnivInterHeader), then create and define all T and C interactions, 
     then dynamically add each non-superclass method from the two subclasses back into the GrandSuperClass
     """

    def __init__(self, window: PaintWindow) -> None:
        self._window = window
        self._bounding_rect = window.window_rect()

        self._mouse = Cursor(window)
        self._keyboard = keyboard.Controller()
