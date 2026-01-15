import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

subscription_key = os.getenv("AZURE_TTS_KEY")
endpoint = "https://eastus2.tts.speech.microsoft.com/cognitiveservices/v1"

def generate_tts(text, voice="pt-BR-FranciscaNeural", style="cheerful", filename="output.wav"):
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
        "User-Agent": "CopilotPythonTTS"
    }
    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'
           xmlns:mstts='http://www.w3/mstts' xml:lang='pt-BR'>
      <voice name='{voice}'>
        <mstts:express-as style='{style}'>
          {text}
        </mstts:express-as>
      </voice>
    </speak>
    """
    try:
        response = requests.post(endpoint, headers=headers, data=ssml.encode("utf-8"))
        response.raise_for_status()
        with open(filename, "wb") as audio:
            audio.write(response.content)
        logging.info(f"Áudio gerado com sucesso: {filename}")
    except Exception as e:
        logging.error(f"Erro ao gerar áudio: {e}")

with open("x.txt", "r", encoding="utf-8") as file:
    text = file.read().strip()
    if text:
        generate_tts(text, style="cheerful", filename="audios/francisca_cheerful.wav")