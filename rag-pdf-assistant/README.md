
RAG PDF Assistant
A Retrieval-Augmented Generation (RAG) web application that lets users upload PDFs and ask questions about their content. The system uses LangChain 0.3, FAISS, and OpenAI embeddings/LLMs

Features

Retrieval-Augmented Generation (RAG)
- Splits PDFs into semantic chunks
- Embeds text using OpenAIEmbeddings
- Stores vectors in a FAISS index
- Retrieves the most relevant chunks for every question
- Generates answers using ChatGPT (gpt-4o-mini)

PDF Processing
- Upload any PDF into /uploads
- Automatic ingestion pipeline (ingest.py)
- Chunking, text cleaning, embedding generation
- Vector index saved locally for fast querying

Web Interface (Flask)
- Simple and clean UI
- Ask questions directly from the browser
- AI answers with context
- Source snippets included

Technology Used
Component	Technology
Backend	Python, Flask
AI Model	OpenAI GPT-4o-mini
Vector Store	FAISS
Framework	LangChain 0.3
Embeddings	OpenAI Embeddings
PDF Parsing	PyPDF
Environment	dotenv

Project Structure

rag-pdf-assistant/
│
├── app.py                 # Flask app for web UI
├── ingest.py              # PDF ingestion + vector store creation
├── requirements.txt       # Dependencies
├── uploads/               # Put your PDFs here
│     └── <yourfile>.pdf
├── vectorstore/           # Auto-generated FAISS index
│     ├── index.faiss
│     └── index.pkl
└── README.md

Installation
1. Clone the repository
bash
Copy code
git clone https://github.com/<your-username>/<repo-name>.git
cd rag-pdf-assistant
2. Create a virtual environment (recommended)
bash
Copy code
python -m venv venv
venv\Scripts\activate       # Windows
3. Install dependencies
bash
Copy code
pip install -r requirements.txt

Environment Setup
Create a .env file:


OPENAI_API_KEY=your_key_here

Add a PDF
Place at least one PDF inside uploads

bash
uploads/sample.pdf

Build the Vector Store
Run the ingestion script:

bash
python ingest.py

You should see:
nginx

Embedding complete! Vector store saved.

Start the Web App
bash
Copy code
python app.py

Visit in browser:
arduino
Copy code
http://localhost:5000
