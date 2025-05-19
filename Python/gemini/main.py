# https://ai.google.dev/gemini-api/docs/models?hl=pt-br

from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17",
    contents=
    "x",
    config=types.GenerateContentConfig(
        # 0 a 24576
        thinking_config=types.ThinkingConfig(thinking_budget=12288)
    ),
)

with open("resp.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(response.text)