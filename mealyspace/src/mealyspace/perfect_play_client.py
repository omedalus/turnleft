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


class PerfectPlayClient(SessionClient):
    def __init__(self, total_sessions: int) -> None:
        if total_sessions < 1:
            raise ValueError("total_sessions must be at least 1")

        self.total_sessions = total_sessions
        self._phase = 0
        self._pending_actions: list[int] = []

    def start(self) -> None:
        return None

    def render(self, state: SessionState) -> None:
        _ = state

    def get_command(self, state: SessionState) -> SessionCommand:
        completed_sessions = state.success_count + state.failure_count
        if completed_sessions >= self.total_sessions:
            return SessionCommand(
                CommandTarget.SESSION_MANAGER,
                SessionManagerCommand.QUIT,
            )

        if state.status is not SessionStatus.RUNNING:
            self._reset_round_plan()
            return SessionCommand(
                CommandTarget.SESSION_MANAGER,
                SessionManagerCommand.BEGIN,
            )

        if self._phase == 0:
            self._phase = 1
            return self._environment_command(3)

        if self._phase == 1:
            if state.sensors is None:
                raise ValueError("Running state must include sensors.")

            go_east_signal = state.sensors[1]
            self._pending_actions = [1, 1] + ([2, 2] if go_east_signal else [4, 4])
            self._phase = 2

        if not self._pending_actions:
            raise ValueError("No planned actions remaining for running round.")

        next_action = self._pending_actions.pop(0)
        return self._environment_command(next_action)

    def show_error(self, message: str) -> None:
        raise RuntimeError(message)

    def stop(self) -> int:
        return 0

    def _environment_command(self, action: int) -> SessionCommand:
        return SessionCommand(CommandTarget.ENVIRONMENT, action)

    def _reset_round_plan(self) -> None:
        self._phase = 0
        self._pending_actions.clear()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run automated Mealy Space sessions with a perfect-play policy."
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
    client = PerfectPlayClient(total_sessions=args.sessions)
    exit_code = session_manager.run(client)

    total = session_manager.success_count + session_manager.failure_count
    print(f"Sessions run: {total}")
    print(f"Successes: {session_manager.success_count}")
    print(f"Failures: {session_manager.failure_count}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
