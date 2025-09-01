import requests

subscription_key = "x"
endpoint = "https://eastus2.tts.speech.microsoft.com/cognitiveservices/v1"

with open("x.txt", "r", encoding="utf-8") as file:
    text = file.read()

voice_name = "pt-BR-FranciscaNeural"
style = "cheerful"

headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Content-Type": "application/ssml+xml",
    "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
    "User-Agent": "CopilotPythonTTS"
}

ssml = f"""
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'
       xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='pt-BR'>
  <voice name='{voice_name}'>
    <mstts:express-as style='{style}'>
      {text}
    </mstts:express-as>
  </voice>
</speak>
"""

response = requests.post(endpoint, headers=headers, data=ssml.encode("utf-8"))

if response.status_code == 200:
    with open("output.wav", "wb") as audio:
        audio.write(response.content)
    print("Áudio gerado com sucesso: output.wav")
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
