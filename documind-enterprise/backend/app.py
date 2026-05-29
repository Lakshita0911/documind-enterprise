
import os
import uuid

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from ingest import ingest_pdf
from rag_chain import ask_question


app = FastAPI(
    title="DocuMind Enterprise API"
)

CURRENT_NAMESPACE = ""


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home Route

@app.get("/")
def home():

    return {
        "message": "DocuMind Enterprise API Running"
    }


# Upload PDF

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_location = f"temp_{file.filename}"

    try:

        # Save uploaded file

        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Process PDF

        namespace = uuid.uuid4().hex
        chunks = ingest_pdf(file_location, namespace=namespace)
        global CURRENT_NAMESPACE
        CURRENT_NAMESPACE = namespace

        return {
            "message": "Upload successful",
            "chunks": chunks,
            "namespace": namespace
        }

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        # Delete temp file

        if os.path.exists(file_location):
            os.remove(file_location)


# Ask Question

@app.get("/ask")
def ask(query: str):

    result = ask_question(query, namespace=CURRENT_NAMESPACE)

    return result

