from vision import Vision
import time
import tkinter as tk
class Game():
    def __init__(self) -> None:
        self.delay = 1
        self.hand = []
        self.username = ''
        self.vns = Vision()
        self.entry = None

    def accept_input(self):
        self.username = self.entry.get()
        root.destroy()

    def input_username(self):
        global root
        root = tk.Tk()
        root.title("Input Prompt")

        # Create a label
        label = tk.Label(root, text="Enter a value:")
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
        time.sleep(2)
        while True:

            new_hand = self.vns.cards()
            break
            
if __name__ == "__main__":
    play = Game()
    play.input_username()
    play.run()