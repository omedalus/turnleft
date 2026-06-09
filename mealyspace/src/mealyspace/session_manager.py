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

    def session_commands(self) -> tuple[str, ...]:
        if self.environment is not None and self.environment.is_active:
            return ("R", "Q")

        return ("B", "R", "Q")

    def environment_commands(self) -> tuple[str, ...]:
        if self.environment is not None and self.environment.is_active:
            return self.environment.available_moves()

        return ()

    def available_commands(self) -> tuple[str, ...]:
        commands: list[str] = list(self.session_commands())

        commands.extend(self.environment_commands())

        return tuple(commands)

    def handle_command(self, command: str) -> bool:
        if command == "Q":
            return False

        if command == "B":
            if self.environment is not None and self.environment.is_active:
                raise ValueError(
                    "Cannot begin while a round is active. Use R to restart."
                )

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
