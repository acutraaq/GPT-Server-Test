from openai import OpenAI
from rich import print
import numpy as np

# New version OpenAI
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8082/v1")
# model: acge_text_embedding yinka zpoint
response = client.embeddings.create(
    model="Conan-embedding-v1", input=["I like you", "I like you too"]
)
print(response.data)
embeddings = [np.array(item.embedding) for item in response.data]  # Convert to NumPy array

v_a = embeddings[0].reshape(1, -1)  # Vector a
v_b = embeddings[1].reshape(-1, 1)  # Vector b
print(v_a.shape)
# Calculate cosine similarity
similarity = np.dot(v_a, v_b)[0][0]
print(f"Cosine similarity: {similarity:.4f}")
