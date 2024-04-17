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
    IM.set_brush("airbrush")
    IM.set_stroke_size(4)
    IM.click_bucket()
    IM.click_brush()
    IM.click_color_two()
    IM.click_color_one()
    IM.click_color_two()
    IM.click_color_one()
    IM.click_color_two()
    IM.click_color_one()
    IM.click_color_two()
    IM.click_color_one()
    IM.click_color_two()
