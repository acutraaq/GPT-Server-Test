TOOL_SUFFIX_PROMPT = (
    "When calling the above tools, the value of Action Input must use JSON format to represent the called parameters."
)

TOOL_CHOICE_SUFFIX_PROMPT = "\nNote: The above tools must be called!"
# default
TOOL_SYSTEM_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

{tool_text}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question:"""
TOOL_SYSTEM_PROMPT_CN = """Answer user questions as best as possible, you have access to the following tools:

{tool_text}

If using tools, please follow the format below:

Thought: Think about what problem the current step needs to solve, whether tools are needed
Action: Tool name, your tool must be selected from [{tool_names}]
Action Input: Tool input parameters, the value of Action Input must use JSON format to represent the called parameters.
Observation: Result after calling the tool
... (Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: Final answer to the original input question

Begin!"""

TOOl_CHOICE_SYSTEM_PROMPT_CN = """You are a tool execution assistant, the provided tools may be used to format user input into JSON mode that conforms to tool descriptions or other functions. You need to judge for yourself, you must forcibly use the following tools:

{tool_text}

Follow the format below:

Thought: I must forcibly execute {tool_names} tool
Action: Tool name must be {tool_names}
Action Input: Tool input parameters, the value of Action Input must use JSON format to represent the called parameters.
Observation: Result after calling the tool
Thought: I now know the final answer
Final Answer: Final answer to the original input question

Begin!"""
TOOl_CHOICE_SYSTEM_PROMPT = """You must use the following tools:

{tool_text}

Use the following format:

Question: the input question you must answer
Thought: I have to execute tool {tool_names}
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question:"""

# Your task is to provide appropriate responses and support for users' questions and requirements
GLM4_TOOL_PROMPT = """"You can use the following tools to provide appropriate responses and support.

# Available tools
{tool_text}
Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question:
"""
