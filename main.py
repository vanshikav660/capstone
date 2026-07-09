import os
os.environ["OPENROUTER_API_KEY"] = "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"
from planner_agent import run_planner
from ui_architect_agent import run_ui_architect
from reviewer_agent import run_reviewer
from component_agent import run_component

def main():
    print("=" * 50)
    print("Welcome to FrontForge AI")
    print("=" * 50)

    # Step 1 - Get user requirement
    user_requirement = input("\nDescribe the React app you want to build: ").strip()

    # Step 2 - Planner Agent
    print("\n[1/3] Running Planner Agent...")
    plan = run_planner(user_requirement)
    print("✓ Plan created")

    # Step 3 - UI Architect Agent
    print("\n[2/3] Running UI Architect Agent...")
    base_path = os.path.join("D:\\AIagent", user_requirement.split()[0].lower() + "_app")
    structure = run_ui_architect(plan, base_path)
    print(f"✓ Folder structure created at {base_path}")

    print("\n[3/4] Running Component Agent...")
    run_component(plan, base_path)
    print("✓ Components generated")

    # Step 4 - Reviewer Agent
    print("\n[3/3] Running Reviewer Agent...")
    review = run_reviewer(base_path)
    print("✓ Review complete")

    print("\n" + "=" * 50)
    print("Pipeline Complete!")
    print(f"Project location: {base_path}")
    print("Check project_plan.md for the plan")
    print("Check review_report.md for the review")
    print("=" * 50)

main()