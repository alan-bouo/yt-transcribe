from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import requests
from time import sleep
import socket
from urllib3.exceptions import ReadTimeoutError

class TimeoutException(Exception):
    """Exception personnalisée pour gérer les timeouts"""
    pass

def check_video_exists(video_id: str, proxies: dict = None) -> bool:
    try:
        # Vérifier si la vidéo existe en essayant d'accéder à sa page
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        return response.status_code == 200
    except Exception as e:
        print(f"Error checking video existence: {str(e)}")
        return False

def check_transcript_available(video_id: str, proxies: dict = None) -> bool:
    """Vérifie si des sous-titres sont disponibles pour la vidéo"""
    try:
        # Démarrer un timer pour gérer le timeout
        socket.setdefaulttimeout(30)
        # Vérifier si des sous-titres sont disponibles
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, proxies=proxies)
        return len(list(transcript_list.transcripts)) > 0
    except Exception as e:
        print(f"Error checking transcript availability: {str(e)}")
        return False

def get_transcript(video_id: str, proxies: dict = None) -> str:
    try:
        print(f"Checking if video {video_id} exists...")
        if not check_video_exists(video_id, proxies):
            raise RuntimeError("Video not found or inaccessible")
            
        print(f"Checking if transcript is available for video {video_id}...")
        if not check_transcript_available(video_id, proxies):
            raise RuntimeError("No transcript available for this video")
            
        # Essai 1 : en français
        print(f"Attempting to get transcript for video {video_id} in French")
        try:
            # Démarrer un timer pour gérer le timeout
            socket.setdefaulttimeout(30)
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=["fr"],
                proxies=proxies
            )
            print(f"Successfully got French transcript for video {video_id}")
            return " ".join([t["text"] for t in transcript])
        except socket.timeout:
            print(f"Timeout occurred while getting French transcript for {video_id}")
            raise TimeoutException("Timeout while getting transcript")
        
    except NoTranscriptFound:
        print(f"No French transcript found for video {video_id}, trying default language")
        # Essai 2 : sans langue précisée = langue par défaut (souvent originale)
        try:
            # Ajouter un délai supplémentaire
            sleep(2)
            try:
                # Démarrer un timer pour gérer le timeout
                socket.setdefaulttimeout(30)
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    proxies=proxies
                )
                print(f"Successfully got default language transcript for video {video_id}")
                return " ".join([t["text"] for t in transcript])
            except socket.timeout:
                print(f"Timeout occurred while getting default transcript for {video_id}")
                raise TimeoutException("Timeout while getting transcript")
            
        except Exception as e:
            print(f"Error getting default language transcript for {video_id}: {str(e)}")
            raise RuntimeError(f"Transcript indisponible : {str(e)}")
    except Exception as e:
        print(f"Error getting transcript for {video_id}: {str(e)}")
        raise RuntimeError(f"Erreur transcript : {str(e)}")
