# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain.chat_models import ChatOpenAI
from rag.build_rag_queries import build_rag_queries

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

# -------- CONFIG --------
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

# -------- AGENT FUNCTION --------
def security_agent(signals: dict, top_k: int = 3):
    """
    Given extracted signals, generate human-readable security explanations.
    """
    # Step 1: Convert signals → RAG queries
    queries = build_rag_queries(signals)

    results_summary = []

    for query in queries["security"]:
        # Step 2: Retrieve relevant KB chunks
        docs = vector_db.similarity_search(query, k=top_k)

        # Step 3: Feed to LLM for reasoning
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = f"""
You are a security expert reviewing the following code signals:

Query: {query}

Knowledge Context:
{context}

Explain clearly:
1. What is the security issue?
2. Why is it risky?
3. How to fix it?
4. Severity
Answer in bullet points.
"""

        response = llm.invoke(prompt)
        results_summary.append({
            "query": query,
            "explanation": response.content
        })

    return results_summary


# # -------- QUICK TEST --------
# if __name__ == "__main__":
#     # Example signals
#     sample_signals = {
#         "security": [
#             "Possible SQL query at line 2",
#             "User input usage at line 2"
#         ],
#         "bad_practice": [],
#         "performance": []
#     }

#     output = security_agent(sample_signals)

#     for r in output:
#         print("\nSecurity Reasoning for:", r["query"])
#         print(r["explanation"])