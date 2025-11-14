from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
import os
import markdown
from gtts import gTTS
from PyPDF2 import PdfReader
import time

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_NAME = "database.db"
AUDIO_DIR = os.path.join("static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)


# ---------------------------
# Database Setup
# ---------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Ensure table exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            response TEXT,
            topic TEXT
        )
    """)
    # Ensure topic column exists (for older DBs)
    c.execute("PRAGMA table_info(sessions)")
    cols = [row[1] for row in c.fetchall()]
    if "topic" not in cols:
        c.execute("ALTER TABLE sessions ADD COLUMN topic TEXT")
    conn.commit()
    conn.close()


def save_session(prompt, response, topic):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO sessions (prompt, response, topic) VALUES (?, ?, ?)",
        (prompt, response, topic),
    )
    conn.commit()
    conn.close()


def clear_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM sessions")
    conn.commit()
    conn.close()


# ---------------------------
# Helpers
# ---------------------------
def extract_topic_and_body(result_text: str):
    """
    Expecting the AI to return:
    Line 1: Topic: Something
    Blank line
    Then summary + quiz in markdown.
    """
    lines = result_text.splitlines()
    topic = ""
    body_text = result_text

    if lines and lines[0].lower().startswith("topic:"):
        topic = lines[0][6:].strip()
        # Skip first line and possible blank second line
        if len(lines) >= 2 and lines[1].strip() == "":
            body_text = "\n".join(lines[2:])
        else:
            body_text = "\n".join(lines[1:])

    return topic, body_text


def generate_tts_audio(text: str) -> str | None:
    """
    Generate an mp3 file from text and return its URL path,
    or None if something fails.
    """
    try:
        if not text.strip():
            return None
        filename = f"summary_{int(time.time())}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        tts = gTTS(text, lang="en")
        tts.save(filepath)
        return f"/static/audio/{filename}"
    except Exception:
        return None


# ---------------------------
# Routes
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 1) Get raw text from textarea
        text = request.form.get("text", "").strip()

        # 2) If a file is uploaded, extract text (PDF support)
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename.lower()
            if filename.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                pdf_text_parts = []
                for page in reader.pages:
                    page_txt = page.extract_text() or ""
                    pdf_text_parts.append(page_txt)
                pdf_text = "\n\n".join(pdf_text_parts).strip()
                if pdf_text:
                    if text:
                        text = text + "\n\n" + pdf_text
                    else:
                        text = pdf_text

        if not text:
            # Nothing to summarize
            return render_template("index.html", error="Please paste notes or upload a PDF.")

        # 3) Build AI prompt with topic + summary + quiz instructions
        prompt = f"""
You are a helpful study assistant.

1. First line of your response MUST be: "Topic: <short topic name>".
2. Then a blank line.
3. Then provide a clear, structured summary in markdown.
4. Then generate a 5-question multiple-choice quiz using this exact format:

1. Question text?
   a) option 1
   b) option 2
   c) option 3
   d) option 4

5. Each answer choice MUST be on its own line, indented under the question.

Here are the notes to summarize and quiz:
{text}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            full_result = response.choices[0].message.content
        except Exception as e:
            return render_template("index.html", error=f"API Error: {e}")

        # 4) Extract topic + markdown body (summary + quiz)
        topic, body_text = extract_topic_and_body(full_result)

        # 5) Save entire raw result (so we can re-render later)
        save_session(text, full_result, topic)

        # 6) Convert body markdown to HTML
        html_summary = markdown.markdown(body_text)

        # 7) Generate TTS audio for the summary+quiz
        audio_url = generate_tts_audio(body_text)

        return render_template(
            "result.html",
            text=text,
            topic=topic,
            result=html_summary,
            audio_url=audio_url,
        )

    # GET
    return render_template("index.html")


@app.route("/history")
def history():
    query = request.args.get("q", "").strip()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if query:
        like = f"%{query}%"
        c.execute(
            """
            SELECT prompt, response, topic 
            FROM sessions
            WHERE prompt LIKE ? OR IFNULL(topic, '') LIKE ?
            ORDER BY id DESC
            LIMIT 50
            """,
            (like, like),
        )
    else:
        c.execute(
            "SELECT prompt, response, topic FROM sessions ORDER BY id DESC LIMIT 50"
        )
    rows = c.fetchall()
    conn.close()

    history_items = []
    for prompt_text, response_text, topic in rows:
        t, body = extract_topic_and_body(response_text or "")
        # Prefer stored topic, fall back to parsed
        topic_final = topic if topic else t
        html_body = markdown.markdown(body)
        history_items.append(
            {
                "prompt": prompt_text,
                "topic": topic_final,
                "html": html_body,
            }
        )

    return render_template("history.html", history=history_items, query=query)


@app.route("/clear_history", methods=["POST"])
def clear_history_route():
    clear_history()
    return redirect(url_for("history"))


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
