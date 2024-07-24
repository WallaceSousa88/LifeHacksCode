# pip install google-generativeai
# https://ai.google.dev/gemini-api/docs
# https://status.cloud.google.com/

import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-pro')

chat = model.start_chat(history=[])

print("Conversa iniciada com o Gemini Pro!")
while True:
    mensagem = input("Sua mensagem: ")
    if mensagem.lower() == "sair":
        break

    response = chat.send_message({"parts": [{"text": mensagem}]})
    print(f"Gemini: {response.text}")
