"""Console entry point for the snackstack application."""

import argparse
import uuid

from langchain_core.messages import HumanMessage
from snackstack.graph import snackstack_graph
from snackstack.logger import get_logger

logger = get_logger(__name__)

class SnackStackAssistant:
    def __init__(self, thread_id: str = "cli-session-1"):
        self.graph = snackstack_graph
        self.thread_id = thread_id
    
    @property
    def _config(self):
        return {"configurable": {"thread_id": self.thread_id}}

    def ask(self, query: str):
        result = self.graph.invoke(
            {"user_query": query, "messages": [HumanMessage(content=query)]},
            config=self._config
        )
        # TODO: Interrupts code goes here.
        return result.get("final_answer", "No answer available")

    def reset(self) -> None:
        self.thread_id = f"cli-session-{uuid.uuid4().hex[:8]}"

def run_text_loop(assistant: SnackStackAssistant):
    print("Snackstack - ask about the menu or your order. ('reset' to clear, 'quit' to exit.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"quit", "exit", "bye"}:
            break
        if not user_input:
            continue
        if user_input.lower() == "reset":
            assistant.reset()
            print("Snakcstack: conversation reset.")
            continue

        logger.info(f"User input: {user_input}")
        result = assistant.ask(user_input)
        print(f"Snackstack: {result}")

def main() -> int:
    """Run the snackstack application.
    
    Wired to the `snackstack` command via [project.scripts] in pyproject.toml.
    Returns an exit code (0 = success)
    """
    parser = argparse.ArgumentParser(description="Snackstack - ask about the menu or your order.")
    parser.add_argument("--thread-id", default="cli-session-1", help="The thread ID for the conversation.")
    args = parser.parse_args()

    assistant = SnackStackAssistant(thread_id=args.thread_id)
    run_text_loop(assistant)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
