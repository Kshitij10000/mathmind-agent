# backend\math_agent\llm\agent.py
from typing import TypedDict, Literal, List, Annotated
from math_agent.llm.services import generate_solution 
from math_agent.llm.guardrails import run_input_guardrails, run_output_guardrail
from math_agent.llm.kb_loader import search_knowledge_base , add_to_knowledge_base
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage
from math_agent.llm.mcp_servers import search_web_mcp
import asyncio
#1. Define the Agent's State
# This is the "memory" that flows between nodes
class AgentState(TypedDict, total=False):
    # messages might be present if the caller passes a chat history
    messages: Annotated[List[BaseMessage], "Chat history"]
    is_safe: bool 
    question: str 
    raw_information_on_question: str
    context: str 
    image_prompt: str
    image_url: str
    answer: str 


# Step 2 Define the Agent's Nodes
# Each node is a function that modifies the state.

async def input_guardrail_node(state: AgentState):
    """
    Runs the input guardrails check.
    Logic:
    - If it's a new chat, check just the question.
    - If it's a history, check the last few messages to understand context.
    """
    messages = state.get("messages", [])
    
    # 1. Extract the specific text to check
    if len(messages) > 0:
        # Get the very last message (the user's current input)
        latest_message = messages[-1]
        user_input = latest_message.content if hasattr(latest_message, "content") else str(latest_message)
        
        # 2. Construct Context for the Guardrail
        # If we have history, send the last 3 messages so the guardrail understands "Why?"
        if len(messages) > 1:
            # Get last 3 messages (e.g., User -> AI -> User)
            context_window = messages[-3:] 
            # Convert list of messages to a string conversation
            conversation_str = "\n".join([f"{type(m).__name__}: {m.content}" for m in context_window])
            text_to_check = f"CONTEXT:\n{conversation_str}\n\nCURRENT QUESTION: {user_input}"
        else:
            # First message ever
            text_to_check = user_input
            
    else:
        # Fallback if state has no messages (shouldn't happen with correct API call)
        user_input = state.get("question", "")
        text_to_check = user_input

    # 3. Save the *actual* user question to state for later nodes to use
    state["question"] = user_input

    # 4. Run the check
    print(f"[Guardrail] Checking: {text_to_check[:100]}...") # Print first 100 chars
    is_safe = run_input_guardrails(text_to_check)

    print(f"[Guardrail] Result: {is_safe}")
    
    # Return updated state
    return {"is_safe": is_safe, "question": user_input}

async def context_gathering_node(state: AgentState):
    """
    Simpler, cleaner logic: Just grab the last message.
    """
    messages = state.get("messages", [])
    
    # Safety check: Should generally not happen if API is correct
    if not messages:
        print("[Context] Error: No messages found in state.")
        return {"raw_information_on_question": "No context."}

    # 1. Get the latest question directly
    latest_message = messages[-1]
    question_text = latest_message.content
    
    # 2. Safety check for empty strings
    if not question_text or not question_text.strip():
        return {"raw_information_on_question": "No context (empty question)."}

    # 3. Proceed with search
    print(f"[Context] Gathering info for: '{question_text}'")
    
    kb_task = search_knowledge_base(question_text, top_k=3)
    web_task = search_web_mcp(question_text)
    
    kb_results, web_res = await asyncio.gather(kb_task, web_task)
    
    full_context = f"---Knowledge Base Results: {kb_results}\n ---Web Search Results: {web_res}"
    return {"raw_information_on_question": full_context}

def generate_solution_node(state: AgentState):
    """ generates the final answer based on context"""
    question = state["question"]
    context = state["raw_information_on_question"]
    answer = generate_solution(question, context)
    return {"answer": answer}


async def output_guardrail_node(state: AgentState):
    """run the output guardrail check"""
    answer = state["answer"]
    is_valid = run_output_guardrail(answer)
    if not is_valid:
        return {
            "answer": "I'm sorry, I was unable to generate a valid solution for this problem."
        }
    return {}


# def human_in_loop_node(state: AgentState):
#     """
#     Human-in-the-loop interrupt node.
#     This node pauses the workflow to wait for human feedback.
#     The actual interruption is configured when compiling the graph.
#     """
#     # Pass through the state unchanged - the interrupt happens at the graph level
#     return {}


# async def self_learning_node(state: AgentState):
#     """
#     'Learns' the final human-approved answer by adding it to the KB.
#     """
#     print("[Self-Learning] Human feedback received. Adding to Knowledge Base...")
    
#     # Get the data from the state
#     question = state.get("question")
#     final_answer = state.get("final_answer") # Using the fixed 'final_answer' key

#     if question and final_answer:
#         # This is the "learning" step
#         await add_to_knowledge_base(question, final_answer)
#     else:
#         print("[Self-Learning] Skipping: Missing question or final_answer in state.")

#     return {}


# --- 3. Define the Graph's Edges (Conditional Logic) ---

def decide_if_valid(state: AgentState):
    """Checks the result of the input guardrail."""
    if state["is_safe"]:
        return "proceed"
    return "end_invalid"

# --- 4. Build the Graph ---
def build_math_agent():

    workflow = StateGraph(AgentState)

    # Add all the nodes
    workflow.add_node("input_guardrail", input_guardrail_node)
    workflow.add_node("context_gathering", context_gathering_node)
    workflow.add_node("generate_solution", generate_solution_node)
    workflow.add_node("output_guardrail", output_guardrail_node)
    # This node will PAUSE the graph for human feedback
    # workflow.add_node("human_in_loop", human_in_loop_node)
    # workflow.add_node("self_learning", self_learning_node)

    # --- 5. Wire the Nodes and Edges ---

    # start at gaurdrail
    workflow.set_entry_point("input_guardrail")

    # gaurdrail conditional edge
    workflow.add_conditional_edges(
        "input_guardrail",
        decide_if_valid,
        {
            "proceed": "context_gathering",
            "end_invalid": END
        }
    )
    # # After passing input guardrail, gather context
    # workflow.add_edge("input_guardrail", "context_gathering")
    # After gathering context, generate solution
    workflow.add_edge("context_gathering", "generate_solution")    
    # After generation , run the output guardrail
    workflow.add_edge("generate_solution", "output_guardrail")

    # # After the output guardrail, go to the human-in-loop
    # workflow.add_edge("output_guardrail", "human_in_loop")
    
    # # --- END OF CHANGES ---
    # # After the human provides feedback (resuming the graph),
    # # run the self-learning node
    # workflow.add_edge("human_in_loop", "self_learning")

    # End after learning
    workflow.add_edge("output_guardrail", END)

    # Compile the graph with a memory checkpointer
    # This is CRITICAL for pausing and resuming
    checkpointer = MemorySaver()
    # Configure interrupt before the human_in_loop node to pause for feedback
    app = workflow.compile(
        checkpointer=checkpointer,
        # interrupt_before=["human_in_loop"]
    )
    return app