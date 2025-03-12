# tests/test_solver.py

"""
Unit tests for the challenge solver and simulation.
"""

import unittest
import os
from src.utils import parse_input
from src.challenge_solver import solve_game
from src.game_simulator import GameSimulator

class TestChallengeSolver(unittest.TestCase):

    def setUp(self):
        # Create a simple test input as a multi-line string.
        # Format: first line (budget, number of resources, number of turns),
        # followed by resource definitions, then turn definitions.
        self.test_input = """
                             10 2 3
                             1 5 1 1 1 3 2 X 0
                             2 3 1 1 1 3 1 X 0
                             3 5 4
                             4 6 3
                             2 7 1
                          """
        # Write the test input to a temporary file.
        self.input_file = "tests/test_input.txt"
        with open(self.input_file, "w") as f:
            f.write(self.test_input)
    
    def tearDown(self):
        # Clean up the temporary file.
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
    
    def test_parse_input(self):
        initial_budget, resources, turns = parse_input(self.input_file)
        self.assertEqual(initial_budget, 10)
        self.assertEqual(len(resources), 2)
        self.assertEqual(len(turns), 3)
    
    def test_solve_game_and_simulation(self):
        initial_budget, resources, turns = parse_input(self.input_file)
        purchase_plan = solve_game(initial_budget, resources, turns)
        simulator = GameSimulator(initial_budget, resources, turns)
        purchase_log, final_budget = simulator.run_simulation(purchase_plan)
        self.assertIsInstance(purchase_log, list)
        self.assertIsInstance(final_budget, int)
        # Additional checks can be added here based on expected simulation outcomes.

if __name__ == '__main__':
    unittest.main()
