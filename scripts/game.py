from vision import Vision
import time
class Game():
    def __init__(self) -> None:
        self.delay = 1
        self.hand = []
        self.vns = Vision()

    def run(self) -> None:
        print("running....")
        time.sleep(2)
        while True:

            new_hand = self.vns.cards()
            break
            
if __name__ == "__main__":
    play = Game()
    play.input_username()
    play.run()