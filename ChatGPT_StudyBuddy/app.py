from flask import Flask, render_template, request
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
import os
import markdown

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------
# Database Setup
# ---------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_session(prompt, response):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO sessions (prompt, response) VALUES (?, ?)",
              (prompt, response))
    conn.commit()
    conn.close()


def fetch_history():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT prompt, response FROM sessions ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return rows


# ---------------------------
# Routes
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]

        prompt = f"""
You are a study assistant.

1. First, summarize the following notes clearly and simply.
2. Then generate a **5-question multiple-choice quiz**.
3. Format the quiz EXACTLY like this:

1. Question text?
   a) option 1
   b) option 2
   c) option 3
   d) option 4

4. Each answer choice MUST be on its own new line.
5. Indent the answer choices under the question.

Here are the notes to summarize and quiz:
{text}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )

            result = response.choices[0].message.content

        except Exception as e:
            result = f"Error: {e}"

        save_session(text, result)

        html_summary = markdown.markdown(result)

        return render_template("result.html", text=text, result=html_summary)

    return render_template("index.html")


@app.route("/history")
def history():
    rows = fetch_history()
    processed = [(p, markdown.markdown(r)) for (p, r) in rows]
    return render_template("history.html", history=processed)


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
