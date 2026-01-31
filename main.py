import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from load_code.code_loader import load_code
from vectorstore.db import load_knowledge_base
from agents.classifier_agent import classify_chunk
from agents.security_agent import security_analysis
from agents.bad_practice_agent import bad_practice_analysis
from agents.performance_agent import performance_analysis

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

retriever = load_knowledge_base()

# Sample code input
with open("sample_code.js", "r") as f:
    code = f.read()

chunks = load_code(code)

results = []

for chunk in chunks:
    categories = classify_chunk(chunk)

    if "security" in categories:
        results.append(
            security_analysis(chunk, retriever, llm)
        )

    if "bad_practice" in categories:
        results.append(
            bad_practice_analysis(chunk, retriever, llm)
        )

    if "performance" in categories:
        results.append(
            performance_analysis(chunk, retriever, llm)
        )

print("\n==== ANALYSIS REPORT ====\n")
for r in results:
    print(r)
    print("-" * 80)