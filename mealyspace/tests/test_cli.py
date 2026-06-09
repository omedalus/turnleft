import unittest
from unittest.mock import patch

from mealyspace.cli import ConsoleClient
from mealyspace.session_manager import (
    CommandTarget,
    SessionManagerCommand,
    SessionState,
    SessionStatus,
)


class ConsoleClientCommandParsingTests(unittest.TestCase):
    def setUp(self):
        self.client = ConsoleClient()
        self.state = SessionState(
            success_count=0,
            failure_count=0,
            status=SessionStatus.FINISHED_WITH_NO_RESULT,
            sensors=None,
            available_actions=None,
        )

    @patch("builtins.input", return_value="B")
    def test_get_command_begin(self, _mock_input):
        command = self.client.get_command(self.state)

        self.assertEqual(command.command_target, CommandTarget.SESSION_MANAGER)
        self.assertEqual(command.command_value, SessionManagerCommand.BEGIN)

    @patch("builtins.input", return_value="Q")
    def test_get_command_quit(self, _mock_input):
        command = self.client.get_command(self.state)

        self.assertEqual(command.command_target, CommandTarget.SESSION_MANAGER)
        self.assertEqual(command.command_value, SessionManagerCommand.QUIT)

    @patch("builtins.input", return_value="3")
    def test_get_command_numeric_action(self, _mock_input):
        command = self.client.get_command(self.state)

        self.assertEqual(command.command_target, CommandTarget.ENVIRONMENT)
        self.assertEqual(command.command_value, 3)

    @patch("builtins.input", return_value="a12")
    def test_get_command_prefixed_action(self, _mock_input):
        command = self.client.get_command(self.state)

        self.assertEqual(command.command_target, CommandTarget.ENVIRONMENT)
        self.assertEqual(command.command_value, 12)

    @patch("builtins.input", return_value="A0")
    def test_get_command_rejects_zero_action(self, _mock_input):
        with self.assertRaisesRegex(ValueError, "Invalid command"):
            self.client.get_command(self.state)

    @patch("builtins.input", return_value="NOPE")
    def test_get_command_rejects_invalid_text(self, _mock_input):
        with self.assertRaisesRegex(ValueError, "Invalid command"):
            self.client.get_command(self.state)


if __name__ == "__main__":
    unittest.main()
