import tkinter as tk
from tkinter import messagebox
import random

class WordleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Clone – Aydin Chowdhury")
        self.master.geometry("400x550")
        self.master.resizable(False, False)

        self.word_list = self.load_words()
        self.secret_word = random.choice(self.word_list).upper()
        self.current_row = 0
        self.guesses = []

        self.create_board()
        self.create_input_box()

    def load_words(self):
        try:
            with open("words.txt", "r") as f:
                return [w.strip() for w in f.readlines() if len(w.strip()) == 5]
        except FileNotFoundError:
            return ["APPLE", "SMILE", "RIGHT"]

    def create_board(self):
        self.cells = []
        for r in range(6):
            row = []
            for c in range(5):
                cell = tk.Label(self.master, text="", width=5, height=2,
                                font=("Helvetica", 18), borderwidth=2, relief="solid")
                cell.grid(row=r, column=c, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)

    def create_input_box(self):
        self.entry = tk.Entry(self.master, font=("Helvetica", 16))
        self.entry.grid(row=7, column=0, columnspan=3, pady=20, padx=10)

        submit_btn = tk.Button(self.master, text="Submit Guess",
                               font=("Helvetica", 14), command=self.submit_guess)
        submit_btn.grid(row=7, column=3, columnspan=2)

    def submit_guess(self):
        guess = self.entry.get().upper()
        self.entry.delete(0, tk.END)

        if len(guess) != 5:
            messagebox.showinfo("Error", "Guess must be 5 letters")
            return

        self.guesses.append(guess)
        self.update_board(guess)

        if guess == self.secret_word:
            messagebox.showinfo("You Win!", "Correct!")
            self.master.quit()
        elif self.current_row == 6:
            messagebox.showinfo("Game Over", f"The word was: {self.secret_word}")
            self.master.quit()

    def update_board(self, guess):
        secret = list(self.secret_word)
        guess_letters = list(guess)

        # Track colors
        colors = ["gray"] * 5

        # Step 1: Green pass
        for i in range(5):
            if guess_letters[i] == secret[i]:
                colors[i] = "green"
                secret[i] = None  # remove used letter

        # Step 2: Yellow pass
        for i in range(5):
            if colors[i] == "gray" and guess_letters[i] in secret:
                colors[i] = "yellow"
                secret[secret.index(guess_letters[i])] = None  # consume one

        # Step 3: Paint board
        for i in range(5):
            cell = self.cells[self.current_row][i]
            cell.config(text=guess_letters[i])

            if colors[i] == "green":
                cell.config(bg="green", fg="white")
            elif colors[i] == "yellow":
                cell.config(bg="yellow", fg="black")
            else:
                cell.config(bg="gray", fg="white")

        self.current_row += 1


if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()
