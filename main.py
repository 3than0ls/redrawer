from pathlib import Path
from pathlib import Path

from redrawer import Redrawer


if __name__ == '__main__':

    images = [r"images\test1.PNG", r"images\test2.jpg",
              r"images\test3.jpg", r"images\test4.jpg", r"images\test5.jpg", r"images\test6.png"]

    rd = Redrawer(Path(images[0]))
    rd.redraw()
