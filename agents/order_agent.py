"""
Order agent for handling order-related operations.
"""

from __future__ import annotations

from typing import Literal

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.types import Command

from snackstack.logger import get_logger
from snackstack.state import SnackStackState 
from snackstack.config import llm

from tools.order_tools import get_order_status
from agents.utils import build_context, get_task_description

from agents.prompts import ORDER_AGENT_SYS_PROMPT

logger = get_logger(__name__)

# ── Tool bindings ────────────────────────────────────────────
order_tools = [get_order_status]
order_tool_map = {t.name: t for t in order_tools}
order_llm = llm.bind_tools(order_tools)

MAX_TOOL_ITERATIONS = 5

def order_agent(state: SnackStackState) -> Command[Literal["synthesizer"]]:
    """
    Handle order-related operations and return a command to the synthesizer.
    """
    user_query = state.get("user_query", "")
    task_desc = get_task_description(state, "order_agent")
    logger.info(f"User query: {user_query}")
    logger.info(f"order_agent  query:{user_query!r}, task: {task_desc!r}")

    context = build_context(state.get("messages", []))

    messages: list[AnyMessage] = [
        SystemMessage(content=ORDER_AGENT_SYS_PROMPT),
        HumanMessage(content=f"{context}\n\nTask: {task_desc}\nUser query: {user_query}")
    ]

    ai_msg: AIMessage | None = None
    for _ in range(MAX_TOOL_ITERATIONS):
        ai_msg = order_llm.invoke(messages)
        messages.append(ai_msg)
        if not ai_msg.tool_calls:
            break
        for tc in ai_msg.tool_calls:
            tool = order_tool_map.get(tc["name"])
            result = tool.invoke(tc["args"]) if tool else f"Unknown tool: {tc['name']}"
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

    answer = ai_msg.content if ai_msg and ai_msg.content else \
        "Sorry, I couldn't find that order."
        
    return Command(
        update={"agent_results": [{"source": "order_agent", "response": answer}]},
        goto="synthesizer"
    )
