# pip install google-genai

from google import genai
from google.genai import types

def gemini(patch_q="question.txt", patch_a="Gemini.txt"):
    try:
        with open(patch_q, "r", encoding="utf-8") as f:
            pergunta = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{patch_q}' não foi encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo de pergunta: {e}")
        return

    try:
        client = genai.Client()
        response = client.models.generate_content(
            # https://ai.google.dev/gemini-api/docs/thinking?hl=pt-br
            model="gemini-2.5-flash-preview-05-20",
            contents=pergunta,
            config=types.GenerateContentConfig(
                # 0 a 24576 ~ 12288
                thinking_config=types.ThinkingConfig(thinking_budget=24576)
            ),
        )
    except Exception as e:
        print(f"Erro ao gerar conteúdo com o Gemini: {e}")
        return

    try:
        with open(patch_a, "w", encoding="utf-8") as f:
            f.write(response.text)
    except Exception as e:
        print(f"Erro ao escrever a resposta no arquivo '{patch_a}': {e}")