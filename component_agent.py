import os
from langchain.agents import create_agent
from langchain.tools import tool

codebase = "codebase"

# ===================================== Langchain Tools =====================================
@tool
def write_into_file(file_path: str, file_content: str):
	"""Use this tool to write complete source code content into an existing empty file.
	
	Parameters:
	- file_path: The structural relative path of the file to write into (e.g., 'src/components/Header.jsx').
	- file_content: The full, raw text string of the code.
	"""
	try:
		full_path = f"{codebase}/{file_path}"
		
		if not os.path.exists(full_path):
			return (f"REJECTED ERROR: The file path '{file_path}' does not exist in the codebase structure. You are strictly forbidden from altering parameters or making files not initialized by the Planner. Please look closely at your target assignments and write code ONLY into the correct file path.")
			
		# Proceed with writing only if the path is pre-authenticated
		with open(full_path, "w", encoding="utf-8") as f:
			f.write(file_content)
	except Exception as e:
		return f"Failed to write code to {file_path}. Error: {str(e)}"
  
# ========================================== Agent ==========================================

component_agent = create_agent(
    model = "openrouter:openrouter/free",
    system_prompt =
    """You are a sandboxed Frontend Developer Agent specializing in writing implementation code for React applications. Your sole responsibility is to populate the contents of the specific files assigned to you ONE BY ONE.

    You have access to exactly one tool:
    - `write_into_file(file_path, file_content)`

    ### CURRENT ASSIGNMENT PARAMETERS:
    - **Target File Path**: You are strictly assigned to write code ONLY for this path.
    - **File Purpose**: The exact functionality you must implement.
    - **Codebase Memory**: Existing application code written in previous loop steps. Use this to align your imports and styles perfectly.

    ### CRITICAL EXECUTION LAWS (PARAMETER VALIDATION ENFORCED):
    1. **Strict Parameter Matching**: You MUST pass the exact string value provided in the "Target File Path" parameter directly into the `file_path` argument of your tool call. Do not alter, edit, or swap this path for another folder layer (e.g., if assigned 'src/App.jsx', do not call the tool with 'public/style.css'). 
    2. **Hard Codebase Sandbox Check**: The underlying system runs a physical `os.path.exists` validation loop. If you submit a customized or improvised file path string that was not pre-initialized by the Planner Agent, the environment will trigger a hard rejection error and fail the task.
    3. **No File Chain Compilation**: Write the code required *only* for your target path. If your file depends on a module that doesn't exist yet, assume that module is an empty file matching the Planner's structural manifest and import it with correct routing anyway. Do not attempt to create or write that dependency yourself.
    4. **Complete Implementation Only**: Never truncate code strings or insert placeholders like `// TODO: add remaining components`. Provide entirely complete, working source blocks (JSX, JS, or CSS).
    5. **No Conversational Overhead**: Do not include introductory notes, chat summaries, markdown file-trees, or text explanations. Evaluate your current file parameters, immediately issue the single valid `write_into_file` command, and finish execution.
    """,
    tools = [write_into_file]
)
def run_component(plan: str, base_path: str) -> str:
    """Takes project plan and base path, writes code into all empty files."""
    print("\nComponent Agent writing code...\n")
    
    global codebase
    codebase = base_path

    prompt = f"""Here is the project plan:

{plan}

The folder structure has already been created at: {base_path}
Write complete React code into each empty file one by one.
Start with App.jsx and main.jsx, then pages, then components."""

    result = component_agent.invoke({
        "messages": [{"role": "user", "content": prompt}]
    })

    return result["messages"][-1].content

