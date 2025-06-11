from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import requests
from time import sleep
import socket
from urllib3.exceptions import ReadTimeoutError
import random

class TimeoutException(Exception):
    """Exception personnalisée pour gérer les timeouts"""
    pass

def get_random_user_agent():
    """Retourne un User-Agent aléatoire qui ressemble à un navigateur réel"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
    ]
    return random.choice(user_agents)

def check_video_status(video_id: str, proxies: dict = None) -> dict:
    """Vérifie le statut de la vidéo et les sous-titres disponibles"""
    try:
        # Démarrer un timer pour gérer le timeout
        socket.setdefaulttimeout(30)
        
        # Ajouter un délai aléatoire pour éviter le rate limiting
        sleep(random.uniform(1, 3))
        
        # Vérifier le statut de la vidéo via l'API YouTube
        url = f"https://www.youtube.com/get_video_info?video_id={video_id}"
        
        # En-têtes qui ressemblent davantage à un navigateur réel
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        
        print(f"Attempting to access YouTube API for video {video_id}")
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30, allow_redirects=False)
        
        if response.status_code == 410:
            raise RuntimeError("YouTube has blocked the request")
            
        if response.status_code == 429:
            raise RuntimeError("Too many requests")
            
        if response.status_code == 302:
            # Vérifier si nous sommes redirigés vers une page de captcha
            if "youtube.com/captcha" in response.headers.get('Location', ''):
                raise RuntimeError("Detected captcha page")
            
        if response.status_code != 200:
            raise RuntimeError(f"Failed to get video info: {response.status_code}")
            
        print(f"Successfully got video info")
        # Analyser la réponse pour vérifier le statut
        video_info = response.text
        print(f"Video info length: {len(video_info)}")
        
        if "status=fail" in video_info:
            raise RuntimeError("Video is not accessible")
            
        # Vérifier si les sous-titres sont disponibles
        if "has_transcript=true" not in video_info:
            raise RuntimeError("No transcript available for this video")
            
        return {
            "status": "ok",
            "has_transcript": True
        }
        
    except Exception as e:
        print(f"Error checking video status: {str(e)}")
        raise

def check_video_exists(video_id: str, proxies: dict = None) -> bool:
    try:
        # Vérifier si la vidéo existe en essayant d'accéder à sa page
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
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
        # Vérifier si il y a des sous-titres manuels ou générés
        return len(list(transcript_list)) > 0
    except Exception as e:
        print(f"Error checking transcript availability: {str(e)}")
        return False

def get_transcript(video_id: str, proxies: dict = None) -> str:
    try:
        print(f"Checking video status for {video_id}...")
        check_video_status(video_id, proxies)
        
        print(f"Checking if transcript is available for video {video_id}...")
        if not check_transcript_available(video_id, proxies):
            raise RuntimeError("No transcript available for this video")
            
        # Essai 1 : en français
        print(f"Attempting to get transcript for video {video_id} in French")
        try:
            # Ajouter un délai aléatoire pour éviter le rate limiting
            sleep(random.uniform(1, 3))
            
            # Utiliser un User-Agent aléatoire
            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept': 'application/json',
                'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                'Connection': 'keep-alive',
            }
            
            # Démarrer un timer pour gérer le timeout
            socket.setdefaulttimeout(30)
            
            # Créer une session pour maintenir les cookies
            session = requests.Session()
            session.headers.update(headers)
            
            # Faire une requête initiale pour obtenir les cookies
            session.get('https://www.youtube.com', proxies=proxies, timeout=30)
            
            # Utiliser la session avec les cookies pour la requête de transcript
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=["fr"],
                proxies=proxies,
                http_client=session
            )
            print(f"Successfully got French transcript for video {video_id}")
            return " ".join([t["text"] for t in transcript])
        except NoTranscriptFound:
            print(f"No French transcript found for video {video_id}, trying default language")
            # Essai 2 : sans langue précisée = langue par défaut (souvent originale)
            try:
                # Ajouter un délai supplémentaire
                sleep(random.uniform(2, 4))
                
                # Utiliser la même session avec les cookies
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    proxies=proxies,
                    http_client=session
                )
                print(f"Successfully got default language transcript for video {video_id}")
                return " ".join([t["text"] for t in transcript])
            except Exception as e:
                print(f"Error getting default language transcript for {video_id}: {str(e)}")
                raise RuntimeError(f"Transcript indisponible : {str(e)}")
    except Exception as e:
        print(f"Error getting transcript for {video_id}: {str(e)}")
        raise RuntimeError(f"Erreur transcript : {str(e)}")
