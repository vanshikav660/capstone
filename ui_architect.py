import os
import re
from pathlib import Path
from langchain.agents import create_agent

# ── API Key ───────────────────────────────────────────────────────────────────
os.environ["OPENROUTER_API_KEY"] = ""

# ── Model ─────────────────────────────────────────────────────────────────────
MODEL = "openrouter:openrouter/free"

# ── Tools ─────────────────────────────────────────────────────────────────────

def create_folder(path: str) -> str:
    """Create a folder at the given path."""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return f"Created folder: {path}"
    except Exception as e:
        return f"Error creating folder: {e}"


def create_empty_file(path: str) -> str:
    """Create an empty file at the given path."""
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).touch()
        return f"Created file: {path}"
    except Exception as e:
        return f"Error creating file: {e}"


def list_created_structure(base_path: str) -> str:
    """List all files and folders created under base path."""
    try:
        result = []
        for p in sorted(Path(base_path).rglob("*")):
            depth = len(p.relative_to(base_path).parts) - 1
            indent = "  " * depth
            result.append(f"{indent}{p.name}")
        return "\n".join(result) if result else "No files found."
    except Exception as e:
        return f"Error listing structure: {e}"


# ── Agent ─────────────────────────────────────────────────────────────────────

agent = create_agent(
    model=MODEL,
    tools=[create_folder, create_empty_file, list_created_structure],
    system_prompt="""You are a UI Architect Agent for React applications.

You receive a project plan in markdown format and a base project path.
Your job is to create the complete folder structure and empty files on disk.

You must:
1. Read the folder structure from the plan carefully
2. Create all required folders using create_folder
3. Create all required empty files using create_empty_file
4. Always create these standard files if not already in the plan:
   - src/App.jsx
   - src/main.jsx
   - src/index.css
   - package.json
   - index.html
5. After creating everything, verify using list_created_structure
6. Report exactly what was created

Rules:
- Never write any code inside the files, leave them completely empty
- Always use the base project path provided as the root
- Create src/pages/ for page components
- Create src/components/ for reusable components
- Do not create node_modules or any build folders
- Be precise and systematic, create folders before files""",
)

# ── Main function ─────────────────────────────────────────────────────────────

def run_ui_architect(project_plan: str, base_path: str) -> str:
    """Takes project plan and base path, creates folder structure and empty files."""
    print(f"\nUI Architect Agent creating structure at: {base_path}\n")

    prompt = f"""Here is the project plan:

{project_plan}

Create the complete folder structure and all empty files at this base path: {base_path}

Follow the folder structure exactly as specified in the plan.
After creating everything, list what was created."""

    result = agent.invoke({
        "messages": [{"role": "user", "content": prompt}]
    })

    output = result["messages"][-1].content

    # Save architecture report
    with open(os.path.join(base_path, "architecture_report.md"), "w", encoding="utf-8") as f:
        f.write(output)

    print("Architecture report saved to architecture_report.md")
    return output


# ── Run directly for testing ──────────────────────────────────────────────────

if __name__ == "__main__":
    # Read plan from planner's output file
    plan_path = "project_plan.md"

    if not os.path.exists(plan_path):
        print("No project_plan.md found. Run planner_agent.py first.")
        exit()

    with open(plan_path, "r", encoding="utf-8") as f:
        plan = f.read()

    base_path = input("Enter the folder path where the project should be created (e.g. D:\\AIagent\\my_react_app): ").strip()

    output = run_ui_architect(plan, base_path)
    print("\n── UI Architect Output ──")
    print(output)
