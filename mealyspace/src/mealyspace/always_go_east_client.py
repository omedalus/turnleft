import argparse

from mealyspace.session_manager import (
    CommandTarget,
    SessionCommand,
    SessionClient,
    SessionManager,
    SessionManagerCommand,
    SessionState,
    SessionStatus,
)


class AlwaysGoEastClient(SessionClient):
    def __init__(self, total_sessions: int) -> None:
        if total_sessions < 1:
            raise ValueError("total_sessions must be at least 1")

        self.total_sessions = total_sessions
        self.command_target = CommandTarget.SESSION_MANAGER
        self.command_value: SessionManagerCommand | int = SessionManagerCommand.BEGIN

    def start(self) -> None:
        return None

    def render(self, state: SessionState) -> None:
        _ = state

    def get_command(self, state: SessionState) -> SessionCommand:
        completed_sessions = state.success_count + state.failure_count
        if completed_sessions >= self.total_sessions:
            self.command_target = CommandTarget.SESSION_MANAGER
            self.command_value = SessionManagerCommand.QUIT
            return SessionCommand(self.command_target, self.command_value)

        if state.status is SessionStatus.RUNNING:
            if state.sensors is None:
                raise ValueError("Running state must include sensors.")

            action = 1 if state.sensors[0] else 2
            self.command_target = CommandTarget.ENVIRONMENT
            self.command_value = action
            return SessionCommand(self.command_target, self.command_value)

        self.command_target = CommandTarget.SESSION_MANAGER
        self.command_value = SessionManagerCommand.BEGIN
        return SessionCommand(self.command_target, self.command_value)

    def show_error(self, message: str) -> None:
        raise RuntimeError(message)

    def stop(self) -> int:
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run automated Mealy Space sessions with an always-go-east policy."
    )
    parser.add_argument(
        "sessions",
        type=int,
        nargs="?",
        default=100,
        help="Number of sessions to run (default: 100).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session_manager = SessionManager()
    client = AlwaysGoEastClient(total_sessions=args.sessions)
    exit_code = session_manager.run(client)

    total = session_manager.success_count + session_manager.failure_count
    print(f"Sessions run: {total}")
    print(f"Successes: {session_manager.success_count}")
    print(f"Failures: {session_manager.failure_count}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
