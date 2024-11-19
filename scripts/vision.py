import pyautogui
import cv2
import numpy as np
import pytesseract
import re
from config import (BOARD_LOWER_COLOR, BOARD_HIGHER_COLOR)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
class Vision():
    def __init__(self, username):
        self.threshold = 0.65
        self.username = username
        self.current_money = ""
        self.screen = None
        self.board_area = None
        self.me = dict()

    def cards(self):
        # print("cards .... ", self.username)
        self.screen_shot()
        self.crop_board_area()
        self.read_all_player()

    def extract_text_from_image(self, image: np.ndarray, num) -> str:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(f'screenshots/player{num + 6}.png', gray_image)
        text = pytesseract.image_to_string(gray_image)    
        return text.strip()

    def filter_extracted_text(self, extracted_text: str,  currency = "€") -> list:
        if self.username in extracted_text:
            return self.username
        else:
            return ""
    
    def get_player_info(self, player, num) -> bool:
        text = self.extract_text_from_image(player, num)
        # print(f"Text from Quadrant {num}\n{text}\n")
        filtered_text = self.filter_extracted_text(text)

        if filtered_text == self.username:
            for line in text.splitlines():
                match = re.findall(r'\S*€\S*', line)
                if match !=  [] and match is not None:
                    self.current_money = match[0]
            print(f"you are sitten at {num}th seat. {self.username}\nAnd your remaining money is {self.current_money}")
            return True
        # print(f"No matches found in {num}th seat.")
        return False

    def read_all_player(self) -> None:
        if self.board_area is None:
            return
        height, width = self.board_area.shape[:2]
        
        # Calculate the mid points
        third_height = height // 3
        third_width = width // 3

        # Split the image into four quadrants
        player = self.board_area[third_height * 2 + 50:height - 10, third_width + 20:third_width * 2 - 20]  # Top-Right
        found_me = self.get_player_info(player, 1)
        cv2.imwrite('screenshots/player1.png', player)
        if found_me: 
            return
        player = self.board_area[third_height * 2 + 25:height - 35, third_width * 2 + 60:width + 20]  # Top-Right
        found_me = self.get_player_info(player, 2)
        cv2.imwrite('screenshots/player2.png', player)
        if found_me: 
            return
        player = self.board_area[15:third_height -45, third_width * 2 + 20:width - 20] # Bottom-Left
        found_me = self.get_player_info(player, 3)
        cv2.imwrite('screenshots/player3.png', player)
        if found_me: 
            return
        player = self.board_area[0:third_height - 60, third_width + 20:third_width * 2 - 20] # Bottom-Right
        found_me = self.get_player_info(player, 4)
        cv2.imwrite('screenshots/player4.png', player)
        if found_me: 
            return
        player = self.board_area[25:third_height - 35, 20:third_width - 20] # Bottom-Right
        found_me = self.get_player_info(player, 5)
        cv2.imwrite('screenshots/player5.png', player)
        if found_me: 
            return
        player = self.board_area[third_height * 2 + 25:height -35, 20:third_width - 20]      # Top-Left
        found_me = self.get_player_info(player, 6)
        cv2.imwrite('screenshots/player6.png', player)
        if not found_me: 
            print("You are not sitten this table")

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

    def screen_shot(self, gray_convert: bool = True):
        # print("take screen shot..")
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshots/screenshot1.png")
        self.screen = np.array(screenshot)
        cv2.imwrite('screenshots/screenshot2.png', self.screen)
        if not gray_convert:
            self.screen = cv2.cvtColor(self.screen, cv2.COLOR_RGB2GRAY)
            cv2.imwrite('screenshots/screenshot3.png', self.screen)

