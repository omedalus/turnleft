import unittest

from mealyspace.environment import Environment


class EnvironmentTests(unittest.TestCase):
    def test_get_available_actions_defaults_to_all_true(self):
        env = Environment()

        self.assertEqual(env.get_available_actions(), (True, True, True, True))

    def test_sensors_are_booleans(self):
        env = Environment()

        sensors = env.sensors()

        self.assertEqual(len(sensors), 4)
        self.assertTrue(all(isinstance(value, bool) for value in sensors))


if __name__ == "__main__":
    unittest.main()
