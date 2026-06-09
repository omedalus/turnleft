from mealyspace.session_manager import SessionClient, SessionManager, SessionState


class ConsoleClient(SessionClient):
    def start(self) -> None:
        print("Mealy Space")
        print("Commands: B begin new round, A1-A4 (or 1-4) move, Q quit.")

    def render(self, state: SessionState) -> None:
        print(f"\nSuccesses: {state.success_count}  Failures: {state.failure_count}")

        if state.status == "IDLE":
            print("Session status: IDLE")
        elif state.status == "ACTIVE":
            print("Session status: ACTIVE")
        else:
            print(f"Session status: COMPLETE ({state.result})")

        for command in state.available_commands:
            print(self._command_label(command))

        if state.sensors is not None:
            print("Environment:")
            print("  Sensors: [S1={0}, S2={1}, S3={2}, S4={3}]".format(*state.sensors))
            print("  Available actions: [A1, A2, A3, A4]")

    def get_command(self, state: SessionState) -> str:
        _ = state
        return input("> ").strip().upper()

    def show_error(self, message: str) -> None:
        print(message)

    def stop(self) -> int:
        print("Goodbye.")
        return 0

    def _command_label(self, command: str) -> str:
        labels = {
            "B": "- B: Begin",
            "Q": "- Q: Quit",
            "A1": "- A1: Move North",
            "A2": "- A2: Move East",
            "A3": "- A3: Move South",
            "A4": "- A4: Move West",
        }
        return labels.get(command, f"- {command}")


def main() -> int:
    session_manager = SessionManager()
    client = ConsoleClient()
    return session_manager.run(client)


if __name__ == "__main__":
    raise SystemExit(main())
