# main.py
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.transcript import get_transcript
import os
from app.auth import is_token_valid, has_quota, update_quota  # 👈 Nouveau
import requests

app = FastAPI(title="YouTube Transcript API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptRequest(BaseModel):
    video_id: str
    proxy_username: str
    proxy_password: str
    proxy_host: str
    proxy_port: int

class TranscriptAuthRequest(BaseModel): 
    video_id: str

def notify_n8n(video_id: str, token: str):
    try:
        requests.post("https://n8n.alanbouo.com/webhook/transcript-event", json={
            "video_id": video_id,
            "token": token
        }, timeout=3)
    except Exception as e:
        print(f"Webhook error: {e}")


@app.post("/transcript")
def transcript(req: TranscriptRequest):
    proxies = {
        "http": f"http://{req.proxy_username}:{req.proxy_password}@{req.proxy_host}:{req.proxy_port}",
        "https": f"http://{req.proxy_username}:{req.proxy_password}@{req.proxy_host}:{req.proxy_port}"
    }
    try:
        text = get_transcript(req.video_id, proxies=proxies)
        notify_n8n(video_id=req.video_id, token="no-token")
        return {"video_id": req.video_id, "transcript": text}
    except Exception:
        raise HTTPException(status_code=400, detail="Erreur lors de la récupération du transcript.")

@app.post("/transcript/auth")
def transcript_with_auth(req: TranscriptAuthRequest, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token.")

    token = authorization.replace("Bearer ", "").strip()

    if not is_token_valid(token):
        raise HTTPException(status_code=401, detail="Invalid token.")

    if not has_quota(token):
        raise HTTPException(status_code=429, detail="Quota exceeded (1/day).")

    try:
        # Utilisation automatique du proxy résidentiel
        try:
            proxies = {
                "http": f"http://{os.environ['PROXY_USERNAME']}:{os.environ['PROXY_PASSWORD']}@{os.environ['PROXY_HOST']}:{os.environ['PROXY_PORT']}",
                "https": f"http://{os.environ['PROXY_USERNAME']}:{os.environ['PROXY_PASSWORD']}@{os.environ['PROXY_HOST']}:{os.environ['PROXY_PORT']}"
            }
        except KeyError:
            raise HTTPException(status_code=500, detail="Proxy configuration is missing.")
        text = get_transcript(req.video_id, proxies=proxies)
        update_quota(token)
        notify_n8n(video_id=req.video_id, token=token)
        return {"video_id": req.video_id, "transcript": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))