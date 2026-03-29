# KY2fileReview

KY2filefrnd is an AI-powered codebase assistant built using Retrieval-Augmented Generation (RAG). It allows users to upload one or more code files and ask questions about them. The system retrieves relevant parts of the code and generates accurate, context-aware answers using a Large Language Model (LLM), making it easier to understand and explore codebases.

---

## Tech Stack

This project is built using a full-stack architecture. The backend is developed using FastAPI, which handles API requests and integrates the RAG pipeline. LangChain is used for orchestrating the workflow, while FAISS is used as the vector database for efficient similarity search. Sentence Transformers are used to generate embeddings from code. The LLM is powered by Groq for fast inference. The frontend is built using HTML, CSS, and JavaScript.

---

## Setup

First, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/YOUR_USERNAME/RAG-Based-File-Assistant.git
cd RAG-Based-File-Assistant
```

## Create the virtual environment and activate it
```
python -m venv venv
venv\Scripts\activate
```

## Install the required dependencies
```
pip install -r requirements.txt
```

## Create a .env file in the root directory and add your API key
GROQ_API_KEY=your_api_key_here

## Start the Backend server
```
cd backend
python -m uvicorn main:app
```


## Start the Frontend
```
cd frontend
python -m http.server 5500
```
Open your browser and go to: http://127.0.0.1:5500



# Usage

After running both backend and frontend, upload your code files through the UI.
You can then ask questions such as "Explain this file" or "What does this function do?".
The system retrieves relevant code and generates answers based on it.
