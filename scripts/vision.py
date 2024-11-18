import pyautogui
import cv2
import numpy as np

class Vision():
    def __init__(self):
        self.threshold = 0.65

    def cards(self):
        gray_card = self.screen_shot()

    def screen_shot(self, gray_convert: bool = False):
        print("take screen shot..")
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot1.png")
        screen = np.array(screenshot)
        cv2.imwrite('screenshot2.png', screen)
        if gray_convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

        return screen