from mealyspace.environment import Environment


def main() -> int:
    environment = Environment()

    print("Mealy Space")
    print("Enter N, E, S, or W to move. Enter Q to quit.")

    while True:
        x, y = environment.position()
        print(f"\nCurrent position: ({x}, {y})")
        print("Available moves: " + ", ".join(environment.available_moves()))

        command = input("> ").strip().upper()

        if command == "Q":
            print("Goodbye.")
            return 0

        if command not in environment.available_moves():
            print("Invalid command. Use N, E, S, W, or Q.")
            continue

        environment.move(command)


if __name__ == "__main__":
    raise SystemExit(main())
