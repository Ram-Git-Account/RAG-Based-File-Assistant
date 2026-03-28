from dotenv import load_dotenv
load_dotenv()

from ingest import load_code_files
from chunker import chunk_code
from retriever import create_vector_store, retrieve_context
from llm_handler import generate_answer


# 🔥 Query-aware retrieval
def get_k_for_query(query):
    query = query.lower()

    if "explain" in query or "overview" in query:
        return 8
    elif "where" in query or "find" in query:
        return 3
    else:
        return 5


def main():
    print("Loading codebase...")
    files = load_code_files("data/")
    print("Files loaded:", len(files))

    print("Chunking...")
    chunks = chunk_code(files)
    print("Chunks ready:", len(chunks))

    print("Creating vector DB...")
    db = create_vector_store(chunks)
    print("Vector DB created successfully!")

    while True:
        query = input("\nAsk: ")

        k = get_k_for_query(query)

        context, docs = retrieve_context(db, query, k=k)

        answer = generate_answer(context, query)

        print("\n==============================")
        print("Answer:\n", answer)
        print("==============================")

        print("\nSources:")
        for d in docs:
            print("-", d.metadata["source"])


if __name__ == "__main__":
    main()