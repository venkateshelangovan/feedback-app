import os
import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import SessionLocal, FeedbackDB

# Setup paths for static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

app = FastAPI(title="Feedback API")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class FeedbackCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    rating: int = Field(..., ge=1, le=5)
    experience: str = Field(..., min_length=5)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def send_telegram_notification(feedback: FeedbackCreate):
    # Force reload environment variables path relative to this file
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    load_dotenv(dotenv_path=env_path, override=True)

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Clean quotes if any (some versions of dotenv or environments preserve them)
    if token: token = token.strip('"').strip("'")
    if chat_id: chat_id = chat_id.strip('"').strip("'")

    if not token or not chat_id or "YOUR_BOT_TOKEN" in token:
        print(f"Telegram configuration missing. Path: {env_path}, Exists: {os.path.exists(env_path)}")
        print(f"DEBUG: Token loaded: {bool(token)}, Chat ID loaded: {bool(chat_id)}")
        return

    message = (
        "🚀 <b>New Feedback Received!</b>\n\n"
        f"👤 <b>Name:</b> {feedback.name}\n"
        f"📧 <b>Email:</b> {feedback.email}\n"
        f"⭐ <b>Rating:</b> {feedback.rating}/5\n"
        f"💬 <b>Experience:</b> {feedback.experience}"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                print(f"Telegram API Error: {response.status_code} - {response.text}")
            response.raise_for_status()
            print("Telegram notification sent successfully!")
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")

@app.post("/submit-feedback")
async def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    try:
        # Save to Database
        db_feedback = FeedbackDB(
            name=feedback.name,
            email=feedback.email,
            rating=feedback.rating,
            experience=feedback.experience
        )
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)

        # Send Telegram Notification
        await send_telegram_notification(feedback)

        return {"status": "success", "message": "Feedback submitted successfully!"}
    except Exception as e:
        print(f"Error in submit_feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount Static Files (Frontend) at Root
# This must be the last route defined to avoid overriding /submit-feedback
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
