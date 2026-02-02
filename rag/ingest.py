from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings # Use Ollama here
from langchain_core.documents import Document
import json

def load_and_index():
    with open('knowledge_base/bad_practice.json', 'r') as f:
        data = json.load(f)

    # Using your 'nomic-embed-text' model
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    documents = [
        Document(
            page_content=f"Pattern: {e['code_pattern']}\nRisk: {e['description']}",
            metadata={"id": e['id'], "fix": e['fix']}
        ) for e in data
    ]

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./db_chroma"
    )
    print("Local index created with nomic-embed-text!")

if __name__ == "__main__":
    load_and_index()