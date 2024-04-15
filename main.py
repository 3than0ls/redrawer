# import PIL


# # TODO: Read image, pixel by pixel, and convert into a set of instructiosn
# #    look into https://stackoverflow.com/questions/3241929/how-to-find-the-dominant-most-common-color-in-an-image
# # TODO: Get settings of buttons
# # TODO: ADD A CLEAR CANCEL
# # TODO: use pyautogui to draw it
# # TODO: Add a tkinter gui to it all


from interactions import InteractionsManager
from window import PaintWindow
import time

if __name__ == '__main__':
    window = PaintWindow()
    window.initialize_window()
    IM = InteractionsManager(window)
    for i in range(0, 10):
        time.sleep(0.25)
        IM._set_color(2, i)
