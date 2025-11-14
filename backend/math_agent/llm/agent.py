# backend\math_agent\llm\agent.py
from typing import TypedDict, Literal
from math_agent.llm.services import generate_solution
from math_agent.llm.gaurdrails import run_input_gaurdrails, run_output_gaurdrail
from math_agent.llm.kb_loader import search_knowledge_base
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from math_agent.llm.mcp_servers import search_web_mcp

# --- 1. Define the Agent's State ---
# This is the "memory" that flows between nodes
class AgentState(TypedDict):
    question: str # user given question
    is_valid: bool # gaurdrail results
    route: Literal["kb","web"] # path choosen by the agent
    context: str # info found from web or kb
    answer: str # final answer
    final_answer: str # answer after human intervention    


# --- 2. Define the Agent's Nodes ---
# Each node is a function that modifies the state.

def input_gaurdrail_node(state: AgentState):
    """runs the input gaurdraials"""
    question = state["question"]
    is_valid = run_input_gaurdrails(question)
    return {"is_valid": is_valid}

async def router_node(state: AgentState):
    """Checks the KB to decide the route."""
    print("[Router] Checking Knowledge Base...")
    question = state["question"]
    
    # YOU MUST AWAIT THE ASYNC FUNCTION
    kb_results = await search_knowledge_base(question, top_k=1)

    if kb_results:
        print(f"[Router] Found {len(kb_results)} match(es) in KB.")
        # Pass the *content* of the result as context
        return {"route": "kb", "context": kb_results[0]['answer']}
    else:
        print("[Router] No match in KB. Routing to web.")
        return {"route": "web"}

async def web_search_node(state: AgentState):
    """Performs web search to get context"""
    question = state["question"]
    web_context = await search_web_mcp(question)
    return {"context": web_context}

def generate_solution_node(state: AgentState):
    """ generates the final answer based on context"""
    question = state["question"]
    context = state["context"]
    answer = generate_solution(question, context)
    return {"answer": answer}

def output_gaurdrail_node(state: AgentState):
    """run the output gaurdrail"""
    answer = state["answer"]
    is_valid = run_output_gaurdrail(answer)
    if not is_valid:
        return {
            "answer": "I'm sorry, I was unable to generate a valid solution for this problem."
        }
    return {}


def human_in_loop_node(state: AgentState):
    """
    Human-in-the-loop interrupt node.
    This node pauses the workflow to wait for human feedback.
    The actual interruption is configured when compiling the graph.
    """
    # Pass through the state unchanged - the interrupt happens at the graph level
    return {}

def self_learning_node(state: AgentState):
    """
    'Learns' the final human-approved answer.
    (This is where you'd add the 'final_answer' back to Qdrant)
    """
    print("[Self-Learning] Human feedback received. (Would add to KB here)")
    # In a real app, you'd call a function:
    # add_to_knowledge_base(state["question"], state["final_answer"])
    return {}

# --- 3. Define the Graph's Edges (Conditional Logic) ---

def decide_if_valid(state: AgentState):
    """Checks the result of the input guardrail."""
    if state["is_valid"]:
        return "proceed"
    return "end_invalid"

def decide_route(state: AgentState):
    """Checks the result of the router node."""
    return state["route"] # Returns "kb" or "web"

# --- 4. Build the Graph ---
def build_math_agent():

    workflow = StateGraph(AgentState)

    # Add all the nodes
    workflow.add_node("input_gaurdrail", input_gaurdrail_node)
    workflow.add_node("router", router_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("generate_solution", generate_solution_node)
    workflow.add_node("output_gaurdrail", output_gaurdrail_node)
    # This node will PAUSE the graph for human feedback
    workflow.add_node("human_in_loop", human_in_loop_node)
    workflow.add_node("self_learning", self_learning_node)

    # --- 5. Wire the Nodes and Edges ---

    # start at gaurdrail
    workflow.set_entry_point("input_gaurdrail")

    # gaurdrail conditional edge
    workflow.add_conditional_edges(
        "input_gaurdrail",
        decide_if_valid,
        {
            "proceed": "router",
            "end_invalid": END
        }
    )

    # Router conditional edge
    workflow.add_conditional_edges(
        "router",
        decide_route,
        {
            "kb": "generate_solution", # KB hits go straight to generation
            "web": "web_search"        # Web misses go to search first
        }
    )

    # Web search flows to generation
    workflow.add_edge("web_search", "generate_solution")
    
    # After generation , run the output gaurdrail
    workflow.add_edge("generate_solution", "output_gaurdrail")

    # After the output guardrail, go to the human-in-loop
    workflow.add_edge("output_gaurdrail", "human_in_loop")
    
    # --- END OF CHANGES ---
    # After the human provides feedback (resuming the graph),
    # run the self-learning node
    workflow.add_edge("human_in_loop", "self_learning")

    # End after learning
    workflow.add_edge("self_learning", END)

    # Compile the graph with a memory checkpointer
    # This is CRITICAL for pausing and resuming
    checkpointer = MemorySaver()
    # Configure interrupt before the human_in_loop node to pause for feedback
    app = workflow.compile(
        checkpointer=checkpointer,
        interrupt_before=["human_in_loop"]
    )
    return app