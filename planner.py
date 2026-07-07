import os
from langchain.agents import create_agent

# ── API Key ───────────────────────────────────────────────────────────────────
os.environ["OPENROUTER_API_KEY"] = "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"

# ── Model ─────────────────────────────────────────────────────────────────────
MODEL = "openrouter:openrouter/free"

# ── Agent ─────────────────────────────────────────────────────────────────────
agent = create_agent(
    model=MODEL,
    tools=[],
    system_prompt="""You are a senior frontend project planner specializing in React applications.

When given a natural language description of a web application, you must produce a complete, structured project plan.

Your output must always follow this exact format:

## Project Plan

### Project Overview
- App Name: (suggest a name)
- Framework: React with Vite
- Styling: Tailwind CSS
- Complexity: (Simple / Medium / Complex)

### Pages
List every page the app needs:
- Page 1: (name and purpose)
- Page 2: (name and purpose)

### Components
List all reusable components needed:
- Component 1: (name and purpose)
- Component 2: (name and purpose)

### Routing Structure
- / → (which page)
- /route → (which page)

### Dependencies
List all npm packages needed beyond React:
- package-name: (reason)

### Folder Structure
src/
  pages/
    (list page files)
  components/
    (list component files)
  App.jsx
  main.jsx

### Hardcoded Data Notes
List any data that will be hardcoded since there is no backend:
- (data item and where it's used)

Be specific, practical, and concise. No extra commentary outside this format.""",
)

# ── Main function ─────────────────────────────────────────────────────────────

def run_planner(user_requirement: str) -> str:
    """Takes user requirement, returns structured project plan."""
    print("\nPlanner Agent thinking...\n")

    result = agent.invoke({
        "messages": [{"role": "user", "content": user_requirement}]
    })

    plan = result["messages"][-1].content

    # Save plan to file so other agents can read it
    with open("project_plan.md", "w", encoding="utf-8") as f:
        f.write(plan)

    print("Project plan saved to project_plan.md")
    return plan


# ── Run directly for testing ──────────────────────────────────────────────────

if __name__ == "__main__":
    requirement = input("Describe the React app you want to build: ")
    plan = run_planner(requirement)
    print("\n── Planner Output ──")
    print(plan)