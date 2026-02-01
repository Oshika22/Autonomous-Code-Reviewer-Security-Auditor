# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain.chat_models import ChatOpenAI
from rag.build_rag_queries import build_rag_queries

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

VECTOR_STORE_DIR = "vector_store"

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)

llm = ChatOllama(
    model="deepseek-coder:6.7b",
    temperature=0
)

vector_db = Chroma(
    persist_directory=VECTOR_STORE_DIR,
    embedding_function=embedding_model
)


def performance_agent(signals: dict, top_k: int = 3):
    """
    Detect and explain performance issues in code.
    """
    queries = build_rag_queries(signals)

    results_summary = []

    for query in queries["performance"]:
        docs = vector_db.similarity_search(query, k=top_k)

        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = f"""
You are a performance optimization expert reviewing code.

Query: {query}

Knowledge Context:
{context}

Explain clearly:
1. What is the performance issue?
2. Why does it matter?
3. How to improve/optimize?
Answer in bullet points.
"""

        response = llm.invoke(prompt)
        results_summary.append({
            "query": query,
            "explanation": response.content
        })

    return results_summary


# # -------- TEST --------
# if __name__ == "__main__":
#     sample_signals = {
#         "security": [],
#         "bad_practice": [],
#         "performance": [
#             "Loop detected at line 4",
#             "Loop detected at line 5"
#         ]
#     }

#     output = performance_agent(sample_signals)

#     for r in output:
#         print("\n⚡ Performance Reasoning for:", r["query"])
#         print(r["explanation"])
