from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import models, schemas, auth, database
import os
import requests
from dotenv import load_dotenv

# Robustly load the .env from the root directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, "../.env"))

router = APIRouter(prefix="/api/chat", tags=["chat"])

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("VITE_GROQ_API_KEY")

@router.post("", response_model=schemas.ChatResponse)
async def chat_with_bot(request: schemas.ChatRequest, current_user: Optional[models.User] = Depends(auth.get_optional_current_user), db: Session = Depends(database.get_db)):
    # If key is missing, return immediately
    if not GROQ_API_KEY:
        return {"text": "AI Service configuration missing. Please ensure VITE_GROQ_API_KEY is set in your .env file."}
    # 1. Get response from Groq
    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": os.getenv("VITE_GROQ_MODEL", "llama-3.3-70b-versatile"),
                "messages": [
                    {
                        "role": "system", 
                        "content": f"You are SUDARSHAN GRID, a helpful AI assistant specialized in Indian government schemes. "
                                   f"IMPORTANT: You MUST respond in { 'Hindi' if request.language == 'hi' else 'English' }. "
                                   f"The user has selected { 'Hindi' if request.language == 'hi' else 'English' } as their preferred language. "
                                   "Stay professional, helpful, and concise."
                    },
                    *request.messages
                ]
            },
            timeout=30
        )
        response.raise_for_status()
        bot_text = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq API Error: {e}")
        bot_text = "I'm sorry, I'm having trouble connecting to the AI service."

    return {
        "text": bot_text
    }
