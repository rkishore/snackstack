"""
Menu agent for handling menu-related operations.
"""
from __future__ import annotations
from typing import Literal

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.types import Command

from snackstack.logger import get_logger
from snackstack.state import SnackStackState 
from snackstack.config import llm
from tools.menu_tools import search_menu_catalog

from agents.prompts import MENU_AGENT_SYS_PROMPT
from agents.utils import build_context, get_task_description

logger = get_logger(__name__)

# ── Tool bindings ────────────────────────────────────────────
menu_tools = [search_menu_catalog]
menu_tool_map = {t.name: t for t in menu_tools}
menu_llm = llm.bind_tools(menu_tools)

MAX_TOOL_ITERATIONS = 5

def menu_agent(state: SnackStackState) -> Command[Literal["synthesizer"]]:
    """
    Handle menu-related operations and return a command to the synthesizer.
    """
    user_query = state.get("user_query", "")
    task_desc = get_task_description(state, "menu_agent")
    logger.info(f"User query: {user_query}")
    logger.info(f"menu_agent  query:{user_query!r}, task: {task_desc!r}")

    context = build_context(state.get("messages", []))

    messages: list[AnyMessage] = [
        SystemMessage(content=MENU_AGENT_SYS_PROMPT),
        HumanMessage(content=f"{context}\n\nTask: {task_desc}\nUser query: {user_query}")
    ]

    ai_msg: AIMessage | None = None
    for _ in range(MAX_TOOL_ITERATIONS):
        ai_msg = menu_llm.invoke(messages)
        messages.append(ai_msg)
        if not ai_msg.tool_calls:
            break
        for tc in ai_msg.tool_calls:
            tool = menu_tool_map.get(tc["name"])
            result = tool.invoke(tc["args"]) if tool else f"Unknown tool: {tc['name']}"
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

    answer = ai_msg.content if ai_msg and ai_msg.content else \
        "Sorry, I couldn't find that on our menu right now."
        
    return Command(
        update={"agent_results": [{"source": "menu_agent", "response": answer}]},
        goto="synthesizer"
    )
