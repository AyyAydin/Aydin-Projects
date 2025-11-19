import os
import glob
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def ingest_pdf(pdf_path, store_path="vectorstore"):
    print(f"Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(store_path)

    print("Embedding complete! Vector store saved.")

if __name__ == "__main__":
    pdfs = glob.glob("uploads/*.pdf")
    if not pdfs:
        print("No PDFs found in uploads/")
    else:
        ingest_pdf(pdfs[0])
