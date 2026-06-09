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
            print("Session status: IDLE")
            print("- B: Begin")
            print("- R: Restart")
            print("- Q: Quit")
        else:
            if environment.is_active:
                print("Session status: ACTIVE")
            else:
                result = "SUCCESS" if environment.was_success else "FAILURE"
                print(f"Session status: COMPLETE ({result})")

            print("- R: Restart")
            print("- Q: Quit")

            if environment.is_active:
                print("Environment:")
                sensors = environment.sensors()
                print("  Sensors: [N={0}, E={1}, S={2}, W={3}]".format(*sensors))
                print("  Available actions: [N, E, S, W]")

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
