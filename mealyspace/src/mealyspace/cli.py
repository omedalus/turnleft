from mealyspace.environment import Environment


def main() -> int:
    environment = Environment()

    print("Mealy Space")
    print("Enter N, E, S, or W to move. Enter Q to quit.")

    while True:
        x, y = environment.position()
        print(f"\nCurrent position: ({x}, {y})")
        print(
            f"Successes: {environment.success_count}  Failures: {environment.failure_count}"
        )
        print("Available moves: " + ", ".join(environment.available_moves()))

        command = input("> ").strip().upper()

        try:
            if not environment.handle_command(command):
                print("Goodbye.")
                return 0
        except ValueError:
            print("Invalid command. Use N, E, S, W, or Q.")
            continue


if __name__ == "__main__":
    raise SystemExit(main())
