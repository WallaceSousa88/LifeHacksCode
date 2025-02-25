# https://ai.google.dev/gemini-api/docs
# https://status.cloud.google.com/

# pip install google-generativeai

import os
import google.generativeai as genai

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está definida.")
    exit()

genai.configure(api_key=api_key)

# for model in genai.list_models():
#   print(f"Nome do modelo: {model.name}")
#   print(f"  Descrição: {model.description}")
#   print(f"  Capabilities: {model.supported_generation_methods}")

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
print("-" * 30)

while True:
    mensagem = input("Sua mensagem: ")
    if mensagem.lower() == "sair":
        break

    print("-" * 30)
    try:
        response = chat.send_message({"parts": [{"text": mensagem}]})
        print(f"Gemini: {response.text}")
    except Exception as e:
        print(f"Erro ao comunicar com o Gemini: {e}")
    print("-" * 30)