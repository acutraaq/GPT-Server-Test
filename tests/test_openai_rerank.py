from openai import OpenAI
from rich import print

# New version OpenAI
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8082/v1")
data = client.embeddings.create(
    model="bge-reranker-base",
    input=["Who are you?", "How old are you this year?"],
    extra_body={"query": "How old are you?"},
)

print(data.data)
