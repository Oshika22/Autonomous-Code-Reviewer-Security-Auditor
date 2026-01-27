import re
from typing import Dict, List

# It’s lightweight signal extraction that enables LLM-based semantic security reasoning.

# -------- BASIC SIGNAL PATTERNS --------

PATTERNS = {
    "sql_query": r"(SELECT|INSERT|UPDATE|DELETE)\s+.*",
    "user_input": r"(req\.body|req\.query|req\.params|userInput)",
    "html_injection": r"(innerHTML|dangerouslySetInnerHTML)",
    "loop": r"(for\s*\(|while\s*\()",
    "hardcoded_secret": r"(api_key|apikey|secret|password)\s*=\s*[\"'].*[\"']"
}


def extract_signals(code: str) -> Dict[str, List[str]]:
    """
    Extracts security, quality, and performance signals from code.
    """
    signals = {
        "security": [],
        "bad_practice": [],
        "performance": []
    }

    lines = code.split("\n")

    for i, line in enumerate(lines):
        line_lower = line.lower()

        # ---- SECURITY SIGNALS ----
        if re.search(PATTERNS["sql_query"], line, re.IGNORECASE):
            signals["security"].append(
                f"Possible SQL query at line {i+1}: {line.strip()}"
            )

        if re.search(PATTERNS["user_input"], line):
            signals["security"].append(
                f"User input usage at line {i+1}: {line.strip()}"
            )

        if re.search(PATTERNS["html_injection"], line):
            signals["security"].append(
                f"HTML injection risk at line {i+1}: {line.strip()}"
            )

        # ---- BAD PRACTICE SIGNALS ----
        if "console.log" in line_lower:
            signals["bad_practice"].append(
                f"Debug statement at line {i+1}"
            )

        # ---- PERFORMANCE SIGNALS ----
        if re.search(PATTERNS["loop"], line):
            signals["performance"].append(
                f"Loop detected at line {i+1}: {line.strip()}"
            )

        if re.search(PATTERNS["hardcoded_secret"], line_lower):
            signals["security"].append(
                f"Hardcoded secret at line {i+1}: {line.strip()}"
            )

    return signals


# -------- QUICK TEST --------
if __name__ == "__main__":
    sample_code = """
    const query = "SELECT * FROM users WHERE id = " + req.query.id;
    element.innerHTML = userInput;
    for(let i=0;i<n;i++){
        for(let j=0;j<n;j++){
            console.log(i,j);
        }
    }
    """

    extracted = extract_signals(sample_code)

    print("\nExtracted Signals:\n")
    for category, items in extracted.items():
        print(f"{category.upper()}:")
        for item in items:
            print(" -", item)


