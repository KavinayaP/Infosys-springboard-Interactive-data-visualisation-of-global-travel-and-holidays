# backend/voice.py

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


router = APIRouter(prefix="/api/voice", tags=["Voice Assistant"])

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("⚠️ OPENAI_API_KEY missing — Voice Assistant in DEMO mode.")
    client = None
else:
    client = OpenAI(api_key=API_KEY)      # ✅ Correct: pass API key here


# ---------------- SPEECH → TEXT ----------------

@router.post("/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    if not client:
        return {"text": "Demo: Voice-to-text available only after API key."}

    try:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-tts",
            file=audio.file
        )
        return {"text": transcript.text}

    except Exception as e:
        raise HTTPException(500, f"STT Error: {str(e)}")


# ---------------- TEXT → SPEECH ----------------

@router.post("/tts")
async def text_to_speech(text: str):
    if not client:
        raise HTTPException(400, "Voice TTS disabled. No API key set.")

    try:
        audio = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )
        return StreamingResponse(audio, media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(500, f"TTS Error: {str(e)}")
