import asyncio
import sys
import os

# Ensure tests can import the package when run directly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from math_agent.llm import agent, guardrails, kb_loader, mcp_servers


async def test_input_guardrail_with_question_only():
    # stub the guardrail to avoid calling external LLM
    orig = guardrails.run_input_guardrails
    guardrails.run_input_guardrails = lambda q: True
    try:
        state = {"question": "What is 2 + 2?"}
        new_state = await agent.input_guardrail_node(state)
        assert isinstance(new_state, dict)
        assert new_state.get("is_safe") is True
    finally:
        guardrails.run_input_guardrails = orig


async def test_context_gathering_fallbacks():
    # stub the kb and web search functions
    orig_kb = kb_loader.search_knowledge_base
    orig_web = mcp_servers.search_web_mcp
    kb_loader.search_knowledge_base = lambda q, top_k=3: ["kb result"]
    mcp_servers.search_web_mcp = lambda q: ["web result"]
    try:
        state = {"question": "Integrate x^2"}
        result = await agent.context_gathering_node(state)
        assert isinstance(result, dict)
        assert "raw_information_on_question" in result
    finally:
        kb_loader.search_knowledge_base = orig_kb
        mcp_servers.search_web_mcp = orig_web


def run_tests():
    asyncio.run(test_input_guardrail_with_question_only(__import__('pytest').MonkeyPatch()))
    asyncio.run(test_context_gathering_fallbacks(__import__('pytest').MonkeyPatch()))


if __name__ == '__main__':
    run_tests()
