# backend/chat.py

import os
import time
from typing import List, Optional
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# ---------------- LOAD ENV -----------------
load_dotenv()

router = APIRouter(prefix="/api", tags=["Chatbot"])

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY) if API_KEY else None


# ---------------- REQUEST MODELS -----------------

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    reply: str


# ---------------- RATE LIMIT -----------------
RATE_LIMIT = 10  # per minute
RATE_DATA = {}

def rate_limit(ip: str):
    now = int(time.time())
    timestamps = [t for t in RATE_DATA.get(ip, []) if now - t < 60]
    timestamps.append(now)
    RATE_DATA[ip] = timestamps
    return len(timestamps) <= RATE_LIMIT


# ---------------- CHAT ENDPOINT -----------------

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, request: Request):

    ip = request.client.host

    if not rate_limit(ip):
        raise HTTPException(429, "Too many messages. Slow down.")

    user_msg = req.message.strip()
    if not user_msg:
        raise HTTPException(400, "Message cannot be empty.")

    # Start messages list
    messages = [
        {
            "role": "system",
            "content": "You are Global Travel Insights AI assistant. Answer clearly."
        }
    ]

    # Add valid history
    if req.history:
        for h in req.history:
            messages.append({"role": h.role, "content": h.content})

    # Add the latest user message
    messages.append({"role": "user", "content": user_msg})


    # DEMO MODE (no API key)
    if not client:
        return {"reply": "Demo mode active. Add API key to enable real chatbot."}

    # REAL OPENAI CALL
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=300
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(500, f"LLM Error: {str(e)}")
