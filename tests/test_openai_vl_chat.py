import base64
from openai import OpenAI
from pathlib import Path


def image_to_base64(image_path):
    """Convert image to Base64 string"""
    base64_prefix = "data:image/png;base64,"

    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_prefix + base64_string


image_path = Path(__file__).parent.parent / "assets/logo.png"
# Use local image
url = image_to_base64(image_path)
# Use network image
url = "https://opencompass.oss-cn-shanghai.aliyuncs.com/image/compass-hub/botchat_banner.png"

# New version OpenAI
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8082/v1")

stream = True
output = client.chat.completions.create(
    model="glm4.1v",  # internlm chatglm3  qwen  llama3 chatglm4
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Please describe this picture",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url,
                    },
                },
            ],
        }
    ],
    stream=stream,
)
if stream:
    for chunk in output:
        print(chunk.choices[0].delta.content or "", end="", flush=True)
else:
    print(output.choices[0].message.content)
print()
