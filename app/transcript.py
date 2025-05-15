from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str, proxies: dict = None, languages: list = ['fr']) -> str:
    transcript = YouTubeTranscriptApi.get_transcript(
        video_id,
        languages=languages,
        proxies=proxies)
    return " ".join([t["text"] for t in transcript])
