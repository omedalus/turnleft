import argparse
from dotenv import load_dotenv
from openai import OpenAI
from mightydatainc_llm_conversation import LLMConversation, JSONSchemaFormat

load_dotenv()

from mealyspace.session_manager import (
    CommandTarget,
    SessionCommand,
    SessionClient,
    SessionManager,
    SessionManagerCommand,
    SessionState,
    SessionStatus,
)


class LLMConvoClient(SessionClient):
    def __init__(self, ai_client: any, max_sessions: int) -> None:
        if max_sessions < 1:
            raise ValueError("max_sessions must be at least 1")

        self.max_sessions = max_sessions

        self.convo = LLMConversation(ai_client=ai_client)
        self.convo.add_system_message(
            "You are playing a single-player game. You will be given "
            "information about the game state, and you must choose "
            "actions that lead to a victory condition or at least "
            "avoid failure. Exploration, experimentation, and "
            "testing of hypotheses is strongly encouraged. "
            "You will be entirely alone during this play-through; "
            "you will be talking only to yourself, and will receive "
            "no guidance, advice, or feedback from the developer "
            "nor the user. If you want to try out an idea, don't ask them; "
            "they aren't listening. You're entirely on your own."
        )

        self.experience_log = ""

    def start(self) -> None:
        return None

    def render(self, state: SessionState) -> None:
        _ = state

    def get_command(self, state: SessionState) -> SessionCommand:
        s = ""
        if state.status is SessionStatus.RUNNING:
            s = "Game is currently running\n"

            s += "  Sensors:\n"
            for i, sensor_state in enumerate(state.sensors or []):
                s += f"    {i+1}: {sensor_state}\n"
            s += "  Actions available:\n"
            for i, action in enumerate(state.available_actions or []):
                s += f"    {i+1}: {action}\n"

        else:
            s = f"Game is not currently running.\n"
            s += f"  Outcome of last game: {state.status}\n"
            s += f"  Total successes so far: {state.success_count}\n"
            s += f"  Total failures so far: {state.failure_count}\n"
            s += "Game will begin automatically after this message.\n"

        print(s)
        self.convo.add_user_message(s)
        self.convo.submit_developer_message("Discuss your next move.")
        print(self.convo.get_last_reply_str())

        if state.status is not SessionStatus.RUNNING:
            return SessionCommand(
                CommandTarget.SESSION_MANAGER,
                SessionManagerCommand.BEGIN,
            )

        choose_action = self.convo.submit(
            json_response=JSONSchemaFormat({"action": int})
        )
        action_chosen = choose_action.get("action")
        print(f"Action chosen: {action_chosen}")

        return SessionCommand(CommandTarget.ENVIRONMENT, action_chosen)

    def show_error(self, message: str) -> None:
        raise RuntimeError(message)

    def stop(self) -> int:
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run automated Mealy Space sessions with an LLM that's given no explanation."
    )
    parser.add_argument(
        "sessions",
        type=int,
        nargs="?",
        default=100,
        help="Maximum number of sessions to run (default: 100).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session_manager = SessionManager()

    ai_client = OpenAI()
    client = LLMConvoClient(ai_client=ai_client, max_sessions=args.sessions)

    exit_code = session_manager.run(client)

    total = session_manager.success_count + session_manager.failure_count
    print(f"Sessions run: {total}")
    print(f"Successes: {session_manager.success_count}")
    print(f"Failures: {session_manager.failure_count}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
