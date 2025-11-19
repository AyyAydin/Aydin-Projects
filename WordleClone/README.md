Wordle Clone – Python Tkinter

A fully interactive, GUI-based Wordle clone built in Python using Tkinter.  
The game follows the exact rules of the original Wordle.

Players have 6 attempts to guess the 5-letter secret word.

Green – Correct letter in the correct position  
Yellow – Letter exists in word, wrong position  
Gray – Letter not in the word  

A `words.txt` file stores the word bank; a random 5-letter word is chosen each game.

Tkinter GUI  
No terminal needed — everything runs in a window application.

---
Project Structure

WordleClone/
│── wordle.py
│── words.txt
│── requirements.txt

---

Running the Game

1. Install dependencies
pip install tk

2. Run the game
python wordle.py

---

Technologies Used
- Python  
- Tkinter  
- File I/O  
---
