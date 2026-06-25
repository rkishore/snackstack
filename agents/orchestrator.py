"""
Orchestrator for handling customer queries and routing them to the appropriate agents.
"""

from __future__ import annotations

from typing import Literal
from langgraph.types import Command, Send

from snackstack.logger import get_logger
from snackstack.state import SnackStackState, ClassificationResult
from snackstack.config import llm
from agents.prompts import get_orchestrator_sys_prompt 

logger = get_logger(__name__)

# ═══════════════════════════════════════════════════════════
#  NODE 1 — Orchestrator
# ═══════════════════════════════════════════════════════════
def orchestrator_node(state: SnackStackState) -> Command[Literal["menu_agent", "order_agent", "synthesizer_node"]]:
    """
    Analyse the customer query and determine which agent(s) should handle it.
    """
    user_query = state.get("user_query", "")
    if not user_query and state.get("messages"):
        user_query = state["messages"][-1].content

    logger.info("Orchestrator  query=%r", user_query)

    prompt = get_orchestrator_sys_prompt(user_query)

    classifier = llm.with_structured_output(ClassificationResult)

    try:
        classification = classifier.invoke(prompt)
    except Exception:
        logger.exception("Classification failed — defaulting to menu_agent")
        classification = ClassificationResult(
            tasks=[], requires_synthesis=False,
            reasoning="Fallback: classification error",
        )

    logger.info("  routing=%s  synthesis=%s",
                [t.agent for t in classification.tasks],
                classification.requires_synthesis)
    
    return Command(
        goto=[t.agent for t in classification.tasks] or ["synthesizer_node"],
        update={
            "tasks": classification.tasks,
            "reasoning": classification.reasoning,
            "requires_synthesis": classification.requires_synthesis,
            "user_query": user_query,
            # "agent_results": [],  # reset stale results from prior turns
        },
    )

    '''
    targets: list[Send] = []
    for task in classification.tasks:
        targets.append(Send(agent=task.agent, {
            "messages": state.get("messages", []),
            "user_query": user_query,
            "task_description": task.task_description
        }))
    
    if not targets:
        target = [Send("synthesizer", {})]
    
    return Command(
        update={
            "tasks": classification.tasks,
            "requires_synthesis": classification.requires_synthesis,
            "user_query": user_query,
            "agent_results": [],  # reset stale results from prior turns
        },
        goto=targets,
    )
    '''