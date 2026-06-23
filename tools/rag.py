"""
RAG: Build a ChromaDB vector store for menu items 

The vector store is created once at import time and re-used by the 
search_menu_catalog and get_order_status tools.
"""
from langchain_chroma import Chroma
from langchain_core.documents import Document

from snackstack.config import embeddings, get_logger
from data.menu import MENU_ITEMS

logger = get_logger("rag")

def _build_documents() -> list[Document]:
    """Convert every menu item into a langchain Document."""
    docs: list[Document] = []
    for m in MENU_ITEMS:
        content = (
            f"Item: {m['name']}, Category: {m['category']}, Cuisine: {m['cuisine']}, Price: {m['price']}, Rating: {m['rating']}, Dietary Tags: {', '.join(m['dietary_tags'])}, Description: {m['description']}"
        )
        doc = Document(
            page_content=content, 
            metadata={
                "id": m["id"], 
                "name": m["name"], 
                "category": m["category"],
                "price": m["price"],
                "rating": m["rating"]
                })
        docs.append(doc)
    return docs

def build_vector_store() -> Chroma:
    """Build an in-memory ChromaDB vector store for the menu items."""
    docs = _build_documents()
    store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="menu_items",
    )
    logger.info("Vector store ready  (%d items indexed)", len(docs))
    return store

# Module level singleton so every importer shares the same store
menu_vectorstore = build_vector_store()