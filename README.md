# Feedback Form Web App with Telegram Integration

A minimalistic, modern full-stack feedback form built with FastAPI (Backend) and Vanilla JS (Frontend).

## Features
- **Modern UI**: Dark mode, glassmorphism, and star rating system.
- **FastAPI Backend**: Fast, asynchronous, and handles data validation.
- **SQLite Storage**: Feedback is saved locally in `feedback.db`.
- **Telegram Notifications**: Real-time alerts sent to your Telegram Bot.

---

## 🛠 Setup Instructions

### 1. Prerequisites
- Python 3.8+ installed.
- A Telegram account to create a bot.

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd feedback-app/backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Telegram (Optional but Recommended):
   - Message `@BotFather` on Telegram to create a bot and get your **API Token**.
   - Get your **Chat ID** (Message `@userinfobot` or check your bot's `getUpdates` URL).
   - Open `.env` and fill in your credentials:
     ```env
     TELEGRAM_BOT_TOKEN=123456...
     TELEGRAM_CHAT_ID=789012...
     ```

### 3. Run the Backend
Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
The server will be running at `http://localhost:8000`.

---

## 🌐 Frontend Setup
1. Simply open `feedback-app/frontend/index.html` in your web browser.
   - Or serve it using a simple HTTP server:
     ```bash
     cd feedback-app/frontend
     python -m http.server 3000
     ```

---

## 🚀 Deployment Steps (Render/Railway)

### Deployment on Render.com
1. **GitHub**: Push your code to a GitHub repository.
2. **New Web Service**: Connect your GitHub repo to Render.
3. **Runtime**: Python.
4. **Build Command**: `pip install -r backend/requirements.txt`.
5. **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
6. **Environment Variables**: Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in the Render dashboard.

---

## 📁 Project Structure
```text
feedback-app/
├── backend/
│   ├── main.py          # API Endpoints & Telegram logic
│   ├── database.py      # SQLite configuration
│   ├── requirements.txt # Dependencies
│   └── .env             # Bot credentials
├── frontend/
│   ├── index.html       # UI structure
│   ├── style.css        # Premium styles
│   └── script.js        # Form logic
```
