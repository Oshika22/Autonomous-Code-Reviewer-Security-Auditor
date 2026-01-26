import json
import os
# from langchain.schema import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from dotenv import load_dotenv
load_dotenv()

# -------- CONFIG --------
KNOWLEDGE_DIR = "knowledge_base"
PERSIST_DIR = "vector_store"

# Use your API key via env variable
# export OPENAI_API_KEY="your_key_here"


embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)


documents = []

# -------- LOAD JSON FILES --------
for file_name in os.listdir(KNOWLEDGE_DIR):
    if file_name.endswith(".json"):
        file_path = os.path.join(KNOWLEDGE_DIR, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            for entry in data:
                content = f"""
Title: {entry.get('title')}
Description: {entry.get('description')}
Risk: {entry.get('risk')}
Explanation: {entry.get('explanation')}
Fix: {entry.get('fix')}
Code Pattern: {entry.get('code_pattern')}
"""

                metadata = {
                    "id": entry.get("id"),
                    "category": entry.get("category"),
                    "severity": entry.get("severity"),
                    "language": entry.get("language"),
                    "framework": entry.get("framework"),
                    "tags": ", ".join(entry.get("tags", []))
                }

                documents.append(
                    Document(page_content=content, metadata=metadata)
                )

print(f"Loaded {len(documents)} knowledge chunks")

# -------- CREATE VECTOR DB --------
vector_db = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory=PERSIST_DIR
)

vector_db.persist()
print("Vector database created and persisted")