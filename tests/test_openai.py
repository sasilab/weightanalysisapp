
from openai import OpenAI
client = OpenAI()

res = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(res.choices[0].message.content)
