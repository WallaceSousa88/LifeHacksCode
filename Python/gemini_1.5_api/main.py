# pip install google-generativeai
# https://status.cloud.google.com/

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

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

historico = []

chat_session = model.start_chat(
  history=historico
)

def carregar_pergunta(nome_arquivo="pergunta.txt"):
  """Carrega a pergunta do arquivo."""
  if os.path.exists(nome_arquivo):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
      pergunta = arquivo.read().strip()
    return pergunta
  else:
    return None

def salvar_resposta(resposta, nome_arquivo="resposta.txt"):
    """Salva a resposta no arquivo, criando-o se não existir."""
    with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write(resposta + "\n")

while True:
  pergunta = carregar_pergunta()
  if pergunta:
    print(f"Você: {pergunta}")

    historico.append(f"Usuário: {pergunta}")
    response = chat_session.send_message(pergunta)
    historico.append(f"Gemini: {response.text}")
    print(f"Gemini: {response.text}")

    salvar_resposta(f"Você: {pergunta}\nGemini: {response.text}")

    with open("pergunta.txt", "w", encoding="utf-8") as arquivo:
      arquivo.write("")
  else:
    print("Arquivo 'pergunta.txt' não encontrado. Crie o arquivo com sua pergunta.")
    break

  if input("Deseja fazer outra pergunta? (s/n): ").lower() != 's':
    if os.path.exists("resposta.txt"):
      os.remove("resposta.txt")
      print("Arquivo 'resposta.txt' deletado.")
    break
