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

### Notes for recent updates (important)

- Fixed a bug in the agent where calling the /agent/chat route could raise a KeyError when the agent was invoked with a plain question and no chat `messages` history. The agent now gracefully falls back to using the provided `question` when a `messages` list is not present.
- The input guardrail signature was simplified to accept a single question string (instead of expecting a list/different parameter), and the agent nodes were updated to support both chat-history and question-only invocation.

These changes make the API robust when the frontend (or any client) sends a single question to the agent.

### 3. Setup Frontend

```bash
cd math-chat-ui
npm install
npm run dev
```

### Running backend tests (new)

There are unit tests added for some of the LLM agent nodes (to avoid calling external services these tests stub functions). Run them from the `backend` folder.

Windows (cmd.exe)
```cmd
cd /d path\to\MathMind-Agent\backend
venv\Scripts\activate
python -m pytest tests/test_agent_nodes.py
```

If you created your environment as `.venv` instead of `venv` use the `.venv` path:
```cmd
cd /d path\to\MathMind-Agent\backend
.venv\Scripts\activate
python -m pytest tests/test_agent_nodes.py
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

✅ Recent bugfixes: KeyError on missing `messages` has been fixed and agent nodes are now robust to question-only invocations.

⚠️ Auto-learning feature is work in progress.

