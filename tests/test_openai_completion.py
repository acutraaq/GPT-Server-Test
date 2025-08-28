from openai import OpenAI
import time
from rich import print

# New version OpenAI
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8082/v1")

t1 = time.time()
output = client.completions.create(
    model="qwen", prompt=["Count from 1 to 10. Start: 1, 2,"] * 8, max_tokens=1000
)


for completion_choice in output.choices:
    print(completion_choice.index + 1, "--->", completion_choice.text)
print("cost time:", time.time() - t1)
