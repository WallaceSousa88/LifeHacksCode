# pip install google-genai

import logging

from pathlib import Path
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def gemini_thinking_processor(
    input_file: str = "question.txt",
    output_file: str = "Gemini.txt",
    model_id: str = "gemini-2.0-flash-thinking-preview-01-21"
):
    path_q = Path(input_file)
    path_a = Path(output_file)

    if not path_q.exists():
        logging.error(f"Arquivo de entrada '{input_file}' não encontrado.")
        return

    try:
        pergunta = path_q.read_text(encoding="utf-8")
        if not pergunta.strip():
            logging.warning("O arquivo de pergunta está vazio.")
            return
    except Exception as e:
        logging.error(f"Erro ao ler arquivo: {e}")
        return

    try:
        client = genai.Client(api_key="")

        logging.info(f"Enviando pergunta ao modelo {model_id}...")

        response = client.models.generate_content(
            model=model_id,
            contents=pergunta,
            config=types.GenerateContentConfig(
                # 0 a 24576 ~ 12288
                thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=16000)
            ),
        )
    except Exception as e:
        logging.error(f"Erro na API do Gemini: {e}")
        return

    if response.text:
        try:
            path_a.write_text(response.text, encoding="utf-8")
            logging.info(f"Resposta salva com sucesso em '{output_file}'.")
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo de resposta: {e}")
    else:
        logging.warning("A IA retornou uma resposta vazia (pode ter sido bloqueada pelos filtros de segurança).")

if __name__ == "__main__":
    gemini_thinking_processor()