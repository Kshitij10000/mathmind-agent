# backend\main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from math_agent.routers import router
app = FastAPI(
    title = 'MathMind-Agent',
    description = 'MathMind-Agent is an intelligent mathematics learning assistant that uses advanced AI to help users understand and solve mathematical problems. The agent features automatic learning capabilities, making it smarter over time as it interacts with users and processes mathematical concepts.',
    version = '0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Your Vite dev server URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get('/', tags=['Root'])
async def root():
    return {'message': 'Welcome to MathMind-Agent'}

app.include_router(router)