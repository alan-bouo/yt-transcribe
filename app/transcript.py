from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

def get_transcript(video_id: str, proxies: dict = None) -> str:
    try:
        # Essai 1 : en français
        print(f"Attempting to get transcript for video {video_id} in French")
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["fr"],
            proxies=proxies
        )
        print(f"Successfully got French transcript for video {video_id}")
        return " ".join([t["text"] for t in transcript])
    
    except NoTranscriptFound:
        print(f"No French transcript found for video {video_id}, trying default language")
        # Essai 2 : sans langue précisée = langue par défaut (souvent originale)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                proxies=proxies
            )
            print(f"Successfully got default language transcript for video {video_id}")
            return " ".join([t["text"] for t in transcript])
        except Exception as e:
            print(f"Error getting default language transcript for {video_id}: {str(e)}")
            raise RuntimeError(f"Transcript indisponible : {str(e)}")
    except Exception as e:
        print(f"Error getting transcript for {video_id}: {str(e)}")
        raise RuntimeError(f"Erreur transcript : {str(e)}")
