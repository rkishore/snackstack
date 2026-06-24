"""
Quick manual test for orchestrator_node.

Usage:
    uv run python scripts/try_orchestrator.py "where is my order ORD101?"
    uv run python scripts/try_orchestrator.py        # uses a default query

Calls the node in isolation (no full graph) and prints the routing decision.
Requires OPENAI_API_KEY — the classifier LLM runs for real.
"""

import sys

from agents.orchestrator import orchestrator_node

query = " ".join(sys.argv[1:]) or "hello"
cmd = orchestrator_node({"user_query": query})

print("query :", query)
print("goto  :", cmd.goto)
print("tasks :", [(t.agent, t.task_description) for t in cmd.update["tasks"]])
print("synth :", cmd.update["requires_synthesis"])
print("reason:", cmd.update["reasoning"])
