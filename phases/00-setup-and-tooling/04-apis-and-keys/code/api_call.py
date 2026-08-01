import os 
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com",
)

resp = client.chat.completions.create(
    model="deepseek-chat",
    max_tokens=256,
    messages=[{"role" : "user",
               "content" : "what is a neural network in one sentence?"}],
)

print(resp.choices[0].message.content)