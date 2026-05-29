# DocuMind Enterprise

## Overview
Enterprise RAG chatbot for SOP and policy documents.

## Features
- PDF Upload
- Semantic Search
- RAG-based QA
- Pinecone Vector DB
- Groq LLM
- Source Citations

## Tech Stack
- FastAPI
- LangChain
- Pinecone
- HuggingFace
- Groq
- HTML/CSS/JS

## Architecture
PDF → Chunking → Embeddings → Pinecone → Retriever → Groq → Answer

## Run Backend
python -m uvicorn backend.app:app --reload

## Run Frontend
cd frontend
python -m http.server 5500