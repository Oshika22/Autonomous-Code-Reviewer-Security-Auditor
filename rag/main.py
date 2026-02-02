import os
from agent import app

def read_file_content(file_path):
    """Safely reads the content of a local file."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    print("\nFILE-BASED SECURITY AUDITOR")
    
    # 1. Ask for the file path
    file_to_scan = "targetcode.js" # You can also use input("Enter file path: ")
    
    print(f"Reading: {file_to_scan}...")
    code_content = read_file_content(file_to_scan)

    if code_content:
        # 2. Feed the file content into the Graph
        initial_input = {
            "code": code_content,
            "context": "",
            "report": ""
        }

        print("Analyzing file content...")
        final_state = app.invoke(initial_input)

        print("\n" + "="*30)
        print("AUDIT REPORT FOR:", file_to_scan)
        print("="*30)
        print(final_state.get('report'))
    else:
        print(f"Error: File '{file_to_scan}' not found.")

if __name__ == "__main__":
    main()