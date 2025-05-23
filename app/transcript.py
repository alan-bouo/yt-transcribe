from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

def get_transcript(video_id: str, proxies: dict = None) -> str:
    try:
        # Essai 1 : en français
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["fr"],
            proxies=proxies
        )
    except NoTranscriptFound:
        # Essai 2 : sans langue précisée = langue par défaut (souvent originale)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                proxies=proxies
            )
        except Exception as e:
            raise RuntimeError(f"Transcript indisponible : {e}")
    except Exception as e:
        raise RuntimeError(f"Erreur transcript : {e}")
    
    return " ".join([t["text"] for t in transcript])
