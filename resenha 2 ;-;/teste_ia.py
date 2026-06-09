from openai import OpenAI

client = OpenAI(api_key="SUA_API_KEY_AQUI")

res = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Diga oi em uma frase"}]
)

print(res.choices[0].message.content)