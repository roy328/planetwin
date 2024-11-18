import pyautogui
import cv2
import numpy as np
import pytesseract
from config import (BOARD_LOWER_COLOR, BOARD_HIGHER_COLOR)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
class Vision():
    def __init__(self, username):
        self.threshold = 0.65
        self.username = username
        self.screen = None
        self.board_area = None
        self.players = []
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
        self.crop_board_area()
        self.read_all_player()
        self.get_player_info()

    def extract_text_from_image(self, image: np.ndarray) -> str:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_image)    
        return text.strip()

    def filter_extracted_text(self, extracted_text: str,  currency = "€") -> list:
        # Split the text into lines or words based on spaces/newlines
        lines = extracted_text.splitlines()
        filtered_texts = [line for line in lines if "nino922" in line]
        # print("filtered text", filtered_texts)
        return filtered_texts
    
    def find_longest_string(self, extracted_text: str) -> str:
        longest_string = ""
    
        # Split the text into lines and check each line
        for line in extracted_text.splitlines():
            # Split the line into substrings by space and find the longest one
            substrings = line.split()
            if substrings:  # Check if there are any substrings
                current_longest = max(substrings, key=len)
                # Update longest_string if the current is longer
                if len(current_longest) > len(longest_string):
                    longest_string = current_longest

        return longest_string

    def get_player_info(self):
        for i, quad in enumerate(self.players):
            text = self.extract_text_from_image(quad)
            print(f"Text from Quadrant {i + 1}\n")
            filtered_text = self.filter_extracted_text(text)
            if not text or text == "VUOTO":
                # empty_array.append(f"Quadrant {i + 1}: Text is empty or 'VUOTO'")
                print(f"Appended to empty_array: Quadrant {i + 1} is empty or 'VUOTO'.")
                continue

            if filtered_text:
                print(f"Filtered Text from Quadrant {i + 1} containing {self.username} and '$':")
                for line in filtered_text:
                    print(line)
            else:
                print(f"No matches found in Quadrant {i + 1}.")

            longest_string = self.find_longest_string(text)
            if longest_string:
                print(f"Longest String from Quadrant {i + 1}: {longest_string}")

    def read_all_player(self) -> None:
        height, width = self.board_area.shape[:2]
        
        # Calculate the mid points
        third_height = height // 3
        third_width = width // 3

        # Split the image into four quadrants
        self.player1 = self.board_area[third_height * 2:height, third_width:third_width * 2]  # Top-Right
        self.players.append(self.player1)
        cv2.imwrite('screenshots/player1.png', self.player1)
        self.player2 = self.board_area[third_height * 2:height, third_width * 2:width]  # Top-Right
        self.players.append(self.player2)
        cv2.imwrite('screenshots/player2.png', self.player2)
        self.player3 = self.board_area[0:third_height, third_width * 2:width] # Bottom-Left
        self.players.append(self.player3)
        cv2.imwrite('screenshots/player3.png', self.player3)
        self.player4 = self.board_area[0:third_height, third_width:third_width * 2] # Bottom-Right
        self.players.append(self.player4)
        cv2.imwrite('screenshots/player4.png', self.player4)
        self.player5 = self.board_area[0:third_height, 0:third_width] # Bottom-Right
        self.players.append(self.player5)
        cv2.imwrite('screenshots/player5.png', self.player5)
        self.player6 = self.board_area[third_height * 2:height, 0:third_width]      # Top-Left
        self.players.append(self.player6)
        cv2.imwrite('screenshots/player6.png', self.player6)

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
        print("take screen shot..")
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshots/screenshot1.png")
        self.screen = np.array(screenshot)
        cv2.imwrite('screenshots/screenshot2.png', self.screen)
        if not gray_convert:
            self.screen = cv2.cvtColor(self.screen, cv2.COLOR_RGB2GRAY)
            cv2.imwrite('screenshots/screenshot3.png', self.screen)


