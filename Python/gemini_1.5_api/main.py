# pip install google-generativeai
# https://ai.google.dev/gemini-api/docs
# https://status.cloud.google.com/

import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

chat = model.start_chat(history=[])

print("Conversa iniciada!")
while True:
    mensagem = input("Sua mensagem: ")
    if mensagem.lower() == "sair":
        break

    response = chat.send_message({"parts": [{"text": mensagem}]})
    print(f"Gemini: {response.text}")
