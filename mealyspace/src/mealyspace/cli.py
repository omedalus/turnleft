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

        session_commands = session_manager.session_commands()
        environment_commands = session_manager.environment_commands()

        print("Session commands: " + ", ".join(session_commands))

        if environment_commands:
            print("Environment commands: " + ", ".join(environment_commands))
        else:
            print("Environment commands: (none)")

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
