from typing import Dict, List

# We don’t blindly query the vector database. We first interpret code signals and then form intent-aware semantic queries
def build_rag_queries(signals: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Converts extracted signals into meaningful RAG queries.
    """
    queries = {
        "security": [],
        "bad_practice": [],
        "performance": []
    }

    # ---- SECURITY ----
    if any("SQL" in s for s in signals["security"]) and any("User input" in s for s in signals["security"]):
        queries["security"].append(
            "SQL injection vulnerability caused by unsanitized user input in backend code"
        )

    if any("HTML injection" in s for s in signals["security"]):
        queries["security"].append(
            "Cross-site scripting vulnerability due to unsafe HTML rendering"
        )

    if any("Hardcoded secret" in s for s in signals["security"]):
        queries["security"].append(
            "Security risks of hardcoded API keys or secrets in source code"
        )

    # ---- BAD PRACTICES ----
    if any("Debug statement" in s for s in signals["bad_practice"]):
        queries["bad_practice"].append(
            "Problems caused by leaving debug or console logs in production code"
        )

    # ---- PERFORMANCE ----
    loop_count = len([s for s in signals["performance"] if "Loop detected" in s])

    if loop_count >= 2:
        queries["performance"].append(
            "Nested loops causing O(n^2) time complexity and performance degradation"
        )
    elif loop_count == 1:
        queries["performance"].append(
            "Loop performance optimization techniques in application code"
        )

    return queries


# -------- QUICK TEST --------
if __name__ == "__main__":
    sample_signals = {
        "security": [
            "Possible SQL query at line 2",
            "User input usage at line 2"
        ],
        "bad_practice": [
            "Debug statement at line 6"
        ],
        "performance": [
            "Loop detected at line 4",
            "Loop detected at line 5"
        ]
    }

    rag_queries = build_rag_queries(sample_signals)

    print("\nGenerated RAG Queries:\n")
    for category, qs in rag_queries.items():
        print(category.upper())
        for q in qs:
            print(" -", q)
