ChatGPT Study Buddy – Flask + SQLite + OpenAI

A full web application that generates summaries, quizzes, and study helpers from user-provided notes.  
Built with Flask, beautifully styled, includes Markdown rendering, and keeps a searchable history of past study sessions.

---

Features

AI-Generated Summaries  
Paste your notes → get a clean, readable explanation.

Auto-Generated Multiple-Choice Quiz  
The app produces a 5-question MCQ quiz using strict formatting:
Question?
a) option
b) option
c) option
d) option

Clean Modern UI  
Includes:
- Card UI
- Soft colors
- Spacing optimized for readability

History Viewer  
All previous summaries and quizzes are saved in an SQLite database.

Clear History Button  
Wipes all stored study sessions.

Markdown Support  
AI output is formatted using Markdown → rendered as clean HTML.

---

Project Structure

ChatGPT_StudyBuddy/
│── app.py
│── requirements.txt
│── .env (not included in GitHub)
│── database.db (auto-created)
│
├── templates/
│ ├── index.html
│ ├── result.html
│ └── history.html
│
└── static/
└── style.css

---

Environment Variables (`.env`)

Create a `.env` file in the project root:

OPENAI_API_KEY=your_key_here

⚠️ **Do NOT upload `.env` to GitHub.**  
Make sure `.gitignore` contains:
.env

---

Running the Application

1. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Run the Flask app
python app.py

4. Open in browser
http://127.0.0.1:5000

---

Technologies Used
- Flask  
- Python  
- SQLite  
- OpenAI API  
- Markdown  
- HTML/CSS  

---
