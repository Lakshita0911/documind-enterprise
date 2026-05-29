
import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_pinecone import (
    PineconeVectorStore
)


# Load Environment Variables

load_dotenv(dotenv_path=".env")


# Ask Question Function

def ask_question(query, namespace=""):

    # Embedding Model

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Pinecone Vector Store

    vectorstore = PineconeVectorStore(
        index_name=os.getenv(
            "PINECONE_INDEX_NAME"
        ),
        embedding=embeddings,
        namespace=namespace
    )

    # Retriever

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    # Retrieve Documents

    docs = retriever.invoke(query)
    print("Docs")
    # No documents found

    if not docs:

        return {
            "answer": "I don't know.",
            "sources": []
        }

    # Build Context

    context = ""

    sources = []

    for doc in docs:

        context += (
            doc.page_content + "\n"
        )

        sources.append({

            "page":
                doc.metadata.get(
                    "page"
                ),

            "source":
                doc.metadata.get(
                    "source"
                )

        })

    # LLM

# LLM

    llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
     )
    # Prompt

    prompt = f"""
      You are a helpful enterprise AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
reply with:
"I don't know."

Context:
{context}

Question:
{query}
"""

    # Generate Response
   
    
    try:
     response = llm.invoke(prompt)

     return {
        "answer": response.content,
        "sources": sources
     }

    except Exception as e:
     return {
        "answer": f"Error: {str(e)}",
        "sources": []
    }

