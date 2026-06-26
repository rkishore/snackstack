"""
Build and compile the SnackStack StateGraph.

Graph topology:

  START → orchestrator ─┬─ menu_agent ──→ synthesizer → END
                        └─ order_agent ──↗
"""
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from snackstack.config import get_logger
from agents.menu_agent import menu_agent
from agents.order_agent import order_agent
from agents.orchestrator import orchestrator_node
from agents.synthesizer import synthesizer_agent
from snackstack.state import SnackStackState

logger = get_logger("graph")

"""
create a StateGraph(StackState), add all nodes, add edges (START -> orchestrator, final node -> END)
(Optional) The orchestrator uses Command + Send() to dispatch to agents in parallel. 
Alternatively, route to one agent at a time using conditional edges
Compile with MemorySaver checkpointer for multi-turn conversation memory
Verify: invoke the graph with a test query and check the final_answer in the result
"""
def build_graph() -> StateGraph:
    
    # ── Add nodes ────────────────────────────────────────
    builder = StateGraph(SnackStackState)
    
    # ── Add edges ────────────────────────────────────────
    builder.add_node("orchestrator", orchestrator_node)
    builder.add_node("menu_agent", menu_agent)
    builder.add_node("order_agent", order_agent)
    builder.add_node("synthesizer_node", synthesizer_agent)

    # ── Add edges ────────────────────────────────────────
    # menu_agent / order_agent route to synthesizer_node themselves via
    # Command(goto=...), so no static edges are needed from them.
    builder.add_edge(START, "orchestrator")
    builder.add_edge("synthesizer_node", END)

    # ── Compile with checkpointer ────────────────────────
    # MemorySaver persists graph state so that interrupt()-based
    # HITL can pause and resume, and conversation history carries
    # forward between queries.
    checkpointer = MemorySaver()
    compiled_graph = builder.compile(checkpointer=checkpointer)

    logger.info("Graph compiled  (with MemorySaver for conversation persistence)")
    return compiled_graph

# Module-level singleton
snackstack_graph = build_graph()