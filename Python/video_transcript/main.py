# pip install youtube-transcript-api

from youtube_transcript_api import YouTubeTranscriptApi

def baixar_transcricao(video_id, output_file="transcricao.txt"):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        with open(output_file, "w", encoding="utf-8") as file:
            for entry in transcript:
                file.write(f"{entry['start']:.2f} - {entry['text']}\n")
        print(f"Transcrição salva em {output_file}")

    except Exception as e:
        print(f"Erro ao baixar a transcrição: {e}")

if __name__ == "__main__":
    video_url = input("Insira o link do YouTube: ")
    video_id = video_url.split("v=")[1].split("&")[0]
    baixar_transcricao(video_id)