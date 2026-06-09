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
        print("Commands: B begin new round, A<number> (or number) move, Q quit.")

    def render(self, state: SessionState) -> None:
        print(f"\nSuccesses: {state.success_count}  Failures: {state.failure_count}")

        print(f"Session status: {state.status.value}")

        print("- B: Begin")
        print("- Q: Quit")

        if (
            state.status is SessionStatus.RUNNING
            and state.available_actions is not None
        ):
            for action, is_available in enumerate(state.available_actions, start=1):
                if is_available:
                    print(f"- A{action}: Execute action {action}")

        if state.sensors is not None:
            print("Environment:")
            sensor_tokens = [
                f"S{index}={value}"
                for index, value in enumerate(state.sensors, start=1)
            ]
            print(f"  Sensors: [{' '.join(sensor_tokens)}]")

        if state.available_actions is not None:
            print(f"  Available actions: {list(state.available_actions)}")

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
        if raw.isdigit() and int(raw) > 0:
            return int(raw)

        if raw.startswith("A") and raw[1:].isdigit() and int(raw[1:]) > 0:
            return int(raw[1:])

        raise ValueError(f"Invalid command: {raw}")


def main() -> int:
    session_manager = SessionManager()
    client = ConsoleClient()
    return session_manager.run(client)


if __name__ == "__main__":
    raise SystemExit(main())
