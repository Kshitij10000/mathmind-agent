from fastapi import APIRouter
from pydantic import BaseModel
from math_agent.llm.agent import build_math_agent
import uuid

# Try to import GraphInterrupt, fall back to Exception if not available
try:
    from langgraph.errors import GraphInterrupt
except ImportError:
    # Fallback if GraphInterrupt is not available
    GraphInterrupt = Exception

router = APIRouter()
langgraph_app = build_math_agent()

#Define API request/response models
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    thread_id: str
    generated_answer: str

class FeedbackRequest(BaseModel):
    thread_id: str
    final_answer: str

@router.post("/agent/start")
async def start_agent_run(request: AskRequest):

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    print(f"Starting run for thread_id: {thread_id}")
    
    # Use ainvoke, not astream. 
    # ainvoke will run until the interrupt and return the state.
    try:
        # Pass the input dictionary
        final_state = await langgraph_app.ainvoke(
            {"question": request.question},
            config=config
        )
        
        # Check if the question was rejected by the guardrail
        if final_state.get("is_valid") is False:
            generated_answer = "I can only help with math questions. Please ask a math-related question."
        # If no interrupt and no answer, it might have finished for another reason
        elif "answer" not in final_state:
            generated_answer = "Graph finished without answer."
        else:
            generated_answer = final_state.get("answer", "Graph finished without answer.")

    except GraphInterrupt:
        # On interrupt, retrieve the snapshot from the checkpointer
        snapshot = langgraph_app.checkpointer.get(config)
        generated_answer = snapshot.values.get("answer", "Error: Paused but no answer found.")
    
    return AskResponse(
        thread_id=thread_id,
        generated_answer=generated_answer
    )

@router.post("/agent/resume")
async def resume_agent_run(request: FeedbackRequest):
    """
    RESUMES a paused agent run with human feedback.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    
    print(f"Resuming run for thread_id: {request.thread_id}")
    
    # This is correct. You 'resume' by invoking again with the
    # new state values. The checkpointer handles the rest.
    await langgraph_app.ainvoke(
        {"final_answer": request.final_answer},
        config=config
    )
    
    return {"status": "success", "message": "Feedback received. Agent learned."}