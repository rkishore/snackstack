"""
Quick manual test for order_agent.

Usage:
    uv run python scripts/try_order_agent.py "status of ORD201?"
    uv run python scripts/try_order_agent.py "hi"     # greeting → no tool call
    uv run python scripts/try_order_agent.py          # uses a default query

Calls the node in isolation (no full graph) and prints the synthesizer-bound result.
Requires OPENAI_API_KEY — the LLM and the get_order_status tool run for real.
"""

import sys

from agents.order_agent import order_agent
from snackstack.state import AgentTask

query = " ".join(sys.argv[1:]) or "status of ORD201?"

state = {
    "user_query": query,
    "tasks": [AgentTask(agent="order_agent", task_description=query)],
    "messages": [],
}

cmd = order_agent(state)

print("query  :", query)
print("goto   :", cmd.goto)
for result in cmd.update["agent_results"]:
    print("source :", result["source"])
    print("answer :", result["response"])
