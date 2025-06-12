from youtube_transcript_api import YouTubeTranscriptApi
import time
import random

def get_transcript(video_id: str, proxies: dict = None):
    """Récupérer les sous-titres d'une vidéo YouTube"""
    
    try:
        # Ajouter un délai aléatoire pour éviter le rate limiting
        delay = random.uniform(1, 3)
        time.sleep(delay)
        
        # Vérifier les sous-titres disponibles
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, proxies=proxies)
        
        # Essayer de récupérer le transcript en français
        try:
            transcript = transcript_list.find_transcript(['fr'])
        except Exception:
            # Si pas de français, prendre le premier disponible
            transcript = next(iter(transcript_list))
        
        # Récupérer le transcript
        transcript_data = transcript.fetch()
        
        # Convertir en texte continu
        full_text = " ".join([snippet.text for snippet in transcript_data])
        
        return full_text
        
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la récupération du transcript: {str(e)}")