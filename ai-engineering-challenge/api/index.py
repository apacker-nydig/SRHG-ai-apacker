from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS so the frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_AUTH_TOKEN"),
    base_url=os.getenv("ANTHROPIC_BASE_URL")
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    if not os.getenv("ANTHROPIC_AUTH_TOKEN"):
        raise HTTPException(status_code=500, detail="ANTHROPIC_AUTH_TOKEN not configured")

    try:
        user_message = request.message
        response = client.messages.create(
            model="claude-haiku-4-5-20250929",
            max_tokens=1024,
            system="You are a practical assistant. Answer only what was asked in natural prose—no extra context, explanations, alternatives, or advice unless requested. Keep responses minimal by default. When you cannot do something, state the limitation and stop; do not offer workarounds or explain how to do it manually. Decline creative writing and entertainment requests. Avoid structured formatting (headers, bullets) unless requested. No preambles.",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return {"reply": response.content[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Anthropic API: {str(e)}")
