# from langchain.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

PERSIST_DIR = "vector_store"

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_db = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embedding_model
)

query = "SQL query using user input without validation"

results = vector_db.similarity_search(query, k=3)

print("\n Retrieved Knowledge:\n")
for r in results:
    print("----")
    print(r.page_content)
    print("METADATA:", r.metadata)


