# pip install youtube-transcript-api

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def baixar_transcricao(video_id, output_file="transcricao.txt"):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
    except NoTranscriptFound:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except NoTranscriptFound:
            print("Não foi possível encontrar transcrição em português ou inglês para este vídeo.")
            return
        except TranscriptsDisabled:
            print("As transcrições estão desativadas para este vídeo.")
            return
        except Exception as e:
            print(f"Erro ao baixar a transcrição: {e}")
            return
    except TranscriptsDisabled:
        print("As transcrições estão desativadas para este vídeo.")
        return
    except Exception as e:
        print(f"Erro ao baixar a transcrição: {e}")
        return

    with open(output_file, "w", encoding="utf-8") as file:
        for entry in transcript:
            time = entry['start']
            text = entry['text']
            file.write(f"{time:.2f} - {text}\n")
    print(f"Transcrição salva em {output_file}")

if __name__ == "__main__":
    video_url = input("Insira o link do YouTube: ")
    if "watch?v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    else:
        video_id = video_url.split("/")[-1]
    baixar_transcricao(video_id)
