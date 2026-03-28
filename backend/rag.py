import sys
import os

# Fix imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingest import load_code_files
from chunker import chunk_code
from retriever import create_vector_store, retrieve_context
from llm_handler import generate_answer

db = None

def load_codebase(path):
    global db

    print("\n=== LOADING CODEBASE ===")

    files = load_code_files(path)
    print("Files loaded:", len(files))
    print("Files:", files)

    chunks = chunk_code(files)
    print("Chunks created:", len(chunks))
    print("Chunks:", chunks)

    if len(chunks) == 0:
        raise Exception("❌ No chunks created — check file reading")

    db = create_vector_store(chunks)

    print("Vector DB ready\n")


def ask_question(query):
    global db

    if db is None:
        return {"answer": "❌ Codebase not loaded. Upload first.", "sources": []}

    context, docs = retrieve_context(db, query, k=5)

    answer = generate_answer(context, query)

    sources = list(set([d.metadata["source"] for d in docs]))

    return {
        "answer": answer,
        "sources": sources
    }