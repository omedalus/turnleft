from mealyspace.environment import Environment


class SessionManager:
    def __init__(self) -> None:
        self.environment: Environment | None = None
        self.success_count = 0
        self.failure_count = 0

    def begin(self) -> None:
        self.environment = Environment()

    def reset(self) -> None:
        self.environment = Environment()

    def available_commands(self) -> tuple[str, ...]:
        commands: list[str] = ["B", "R", "Q"]

        if self.environment is not None and self.environment.is_active:
            commands.extend(self.environment.available_moves())

        return tuple(commands)

    def handle_command(self, command: str) -> bool:
        if command == "Q":
            return False

        if command == "B":
            self.begin()
            return True

        if command == "R":
            self.reset()
            return True

        if command not in {"N", "E", "S", "W"}:
            raise ValueError(f"Invalid command: {command}")

        if self.environment is None:
            raise ValueError("No environment. Use B to begin.")

        if not self.environment.is_active:
            raise ValueError("Round is over. Use B or R to start a new round.")

        self.environment.move(command)

        if not self.environment.is_active:
            if self.environment.was_success:
                self.success_count += 1
            else:
                self.failure_count += 1

        return True
