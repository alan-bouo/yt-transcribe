from fastapi import FastAPI, HTTPException, Query
from app.transcript import get_transcript

app = FastAPI(title="YouTube Transcript API")

@app.get("/transcript")
def transcript(
    video_id: str = Query(..., description="ID de la vidéo YouTube"),
    proxy_username: str = Query(None, description="Nom d'utilisateur du proxy"),
    proxy_password: str = Query(None, description="Mot de passe du proxy"),
    proxy_host: str = Query(None, description="Hôte du proxy"),
    proxy_port: int = Query(None, description="Port du proxy")
):
    proxies = None
    if all([proxy_username, proxy_password, proxy_host, proxy_port]):
        proxies = {
            "http": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
            "https": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
        }
    
    try:
        text = get_transcript(video_id, proxies=proxies)
        return {"video_id": video_id, "transcript": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))