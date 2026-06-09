from dataclasses import dataclass
from typing import Protocol

from mealyspace.environment import Environment

ACTION_LABELS = ("A1", "A2", "A3", "A4")
ACTION_INPUT_TO_DIRECTION = {
    "1": "N",
    "2": "E",
    "3": "S",
    "4": "W",
    "A1": "N",
    "A2": "E",
    "A3": "S",
    "A4": "W",
}


@dataclass(frozen=True, slots=True)
class SessionState:
    success_count: int
    failure_count: int
    status: str
    result: str | None
    sensors: tuple[int, int, int, int] | None
    available_commands: tuple[str, ...]


class SessionClient(Protocol):
    def start(self) -> None: ...

    def render(self, state: SessionState) -> None: ...

    def get_command(self, state: SessionState) -> str: ...

    def show_error(self, message: str) -> None: ...

    def stop(self) -> int: ...


class SessionManager:
    def __init__(self) -> None:
        self.environment: Environment | None = None
        self.success_count = 0
        self.failure_count = 0

    def begin(self) -> None:
        self.environment = Environment()

    def session_commands(self) -> tuple[str, ...]:
        return ("B", "Q")

    def environment_commands(self) -> tuple[str, ...]:
        if self.environment is not None and self.environment.is_active:
            return ACTION_LABELS

        return ()

    def available_commands(self) -> tuple[str, ...]:
        commands: list[str] = list(self.session_commands())

        commands.extend(self.environment_commands())

        return tuple(commands)

    def state(self) -> SessionState:
        environment = self.environment

        if environment is None:
            status = "IDLE"
            result = None
            sensors = None
        elif environment.is_active:
            status = "ACTIVE"
            result = None
            sensors = environment.sensors()
        else:
            status = "COMPLETE"
            result = "SUCCESS" if environment.was_success else "FAILURE"
            sensors = None

        return SessionState(
            success_count=self.success_count,
            failure_count=self.failure_count,
            status=status,
            result=result,
            sensors=sensors,
            available_commands=self.available_commands(),
        )

    def run(self, client: SessionClient) -> int:
        client.start()

        while True:
            state = self.state()
            client.render(state)
            command = client.get_command(state)

            try:
                should_continue = self.handle_command(command)
            except ValueError as error:
                client.show_error(str(error))
                continue

            if not should_continue:
                return client.stop()

    def handle_command(self, command: str) -> bool:
        if command == "Q":
            return False

        if command == "B":
            self.begin()
            return True

        if command not in ACTION_INPUT_TO_DIRECTION:
            raise ValueError(f"Invalid command: {command}")

        if self.environment is None:
            raise ValueError("No environment. Use B to begin.")

        if not self.environment.is_active:
            raise ValueError("Round is over. Use B to start a new round.")

        self.environment.move(ACTION_INPUT_TO_DIRECTION[command])

        if not self.environment.is_active:
            if self.environment.was_success:
                self.success_count += 1
            else:
                self.failure_count += 1

        return True
