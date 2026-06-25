"""
Utility functions for the agents.
"""

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from snackstack.logger import get_logger
from snackstack.state import SnackStackState 

logger = get_logger(__name__)

def build_context(messages: list[AnyMessage]) -> str:
    """Format prior conversation turns as text for agent context"""
    if not messages:
        return ""
    
    parts = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            parts.append(f"Customer: {msg.content}")
        elif isinstance(msg, AIMessage):
            parts.append(f"Assistant: {msg.content}")
    
    if not parts:
        return ""

    return "CONVERSATION SO FAR:\n" + "\n".join(parts) + "\n\n"

def get_task_description(state: SnackStackState, agent_name: str) -> str:
    for task in state.get("tasks", []):
        if task.agent == agent_name:
            return task.task_description
    return ""
