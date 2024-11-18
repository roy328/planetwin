from vision import Vision
import time
import tkinter as tk
class Game():
    def __init__(self) -> None:
        self.delay = 1
        self.hand = []
        self.username = ''
        self.vns = None
        self.entry = None

    def accept_input(self) -> None:
        self.username = self.entry.get()
        self.vns = Vision(self.username)
        root.destroy()

    def input_username(self) -> None:
        global root
        root = tk.Tk()
        root.title("Input Prompt")

        # Create a label
        label = tk.Label(root, text="Enter your username")
        label.pack(pady=10)

        # Create an entry widget for user input
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        # Create a button to accept the input
        button = tk.Button(root, text="Submit", command=self.accept_input)
        button.pack(pady=20)

        # Start the main loop
        root.mainloop()

    def run(self) -> None:
        print("running....", self.username)
        while True:
            new_hand = self.vns.cards()
            time.sleep(self.delay)
            break
            
if __name__ == "__main__":
    play = Game()
    play.input_username()
    play.run()