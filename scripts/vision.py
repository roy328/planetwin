import pyautogui
import cv2
import numpy as np
from config import (BOARD_LOWER_COLOR, BOARD_HIGHER_COLOR)

class Vision():
    def __init__(self, username):
        self.threshold = 0.65
        self.username = username
        self.screen = None
        self.board_area = None
        self.player1 = None
        self.player2 = None
        self.player3 = None
        self.player4 = None
        self.player5 = None
        self.player6 = None
        self.me = None

    def cards(self):
        print("cards .... ", self.username)
        self.screen_shot()

    def read_all_player(self) -> None:
        height, width = self.board_area.shape[:2]
        
        # Calculate the mid points
        third_height = height // 3
        third_width = width // 3

        # Split the image into four quadrants
        self.player6 = self.board_area[third_height * 2:height, 0:third_width]      # Top-Left
        cv2.imwrite('screenshots/player6.png', self.player6)
        self.player1 = self.board_area[third_height * 2:height, third_width:third_width * 2]  # Top-Right
        cv2.imwrite('screenshots/player1.png', self.player1)
        self.player2 = self.board_area[third_height * 2:height, third_width * 2:width]  # Top-Right
        cv2.imwrite('screenshots/player2.png', self.player2)
        self.player3 = self.board_area[0:third_height, third_width * 2:width] # Bottom-Left
        cv2.imwrite('screenshots/player3.png', self.player3)
        self.player4 = self.board_area[0:third_height, third_width:third_width * 2] # Bottom-Right
        cv2.imwrite('screenshots/player4.png', self.player4)
        self.player5 = self.board_area[0:third_height, 0:third_width] # Bottom-Right
        cv2.imwrite('screenshots/player5.png', self.player5)


    def crop_board_area(self):
        if self.screen is None:
            raise ValueError("Image not found or could not be loaded.")
    
        # Convert the image from BGR to RGB (or use HSV if preferred)
        img_rgb = cv2.cvtColor(self.screen, cv2.COLOR_BGR2RGB)

        # Create a mask based on the specified color range
        lower_bound = np.array(BOARD_LOWER_COLOR)
        upper_bound = np.array(BOARD_HIGHER_COLOR)
        mask = cv2.inRange(img_rgb, lower_bound, upper_bound)

        # Zero out mask pixels to the left of start_x
        mask[:, :200] = 0

        # Find contours in the masked image
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print("No areas found with the specified color range.")
            return None

        # Get the bounding rectangle that includes all contours
        x, y, w, h = cv2.boundingRect(np.vstack(contours))

        # Crop the region of interest from the original image
        self.board_area = self.screen[y-50:y+h+50, x-50:x+w+50]
        cv2.imwrite('screenshots/screenshot4.png', self.board_area)

    def screen_shot(self, gray_convert: bool = False):
        print("take screen shot..")
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshots/screenshot1.png")
        self.screen = np.array(screenshot)
        cv2.imwrite('screenshots/screenshot2.png', self.screen)
        self.crop_board_area()
        self.read_all_player()
        if not gray_convert:
            self.screen = cv2.cvtColor(self.screen, cv2.COLOR_RGB2GRAY)
            cv2.imwrite('screenshots/screenshot3.png', self.screen)


