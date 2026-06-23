"""
Agent tools - the concrete actions agents can take

Menu Discovery (1 tool):
    - search_menu_catalog: Find menu items based on user queries (RAG semantic search)
"""

from __future__ import annotations

from langchain_core.tools import tool

from snackstack.logger import get_logger
from tools.rag import menu_vectorstore
from data.orders import ORDERS

logger = get_logger("menu_tools")

# ═══════════════════════════════════════════════════════════
#  MENU DISCOVERY TOOL
# ═══════════════════════════════════════════════════════════
@tool
def search_menu_catalog(query: str) -> str:
    """
    Search the Snackstack menu using Semantic search (RAG)

    Args:
        query: natural language search, e.g. "Paneer tikka masala"
    """
    logger.info(f"search_menu_catalog.  query: {query}")
    try:
        docs = menu_vectorstore.similarity_search(query, k=3)
        if not docs:
            return "No menu items matching your query"
        results = "Found the following menu items:\n\n"
        for i, doc in enumerate(docs, 1):
            results += f"Product {i}:\n{doc.page_content}\n\n"
        return results
    except Exception as exc:
        logger.exception("Menu catalog search failed")
        return f"Error searching menu: {exc}"
