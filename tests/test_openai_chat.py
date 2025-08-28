from openai import OpenAI

# New version OpenAI
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8082/v1")

stream = True
output = client.chat.completions.create(
    model="qwen",  # internlm chatglm3  qwen  llama3 chatglm4 qwen-72b
    messages=[{"role": "user", "content": "Who are you?"}],
    stream=stream,
)
if stream:
    for chunk in output:
        print(chunk.choices[0].delta.content or "", end="", flush=True)
else:
    print(output.choices[0].message.content)
print()
