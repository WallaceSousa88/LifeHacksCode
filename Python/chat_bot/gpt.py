from openai import OpenAI
import os

client = OpenAI(api_key="x")

def gpt(patch_q="question.txt", patch_a="gpt.txt"):
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": pergunta}
            ]
        )
    except Exception as e:
        print(f"Erro ao gerar conteúdo com o GPT: {e}")
        return

    try:
        with open(patch_a, "w", encoding="utf-8") as f:
            f.write(response.choices[0].message.content)
    except Exception as e:
        print(f"Erro ao escrever a resposta no arquivo '{patch_a}': {e}")
