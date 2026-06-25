"""
Synthesizer agent for combining and presenting the results from other agents.
"""

from __future__ import annotations

from snackstack.logger import get_logger
from snackstack.state import SnackStackState 
from snackstack.config import llm

from agents.prompts import get_synthesizer_sys_prompt

logger = get_logger(__name__)

def synthesizer_agent(state: SnackStackState) -> dict:
    """Merge results from one or more agents into a single user-facing reply."""
    logger.info(f"Synthesizing results for state: {state}")
    results = state.get("agent_results", [])
    user_query = state.get("user_query", "")

    if not results:
        logger.info(f"No results to synthesize for query: {user_query}")
        return {"final_answer": "Sorry, I couldn't process that request. Please try again."}

    if len(results) == 1:
        logger.info(f"Single result found for query: {user_query}")
        return {"final_answer": results[0]["response"]}

    logger.info(f"Multiple results found for query: {user_query}")

    parts = "\n\n".join(
        f"[{r['source'].upper()}]:\n{r['response']}" for r in results
    )

    prompt = get_synthesizer_sys_prompt(user_query, parts)
    merged = llm.invoke(prompt)
    
    return {"final_answer": merged.content}