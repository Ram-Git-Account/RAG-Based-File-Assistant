from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_store(chunks):
    texts = [c["content"] for c in chunks]
    metadata = [{"source": c["path"]} for c in chunks]

    if len(texts) == 0:
        raise Exception("❌ No text data to embed")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = FAISS.from_texts(texts, embeddings, metadatas=metadata)

    return db


def retrieve_context(db, query, k=5):
    docs = db.similarity_search(query, k=k)

    context = "\n\n".join([
        f"File: {d.metadata['source']}\n{d.page_content}"
        for d in docs
    ])

    return context, docs