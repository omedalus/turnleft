import unittest

from mealyspace.session_manager import (
    CommandTarget,
    SessionCommand,
    SessionManager,
    SessionManagerCommand,
    SessionStatus,
)


class FakeEnvironment:
    def __init__(
        self,
        *,
        is_active=True,
        was_success=None,
        available_actions=(True, True, True, True),
        sensors=(True, False, True, False),
        complete_on_execute=False,
        success_on_complete=False,
    ):
        self.is_active = is_active
        self.was_success = was_success
        self._available_actions = available_actions
        self._sensors = sensors
        self.complete_on_execute = complete_on_execute
        self.success_on_complete = success_on_complete
        self.executed_actions = []

    def get_available_actions(self):
        return self._available_actions

    def sensors(self):
        return self._sensors

    def execute_action(self, action):
        self.executed_actions.append(action)
        if self.complete_on_execute:
            self.is_active = False
            self.was_success = self.success_on_complete


class SessionManagerTests(unittest.TestCase):
    def test_state_without_environment_is_finished_with_no_result(self):
        manager = SessionManager()

        state = manager.state()

        self.assertEqual(state.status, SessionStatus.FINISHED_WITH_NO_RESULT)
        self.assertIsNone(state.sensors)
        self.assertIsNone(state.available_actions)

    def test_state_running_includes_sensors_and_available_actions(self):
        manager = SessionManager()
        fake_env = FakeEnvironment(is_active=True)
        manager.environment = fake_env

        state = manager.state()

        self.assertEqual(state.status, SessionStatus.RUNNING)
        self.assertEqual(state.sensors, fake_env.sensors())
        self.assertEqual(state.available_actions, fake_env.get_available_actions())

    def test_begin_command_creates_environment(self):
        manager = SessionManager()

        should_continue = manager.handle_command(
            SessionCommand(
                command_target=CommandTarget.SESSION_MANAGER,
                command_value=SessionManagerCommand.BEGIN,
            )
        )

        self.assertTrue(should_continue)
        self.assertIsNotNone(manager.environment)

    def test_quit_command_stops_session(self):
        manager = SessionManager()

        should_continue = manager.handle_command(
            SessionCommand(
                command_target=CommandTarget.SESSION_MANAGER,
                command_value=SessionManagerCommand.QUIT,
            )
        )

        self.assertFalse(should_continue)

    def test_environment_command_requires_active_environment(self):
        manager = SessionManager()

        with self.assertRaisesRegex(ValueError, "No environment"):
            manager.handle_command(
                SessionCommand(
                    command_target=CommandTarget.ENVIRONMENT,
                    command_value=1,
                )
            )

    def test_environment_command_respects_available_actions(self):
        manager = SessionManager()
        manager.environment = FakeEnvironment(
            available_actions=(True, False, True, True)
        )

        with self.assertRaisesRegex(ValueError, "not available"):
            manager.handle_command(
                SessionCommand(
                    command_target=CommandTarget.ENVIRONMENT,
                    command_value=2,
                )
            )

    def test_environment_command_updates_success_count_on_completed_success(self):
        manager = SessionManager()
        fake_env = FakeEnvironment(complete_on_execute=True, success_on_complete=True)
        manager.environment = fake_env

        should_continue = manager.handle_command(
            SessionCommand(
                command_target=CommandTarget.ENVIRONMENT,
                command_value=1,
            )
        )

        self.assertTrue(should_continue)
        self.assertEqual(fake_env.executed_actions, [1])
        self.assertEqual(manager.success_count, 1)
        self.assertEqual(manager.failure_count, 0)

    def test_environment_command_updates_failure_count_on_completed_failure(self):
        manager = SessionManager()
        fake_env = FakeEnvironment(complete_on_execute=True, success_on_complete=False)
        manager.environment = fake_env

        should_continue = manager.handle_command(
            SessionCommand(
                command_target=CommandTarget.ENVIRONMENT,
                command_value=1,
            )
        )

        self.assertTrue(should_continue)
        self.assertEqual(fake_env.executed_actions, [1])
        self.assertEqual(manager.success_count, 0)
        self.assertEqual(manager.failure_count, 1)


if __name__ == "__main__":
    unittest.main()
