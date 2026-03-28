import sys
import os
from dotenv import load_dotenv

# Load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Fix imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil

from rag import load_codebase, ask_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_code"

@app.post("/upload")
async def upload(files: list[UploadFile]):
    print("\n=== UPLOAD REQUEST ===")

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Clear old files
    for f in os.listdir(UPLOAD_DIR):
        os.remove(os.path.join(UPLOAD_DIR, f))

    for file in files:
        print("Received:", file.filename)
        path = os.path.join(UPLOAD_DIR, file.filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    load_codebase(UPLOAD_DIR)

    return {"message": "Codebase loaded successfully"}

@app.post("/ask")
async def ask(query: str = Form(...)):
    print("Query:", query)
    return ask_question(query)