# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.transcript import get_transcript

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

@app.post("/transcript")
def transcript(req: TranscriptRequest):
    proxies = {
        "http": f"http://{req.proxy_username}:{req.proxy_password}@{req.proxy_host}:{req.proxy_port}",
        "https": f"http://{req.proxy_username}:{req.proxy_password}@{req.proxy_host}:{req.proxy_port}"
    }
    try:
        text = get_transcript(req.video_id, proxies=proxies)
        return {"video_id": req.video_id, "transcript": text}
    except Exception:
        raise HTTPException(status_code=400, detail="Erreur lors de la récupération du transcript.")
