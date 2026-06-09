from mealyspace.session_manager import (
    CommandTarget,
    SessionCommand,
    SessionClient,
    SessionManagerCommand,
    SessionManager,
    SessionState,
    SessionStatus,
)


class ConsoleClient(SessionClient):
    def __init__(self) -> None:
        self.command_target = CommandTarget.SESSION_MANAGER
        self.command_value: SessionManagerCommand | int = SessionManagerCommand.BEGIN

    def start(self) -> None:
        print("Mealy Space")
        print("Commands: B begin new round, A1-A4 (or 1-4) move, Q quit.")

    def render(self, state: SessionState) -> None:
        print(f"\nSuccesses: {state.success_count}  Failures: {state.failure_count}")

        print(f"Session status: {state.status.value}")

        print("- B: Begin")
        print("- Q: Quit")

        if state.status is SessionStatus.RUNNING:
            print("- A1: Move North")
            print("- A2: Move East")
            print("- A3: Move South")
            print("- A4: Move West")

        if state.sensors is not None:
            print("Environment:")
            print("  Sensors: [S1={0}, S2={1}, S3={2}, S4={3}]".format(*state.sensors))
            print("  Available actions: [A1, A2, A3, A4]")

    def get_command(self, state: SessionState) -> SessionCommand:
        _ = state
        raw = input("> ").strip().upper()

        if raw == "B":
            self.command_target = CommandTarget.SESSION_MANAGER
            self.command_value = SessionManagerCommand.BEGIN
        elif raw == "Q":
            self.command_target = CommandTarget.SESSION_MANAGER
            self.command_value = SessionManagerCommand.QUIT
        else:
            action = self._parse_action(raw)
            self.command_target = CommandTarget.ENVIRONMENT
            self.command_value = action

        return SessionCommand(
            command_target=self.command_target,
            command_value=self.command_value,
        )

    def show_error(self, message: str) -> None:
        print(message)

    def stop(self) -> int:
        print("Goodbye.")
        return 0

    def _parse_action(self, raw: str) -> int:
        if raw in {"1", "2", "3", "4"}:
            return int(raw)

        if raw in {"A1", "A2", "A3", "A4"}:
            return int(raw[1])

        raise ValueError(f"Invalid command: {raw}")


def main() -> int:
    session_manager = SessionManager()
    client = ConsoleClient()
    return session_manager.run(client)


if __name__ == "__main__":
    raise SystemExit(main())
