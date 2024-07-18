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

historico_conversa = ""

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

    historico_conversa += f"Usuário: {pergunta}\n"

    response = model.generate_content(
        historico_conversa 
    )

    resposta_texto = response.text

    historico_conversa += f"Gemini: {resposta_texto}\n"

    print(f"Gemini: {resposta_texto}")

    salvar_resposta(f"Você: {pergunta}\nGemini: {resposta_texto}")

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
  