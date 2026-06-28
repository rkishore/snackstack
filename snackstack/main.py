"""Console entry point for the snackstack application."""

import argparse
import uuid

from langgraph.types import Command
from langchain_core.messages import HumanMessage
from snackstack.graph import snackstack_graph
from snackstack.logger import get_logger
from voice.recorder import VoiceRecorder
from voice.speaker import VoiceSpeaker

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
        
        while True:
            intrs = self.graph.get_state(self._config).interrupts
            if not intrs:
                break
            answer = input(f"Snackstack: {intrs[0].value}\nYou: ").strip()
            result = self.graph.invoke(Command(resume=answer), config=self._config)
        
        return result.get("final_answer", "No answer available")

    def reset(self) -> None:
        self.thread_id = f"cli-session-{uuid.uuid4().hex[:8]}"

def _handle_input(assistant: SnackStackAssistant, user_input: str, speaker: VoiceSpeaker = None):
    result = assistant.ask(user_input)
    print(f"Snackstack: {result}")
    if speaker:
        speaker.speak(result)   

def run_text_loop(assistant: SnackStackAssistant, speaker: VoiceSpeaker = None):
    print("Snackstack - ask about the menu or your order. ('reset' to clear, 'quit' to exit).")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"quit", "exit", "bye"}:
            break
        if not user_input:
            continue
        if user_input.lower() == "reset":
            assistant.reset()
            print("Snackstack: conversation reset.")
            continue

        logger.info(f"User input: {user_input}")
        _handle_input(assistant, user_input, speaker)

def run_voice_loop(assistant: SnackStackAssistant, recorder: VoiceRecorder, speaker: VoiceSpeaker = None):
    print("Snackstack - ask about the menu or your order. ('reset' to clear, 'quit' to exit).")
    while True:
        cmd = input("\n[Enter] to speak: ").strip().lower()
        if cmd in {"quit", "exit", "bye"}:
            break
        if cmd == "reset":
            assistant.reset()
            print("Snackstack: conversation reset.")
            continue
        _, user_input = recorder.record_and_transcribe()
        print(f"You said: {user_input}")
        if not user_input.strip():
            print("Snackstack: heard nothing - try again.")
            continue

        _handle_input(assistant, user_input, speaker)

def main() -> int:
    """Run the snackstack application.
    
    Wired to the `snackstack` command via [project.scripts] in pyproject.toml.
    Returns an exit code (0 = success)
    """
    parser = argparse.ArgumentParser(description="Snackstack - ask about the menu or your order.")
    parser.add_argument("--thread-id", default="cli-session-1", help="The thread ID for the conversation.")
    parser.add_argument("--voice", action="store_true", help="record spoken input (microphone + Whisper).")
    parser.add_argument("--voice-out", action="store_true", help="speak responses (OpenAI TTS).")
    args = parser.parse_args()

    recorder = VoiceRecorder() if args.voice else None
    speaker = VoiceSpeaker() if args.voice_out else None
    assistant = SnackStackAssistant(thread_id=args.thread_id)
    
    if args.voice:
        run_voice_loop(assistant, recorder, speaker)
    else:
        run_text_loop(assistant, speaker)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
