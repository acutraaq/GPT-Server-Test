TOOL_SUFFIX_PROMPT = (
    "When calling the above tools, the value of action_input must use JSON format to represent the called parameters."
)

TOOL_CHOICE_SUFFIX_PROMPT = "\n\n## Note: \nThe above tools must be called!"
# default

TOOL_SYSTEM_PROMPT_CN = """# Tools
## You have the following tools:

{tool_text}

## If using tools, you can reply zero, one or more times with the following JSON format content to call tools. After calling tools, Observation represents the result of calling the tool. The JSON format is as follows:
{{
    "thought":"You should always think about what to do",
    "reason":{{
        "action":"Tool name, must be one of [{tool_names}]",
        "action_input":"Tool input, value must use JSON format"
    }}
}}
or
{{
    "thought":"You should always think about what to do",
    "reason":{{
        "final_answer":"Reply based on tool results, if tool return value contains image URL, render it with ![](url)"
    }}
}}
"""

TOOl_CHOICE_SYSTEM_PROMPT_CN = """# The provided tools are used to format user input or replies into JSON mode that conforms to tool descriptions, you must forcibly use the following tools:
## Tools
## #You have the following tools:

{tool_text}

### You can insert zero, one or more times the following JSON format content in replies to call tools. After calling tools, Observation represents the result of calling the tool. The JSON format is as follows:
{{
    "thought":"You should always think about what to do",
    "reason":{{
        "action":"Tool name, must be one of [{tool_names}]",
        "action_input":"Tool input, value must use JSON format"
    }}
}}
or
{{
    "thought":"You should always think about what to do",
    "reason":{{
        "final_answer":"Reply based on tool results, if tool return value contains image URL, render it with ![](url)"
    }}
}}"""
