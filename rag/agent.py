from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import PromptTemplate 


load_dotenv()

# OpenRouter Connection
# llm = ChatOpenAI(
#     model="arcee-ai/trinity-large-preview:free", 
#     openai_api_base="https://openrouter.ai/api/v1",
#     openai_api_key=os.getenv("OPENROUTER_API_KEY"), # Fixed: Use your OpenRouter key
# )

llm = ChatOllama(
    model="llama3.2:1b", 
    temperature=0,
    # This ensures it doesn't try to use 100% of your CPU
    num_thread=4 
)

class AgentState(TypedDict):
    code: str
    context: str
    report: str
    metrics: Dict[str, str]
    review_feedback: str 
    iterations: int

def retrieval_node(state: AgentState):
    print("--- STEP: RETRIEVING PATTERNS ---")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory="./db_chroma", embedding_function=embeddings)
    
    docs = db.similarity_search(state['code'], k=2)
    
    # Explicitly pull ID and title into the context string
    context_list = []
    for d in docs:
        content = f"RULE_ID: {d.metadata.get('id', 'N/A')}\nCONTENT: {d.page_content}"
        context_list.append(content)
        
    context = "\n---\n".join(context_list)
    return {"context": context}

def analysis_node(state: AgentState):
    print("--- STEP: ANALYZING CODE ---")

    prompt = PromptTemplate.from_template("""
SYSTEM: You are a Security Auditor. You MUST identify violations using the provided PATTERNS.
Each pattern has a 'RULE_ID'. You MUST include this ID in your report.

PATTERNS:
{context}

USER CODE:
{code}

REPORT FORMAT (Strictly follow this):
- ID: [Insert RULE_ID here]
- Vulnerability: [Title]
- Recommendation: [Fix from pattern]
""")
    # Using the pipe (|) operator is the "Pro" way in 2026
    chain = prompt | llm
    response = chain.invoke({"context": state['context'], "code": state['code']})
    
    return {"report": response.content}

# def reviewer_node(state: AgentState):
#     print("--- STEP: REVIEWING REPORT ---")
#     report = state.get("report", "")
    
#     # Logic: If the AI repeats itself or doesn't provide a clear ID, reject it.
#     if report.count("SYSTEM:") > 1 or "ID:" not in report:
#         return {
#             "review_feedback": "REJECTED: Your report is repetitive or missing the ID. Please provide ONLY the ID, Vulnerability, and Recommendation.",
#             "iterations": state.get("iterations", 0) + 1
#         }
    
#     return {"review_feedback": "APPROVED"}

# def should_continue(state: AgentState):
#     # Stop if approved OR if we've tried 3 times (to save your CPU)
#     if state["review_feedback"] == "APPROVED" or state.get("iterations", 0) >= 3:
#         return END
#     return "analyze"


#### Scoring node for visalization 
def scoring_node(state: AgentState):
    print("--- STEP: SCORING PERFORMANCE & SECURITY ---")
    
    prompt = PromptTemplate.from_template("""
    SYSTEM: Rate the following code on three criteria: 
    1. Performance
    2. Bad Practices
    3. Security
    
    Use a scale of 1-10 (where 10 is best/safest).
    
    CODE:
    {code}
    
    VULNERABILITIES FOUND:
    {report}
    
    FORMAT:
    Performance: [score]/10
    Bad Practice: [score]/10
    Security: [score]/10
    """)
    
    chain = prompt | llm
    response = chain.invoke({"code": state['code'], "report": state['report']})
    
    # Simple logic to "save" it into our state
    return {"metrics": {"rating_details": response.content}}


# 3. Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieval_node)
workflow.add_node("analyze", analysis_node)
workflow.add_node("score", scoring_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "analyze")
workflow.add_edge("analyze", "score")  
workflow.add_edge("score", END)

app = workflow.compile()