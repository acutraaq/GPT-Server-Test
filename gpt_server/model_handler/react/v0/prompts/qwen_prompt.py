TOOL_SUFFIX_PROMPT = (
    "When calling the above tools, the value of Action Input must use JSON format to represent the called parameters."
)

TOOL_CHOICE_SUFFIX_PROMPT = "\n\n## Note: \nThe above tools must be called!"
# default

TOOL_SYSTEM_PROMPT_CN = """# Tools
## You have the following tools:

{tool_text}

## If using tools, you can insert zero, one or more times the following commands in replies to call tools:

Action: Tool name, must be one of [{tool_names}]
Action Input: Tool input, value must use JSON format, and must be output in one line, cannot wrap lines.
Observation: Result after calling the tool
✿Retrun✿: Reply based on tool results, images need to be rendered with ![](url)"""

TOOl_CHOICE_SYSTEM_PROMPT_CN = """# The provided tools are used to format user input or replies into JSON mode that conforms to tool descriptions, you must forcibly use the following tools:
## Tools
## #You have the following tools:

{tool_text}

### You can insert zero, one or more times the following commands in replies to call tools:

Thought: you should always think about what to do
Action: Tool name, must be one of [{tool_names}]
Action Input: Tool input, value must use JSON format, and must be output in one line, cannot wrap lines.
Observation: Result after calling the tool
✿Retrun✿: Reply based on tool results, images need to be rendered with ![](url)"""
