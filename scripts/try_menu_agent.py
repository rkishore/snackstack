"""
Quick manual test for menu_agent.

Usage:
    uv run python scripts/try_menu_agent.py "do you have any paneer dishes?"
    uv run python scripts/try_menu_agent.py "hi"     # greeting → no tool call
    uv run python scripts/try_menu_agent.py          # uses a default query

Calls the node in isolation (no full graph) and prints the synthesizer-bound result.
Requires OPENAI_API_KEY — the LLM and the search_menu_catalog tool run for real.
"""

import sys

from agents.menu_agent import menu_agent
from snackstack.state import AgentTask

query = " ".join(sys.argv[1:]) or "do you have any paneer dishes?"

state = {
    "user_query": query,
    "tasks": [AgentTask(agent="menu_agent", task_description=query)],
    "messages": [],
}

cmd = menu_agent(state)

print("query  :", query)
print("goto   :", cmd.goto)
for result in cmd.update["agent_results"]:
    print("source :", result["source"])
    print("answer :", result["response"])
