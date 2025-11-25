# backend\math_agent\routers.py
from fastapi import APIRouter
from math_agent.api.agent_endpoints import router as agent_router

# Create a main router and include the agent router
router = APIRouter()

# Include the agent endpoints router (routes already have /agent prefix)
router.include_router(agent_router, tags=["Agent"])