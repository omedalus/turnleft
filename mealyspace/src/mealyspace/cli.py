from mealyspace.session_manager import SessionManager


def main() -> int:
    session_manager = SessionManager()

    print("Mealy Space")
    print("Commands: B begin, R restart, N/E/S/W move, Q quit.")

    while True:
        print(
            f"\nSuccesses: {session_manager.success_count}  Failures: {session_manager.failure_count}"
        )

        environment = session_manager.environment

        if environment is None:
            print("No active environment. Enter B to begin.")
        else:
            x, y = environment.position()
            print(f"Current position: ({x}, {y})")

            if environment.is_active:
                print("Round status: ACTIVE")
            else:
                result = "SUCCESS" if environment.was_success else "FAILURE"
                print(f"Round status: COMPLETE ({result})")

        print("Available commands: " + ", ".join(session_manager.available_commands()))

        command = input("> ").strip().upper()

        try:
            if not session_manager.handle_command(command):
                print("Goodbye.")
                return 0
        except ValueError:
            print("Invalid command. Use available commands shown above.")
            continue


if __name__ == "__main__":
    raise SystemExit(main())
