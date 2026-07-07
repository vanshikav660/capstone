import os
import json
from pathlib import Path
from langchain.agents import create_agent

# ── API key ──────────────────────────────────────────────────────────────────
os.environ["OPENROUTER_API_KEY"] = "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"

# ── Model ────────────────────────────────────────────────────────────────────
MODEL = "openrouter:openrouter/free"

# ── Tools ────────────────────────────────────────────────────────────────────

def read_file(filepath: str) -> str:
    """Read a file and return its contents as a string."""
    try:
        return Path(filepath).read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"


def list_files(folder: str) -> str:
    """List all files in a folder recursively."""
    try:
        files = [str(p) for p in Path(folder).rglob("*") if p.is_file()]
        return "\n".join(files) if files else "No files found."
    except Exception as e:
        return f"Error listing files: {e}"


def write_file(filepath: str, content: str) -> str:
    """Write corrected content to a file."""
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        Path(filepath).write_text(content, encoding="utf-8")
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"


def save_review_report(report: str, output_path: str = "review_report.md") -> str:
    """Save the review report to a markdown file."""
    try:
        Path(output_path).write_text(report, encoding="utf-8")
        return f"Review report saved to {output_path}"
    except Exception as e:
        return f"Error saving report: {e}"


# ── Agent ────────────────────────────────────────────────────────────────────

agent = create_agent(
    model=MODEL,
    tools=[read_file, list_files, write_file, save_review_report],
    system_prompt="""You are a senior frontend code reviewer specializing in React applications.

Your job is to review generated React codebases and produce a structured review report.

When given a folder path, you must:
1. List all files in that folder using list_files
2. Read each relevant file (.jsx, .tsx, .js, .ts, .css, .json) using read_file
3. Review each file for:
   - Correctness: Does the code work logically? Are there syntax errors?
   - Consistency: Are naming conventions, indentation, and patterns consistent?
   - Completeness: Are imports missing? Are components incomplete?
   - React best practices: Proper use of props, state, keys in lists, etc.
4. For each file with issues, write a corrected version using write_file
5. Save a full review report using save_review_report

Your review report must follow this exact structure:
## Review Report

### Summary
- Total files reviewed: X
- Files with issues: X
- Files that passed: X
- Overall quality: (Poor / Fair / Good / Excellent)

### File-by-File Review
For each file:
**File:** filename
**Status:** Pass / Fail
**Issues found:**
- issue 1
- issue 2
**Corrections made:** Yes / No

### Overall Recommendations
- recommendation 1
- recommendation 2

Do not flood with unnecessary content. Be precise and technical.""",
)


# ── Main ─────────────────────────────────────────────────────────────────────

def run_reviewer(project_folder: str):
    """Run the reviewer agent on a given project folder."""
    print(f"\nReviewer Agent starting review of: {project_folder}\n")

    prompt = f"""Please review the React project located at: {project_folder}
    
List all files first, then read and review each one.
After reviewing, save a complete review report and correct any files that have issues."""

    result = agent.invoke({
        "messages": [{"role": "user", "content": prompt}]
    })

    final_message = result["messages"][-1].content
    print("\n── Reviewer Agent Final Output ──")
    print(final_message)
    return final_message


if __name__ == "__main__":
    folder = input("Enter the path to the React project folder to review: ").strip()
    run_reviewer(folder)