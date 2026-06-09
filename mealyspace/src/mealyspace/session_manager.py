from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from mealyspace.environment import Environment


class SessionStatus(StrEnum):
    RUNNING = "running"
    FINISHED_WITH_VICTORY = "finished with victory"
    FINISHED_WITH_DEFEAT = "finished with defeat"
    FINISHED_WITH_NO_RESULT = "finished with no result"


class CommandTarget(StrEnum):
    ENVIRONMENT = "ENVIRONMENT"
    SESSION_MANAGER = "SESSION_MANAGER"


class SessionManagerCommand(StrEnum):
    BEGIN = "BEGIN"
    QUIT = "QUIT"


@dataclass(frozen=True, slots=True)
class SessionCommand:
    command_target: CommandTarget
    command_value: SessionManagerCommand | int


@dataclass(frozen=True, slots=True)
class SessionState:
    success_count: int
    failure_count: int
    status: SessionStatus
    sensors: tuple[bool, bool, bool, bool] | None


class SessionClient(Protocol):
    def start(self) -> None: ...

    def render(self, state: SessionState) -> None: ...

    def get_command(self, state: SessionState) -> SessionCommand: ...

    def show_error(self, message: str) -> None: ...

    def stop(self) -> int: ...


class SessionManager:
    def __init__(self) -> None:
        self.environment: Environment | None = None
        self.success_count = 0
        self.failure_count = 0

    def begin(self) -> None:
        self.environment = Environment()

    def state(self) -> SessionState:
        environment = self.environment

        if environment is None:
            status = SessionStatus.FINISHED_WITH_NO_RESULT
            sensors = None
        elif environment.is_active:
            status = SessionStatus.RUNNING
            sensors = environment.sensors()
        else:
            status = (
                SessionStatus.FINISHED_WITH_VICTORY
                if environment.was_success
                else SessionStatus.FINISHED_WITH_DEFEAT
            )
            sensors = None

        return SessionState(
            success_count=self.success_count,
            failure_count=self.failure_count,
            status=status,
            sensors=sensors,
        )

    def run(self, client: SessionClient) -> int:
        client.start()

        while True:
            state = self.state()
            try:
                client.render(state)
                command = client.get_command(state)
                should_continue = self.handle_command(command)
            except ValueError as error:
                client.show_error(str(error))
                continue

            if not should_continue:
                return client.stop()

    def handle_command(self, command: SessionCommand) -> bool:
        if command.command_target is CommandTarget.SESSION_MANAGER:
            if command.command_value is SessionManagerCommand.QUIT:
                return False

            if command.command_value is SessionManagerCommand.BEGIN:
                self.begin()
                return True

            raise ValueError("Invalid session-manager command.")

        if command.command_target is not CommandTarget.ENVIRONMENT:
            raise ValueError("Invalid command target.")

        if not isinstance(command.command_value, int):
            raise ValueError("Environment command must be a numeric action.")

        if self.environment is None:
            raise ValueError("No environment. Use B to begin.")

        if not self.environment.is_active:
            raise ValueError("Round is over. Use B to start a new round.")

        self.environment.execute_action(command.command_value)

        if not self.environment.is_active:
            if self.environment.was_success:
                self.success_count += 1
            else:
                self.failure_count += 1

        return True
