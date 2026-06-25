"""
Quick manual test for synthesizer_agent.

Usage:
    uv run python scripts/try_synthesizer.py          # runs all three cases
    uv run python scripts/try_synthesizer.py none     # no agent results  → fallback
    uv run python scripts/try_synthesizer.py single   # one result        → pass-through
    uv run python scripts/try_synthesizer.py multi     # two results       → LLM merge

Calls the node in isolation (no full graph) with a mock SnackStackState and
prints the resulting final_answer.

Only the 'multi' case calls the LLM (and so needs OPENAI_API_KEY); the 'none'
and 'single' cases are pure pass-through and run offline.
"""

import sys

from agents.synthesizer import synthesizer_agent

# Mock agent_results entries, shaped exactly like what menu_agent / order_agent emit.
ORDER_RESULT = {
    "source": "order_agent",
    "response": "Your order ORD-201 (Butter Chicken) is out for delivery, arriving today.",
}
MENU_RESULT = {
    "source": "menu_agent",
    "response": "Yes — we have Paneer Tikka and Paneer Butter Masala on the menu.",
}

CASES = {
    "none":   {"user_query": "where is my order?",                  "agent_results": []},
    "single": {"user_query": "where is my order?",                  "agent_results": [ORDER_RESULT]},
    "multi":  {"user_query": "any paneer dishes, and my order?",    "agent_results": [MENU_RESULT, ORDER_RESULT]},
}

selected = sys.argv[1:] or list(CASES)

for name in selected:
    state = CASES[name]
    print(f"\n=== case: {name} ===")
    print("query  :", state["user_query"])
    print("results:", [r["source"] for r in state["agent_results"]])
    out = synthesizer_agent(state)
    print("answer :", out.get("final_answer"))
