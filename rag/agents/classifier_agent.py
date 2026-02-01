from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0)

def classify_chunk(code_chunk: str):
    prompt = f"""
You are a senior software auditor.

Analyze the code below and classify issues as:
- security
- bad_practice
- performance
- none

Code:
{code_chunk}

Return only a Python list.
"""

    response = llm.predict(prompt)
    return eval(response)
