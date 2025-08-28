from openai import OpenAI
from pydantic import BaseModel, Field

# New version OpenAI
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8082/v1")
# Method 1
output = client.chat.completions.create(
    model="qwen",
    messages=[{"role": "user", "content": "How far is it from Nanjing to Beijing?"}],
    response_format={"type": "text"},
)
print(output.choices[0].message.content)
print("-" * 100)
# Method 2
output = client.chat.completions.create(
    model="qwen",
    messages=[
        {"role": "system", "content": "Answer using JSON"},
        {"role": "user", "content": "How far is it from Nanjing to Beijing?"},
    ],
    response_format={"type": "json_object"},
)
print(output.choices[0].message.content)
print("-" * 100)


# Method 3
class Distance(BaseModel):
    distance: int = Field()
    unit: str


output = client.beta.chat.completions.parse(
    model="qwen",
    messages=[{"role": "user", "content": "How far is it from Nanjing to Beijing?"}],
    response_format=Distance,
)

print(output.choices[0].message.parsed.dict())
print()
