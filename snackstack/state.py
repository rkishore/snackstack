"""
Langgraph state management for the snackstack application.

SnackStackState         – the main graph state shared by all nodes.
WorkerInput             – the input data for each worker node.
AgentTask               – the task data for each agent node.
ClassificationResult    – the result of each classification task.
"""

#from __future__ import annotations

import operator
from typing import Annotated, List, Literal, TypedDict

from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field

def agent_results_reducer(current: list[dict], update: list[dict]) -> list[dict]:
    """Like operator.add but empty update signals reset."""
    if not update:
        return []
    return current + update

class AgentTask(BaseModel):
    """A Single task assigned to a specialized agent."""

    agent: Literal["menu_agent", "order_agent"] = Field(
        description="Which agent handles this task." 
    )

    task_description: str = Field(
        description="What the agent should do."
    )

class ClassificationResult(BaseModel):
    """The result of a classification task."""

    tasks: List[AgentTask] = Field(description="The list of tasks to dispatch.")
    requires_synthesis: bool = Field(
        description="True when the output from multiple agents needs to be merged."
    )
    reasoning: str = Field(
        description="Brief explanation of the routing result."
    )

class SnackStackState(TypedDict):
    """The main graph state shared by all nodes."""

    # Conversation state
    messages: Annotated[List[AnyMessage], operator.add]
    user_query: str

    # Routing
    tasks: List[AgentTask]
    reasoning: str
    requires_synthesis: bool

    # --- Specialist agent outputs ----
    menu_response: str
    order_response: str

    # Collected results
    #agent_results: Annotated[list[dict], agent_results_reducer]

    # Final response returned to the user
    final_answer: str 

'''
class WorkerInput(TypedDict):
    """Payload delivered to an agent worker node via Send().

    NOTE: This is intentionally flat; no nested Pydantic objects;
    so that Send() serialisation works without surprises.
    """

    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    task_description: str
'''


