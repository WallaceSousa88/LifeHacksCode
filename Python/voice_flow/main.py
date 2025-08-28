# pip install pyttsx3

import pyttsx3
import os

def listar_vozes():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if not voices:
        print("Nenhuma voz SAPI5 encontrada no sistema.")
        return []

    print("Vozes disponíveis no seu sistema:")
    for i, voice in enumerate(voices):
        idioma = voice.languages[0] if voice.languages else 'N/A'
        print(f"{i+1}. ID: {voice.id}, Nome: {voice.name}, Idioma: {idioma}")

    return voices

def gerar_audio(texto, filename="output.wav", voice_id=None, rate=170, volume=1.0):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    voices = engine.getProperty('voices')
    selected_voice = None

    if voice_id:
        for voice in voices:
            if voice.id == voice_id:
                selected_voice = voice
                break

    if not selected_voice:
        for voice in voices:
            if voice.languages and 'pt-BR' in voice.languages:
                selected_voice = voice
                break
        if not selected_voice:
            selected_voice = voices[0]
            print(f"Usando a voz padrão: {selected_voice.name} (ID: {selected_voice.id})")
        else:
            print(f"Usando a voz em português: {selected_voice.name} (ID: {selected_voice.id})")
    else:
        print(f"Usando a voz especificada: {selected_voice.name} (ID: {selected_voice.id})")

    engine.setProperty('voice', selected_voice.id)

    print(f"Gerando áudio e salvando em {filename}...")
    engine.save_to_file(texto, filename)
    engine.runAndWait()

    if os.path.exists(filename):
        print(f"Áudio salvo com sucesso em: {os.path.abspath(filename)}")
    else:
        print(f"Erro: O arquivo '{filename}' não foi criado. Tente salvar em .wav.")

if __name__ == "__main__":
    vozes = listar_vozes()
    with open("x.txt", "r", encoding="utf-8") as arquivo:
        texto = arquivo.read()
    gerar_audio(texto, filename="x.wav", voice_id=None)
