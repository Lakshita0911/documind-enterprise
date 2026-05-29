
import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain_pinecone import PineconeVectorStore


# Load Environment Variables

load_dotenv(dotenv_path=".env")
print(os.getenv("PINECONE_API_KEY"))

# Ingest PDF

def ingest_pdf(file_path, namespace=""):

    # Load PDF

    loader = PyPDFLoader(file_path)

    documents = list(loader.lazy_load())

    # Split into chunks

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    # Embedding Model

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Store in Pinecone

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=os.getenv(
            "PINECONE_INDEX_NAME"
        ),
        namespace=namespace
    )
    print("Chunks Created:", len(chunks))
    return len(chunks)

