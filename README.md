# MathMind-Agent

Smart math assistant with auto-learning capabilities.

## What It Does

- Answers math questions
- Learns from user feedback
- Interactive chat interface

## Tech Stack

- **Backend**: Python, FastAPI, LangGraph, Qdrant
- **Frontend**: React, Vite

## How to Run

### 1. Start Qdrant Database

```bash
docker volume create qdrant_storage
docker run -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file in `backend/` folder (copy from `.env.development` and add your API keys).

```bash
uvicorn main:app --reload
```

### 3. Setup Frontend

```bash
cd math-chat-ui
npm install
npm run dev
```

## File Structure

### Backend (`backend/`)

- `main.py` – FastAPI entrypoint
- `core/` – shared config
- `math_agent/` – agents, routers, LLM logic
- `requirements.txt`

### Frontend (`math-chat-ui/`)

- `src/main.jsx` – React bootstrap
- `src/components/` – chat UI pieces
- `src/pages/MathChat.jsx` – main chat page
- `src/services/api.js` – API client
- `public/` – static assets

## Status

⚠️ Auto-learning feature is work in progress.

