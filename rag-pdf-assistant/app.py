from flask import Flask, request, render_template_string
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import PromptTemplate

load_dotenv()

app = Flask(__name__)

# ---------------------------
# Load VectorStore (FAISS)
# ---------------------------
embeddings = OpenAIEmbeddings()

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ---------------------------
# LLM Configuration
# ---------------------------
llm = ChatOpenAI(model="gpt-4o-mini")

prompt = PromptTemplate.from_template("""
You are an AI assistant. Use ONLY the provided context to answer.

Question:
{question}

Context:
{context}

If the answer is not in the context, say: "I cannot answer based on the document."

Answer:
""")

# ---------------------------
# NEW RAG PIPELINE (LangChain 0.3)
# ---------------------------
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

rag_chain = (
    RunnableParallel(
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
    )
    | prompt
    | llm
)

# ---------------------------
# HTML Template
# ---------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI PDF Assistant</title>
<style>
body { font-family: Arial; margin: 40px; background: #f9f9f9; }
textarea, input { width: 100%; padding: 12px; font-size: 16px; }
button { padding: 14px; font-size: 18px; margin-top: 10px; width: 100%; cursor: pointer; }
.result { margin-top: 20px; background: #fff; padding: 20px; border-radius: 8px; }
pre { white-space: pre-wrap; }
</style>
</head>
<body>

<h1>AI PDF Assistant</h1>
<p>Ask any question about the uploaded PDF.</p>

<form method="POST">
<textarea name="question" rows="4" placeholder="Ask a question...">{{ question }}</textarea>
<button type="submit">Ask</button>
</form>

{% if answer %}
<div class="result">
<h3>Answer:</h3>
<pre>{{ answer }}</pre>
</div>
{% endif %}

</body>
</html>
"""

# ---------------------------
# Flask Route
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    answer = None

    if request.method == "POST":
        question = request.form["question"]
        result = rag_chain.invoke(question)
        answer = result.content  # ChatOpenAI output

    return render_template_string(HTML, question=question, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)
