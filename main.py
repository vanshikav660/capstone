import os
os.environ["GEMINI_API_KEY"]=''

from planner import planner_agent
from component import component_agent

planner = planner_agent
component = component_agent

user_prompt = input("What do you want to build today? ")

planner_output = planner.invoke({
     "messages": [{"role": "user", "content": user_prompt}]
})

component_result = component_generator.invoke({
    "messages": [{
        "role": "user", 
        "content": (
            f"The structural skeleton has been successfully created. "
            f"Please implement the component code using your write_code_to_file tool for: {user_prompt}"
        )
    }]
})
