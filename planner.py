import os
from langchain.agents import create_agent
from langchain.tools import tool

codebase = "codebase"

# ===================================== Langchain Tools =====================================
@tool
def make_directory(dir_path: str):  
    """Use this tool to create a new folder. It takes only one parameter 'dir_path' which is the path of the directory to be created
    """
    try:
        os.makedirs(f"{codebase}/{dir_path}", exist_ok=True)
    except Exception as e:
        return f"Failed to create directory {dir_path}. Error: {str(e)}"

@tool  
def make_file(file_path: str):  
    """Use this tool to create a new file. It takes only one parameter 'file_path' which is the address of the file to be created"""
    try:
        full_path = f"{codebase}/{file_path}"
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("")
    except Exception as e:
        return f"Failed to create file {file_path}. Error: {str(e)}"
    
@tool
def pass_to_component(content: str): 
    with open("w", encoding="utf-8") as f:
            f.write(content)
      

# ========================================== Agent ==========================================
planner_agent = create_agent(
    model = "google_genai:gemini-2.5-flash-lite",
    system_prompt =
    """
    You are an expert Software Architect Agent specialising in React applications. When given a natural language description of a web application, your sole task is to generate complete, empty directory and file structures based on user requirements.

    You have access to three tools:
    1. `make_directory(dir_path)` - Creates a folder at the specified path.
    2. `make_file(file_path)` - Creates a completely empty file at the specified path.
    3. `pass_to_component() - Pass instructions to the component agent to write code inside the empty files one by one

    ### CRITICAL EXECUTION RULES:
    1. **Order of Operations (Crucial)**: You must always call `make_directory` for a folder BEFORE attempting to create any empty files inside it via `make_file`. If you try to create a file inside a folder that doesn't exist yet, the system will error out.
    2. **Sequential Creation**: When building a nested path (e.g., `src/features/auth`), create the directories first, then create the files inside them. 
    3. **Completely Empty Files**: Do not attempt to write code, content, boilerplate, or comments into the files. The `make_file` only accepts a `file_path` parameter and generates completely blank files.
    4. **No Visual Explanations**: Do not explain your steps, do not provide markdown tree diagrams, and do not write conversational text. Simply analyze the request and execute the tool calls required to build the structure.
    5. **Report for Component Agent** - After all the steps above are completed, pass a .md file instructing the component agent about the user prompt and about what code to write in the created empty files.

    ### WORKFLOW:
    1. Identify all directories needed for the requested project architecture.
    2. Call `make_directory` to create those folders.
    3. Call `make_file` to populate those folders with the necessary blank files.
    4. Write in 
    """,
    tools = [make_directory, make_file]
)

