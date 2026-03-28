import streamlit as st
import tempfile
import os

from ingest import load_code_files
from chunker import chunk_code
from retriever import create_vector_store, retrieve_context
from llm_handler import generate_answer

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="Codebase Assistant", layout="wide")
st.title("💻 Codebase AI Assistant")

# -------------------------------
# Upload files
# -------------------------------
uploaded_files = st.file_uploader(
    "Upload code files",
    accept_multiple_files=True,
    type=["py", "java", "cpp", "js"]
)

# -------------------------------
# Build system after upload
# -------------------------------
if uploaded_files:
    if "db" not in st.session_state:

        with st.spinner("Processing files..."):

            # Create temp directory
            temp_dir = tempfile.mkdtemp()

            # Save uploaded files
            for file in uploaded_files:
                file_path = os.path.join(temp_dir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

            # Run pipeline
            files = load_code_files(temp_dir)
            chunks = chunk_code(files)
            db = create_vector_store(chunks)

            # Save in session
            st.session_state.db = db
            st.session_state.ready = True

        st.success("✅ Codebase processed successfully!")

# -------------------------------
# Chat system
# -------------------------------
def get_k_for_query(query):
    query = query.lower()

    if "explain" in query or "overview" in query:
        return 8
    elif "where" in query or "find" in query:
        return 3
    else:
        return 5


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# Chat input
# -------------------------------
if "ready" in st.session_state:
    query = st.chat_input("Ask about your code...")

    if query:
        st.session_state.chat_history.append(("user", query))

        db = st.session_state.db
        k = get_k_for_query(query)

        context, docs = retrieve_context(db, query, k=k)
        answer = generate_answer(context, query)

        st.session_state.chat_history.append(("bot", answer))

# -------------------------------
# Display chat
# -------------------------------
for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant"):
            st.write(message)

# -------------------------------
# Show sources
# -------------------------------
if "ready" in st.session_state and "chat_history" in st.session_state:
    if len(st.session_state.chat_history) > 0:
        st.subheader("📄 Retrieved Code Snippets")

        db = st.session_state.db
        last_query = st.session_state.chat_history[-2][1] if len(st.session_state.chat_history) >= 2 else ""

        if last_query:
            context, docs = retrieve_context(db, last_query, k=5)

            for d in docs:
                st.code(d.page_content, language="python")