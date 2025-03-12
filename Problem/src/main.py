# src/main.py
"""
Main entry point for the Reply Hack the Code challenge solver.
This script:
  1. Parses the input file.
  2. Uses a simple strategy to decide on resource purchases.
  3. Simulates the game turn by turn.
  4. Writes the purchase plan to an output file.
Usage:
    python main.py <input_file> <output_file>
"""

import sys
from src.utils import parse_input, write_output
from src.game_simulator import GameSimulator
from src.challenge_solver import solve_game

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Parse the challenge input.
    initial_budget, resources, turns = parse_input(input_file)
    
    # Obtain a purchase plan using the baseline strategy.
    purchase_plan = solve_game(initial_budget, resources, turns)
    
    # Initialize the game simulator.
    simulator = GameSimulator(initial_budget, resources, turns)
    
    # Run the simulation using the purchase plan.
    purchase_log, final_budget = simulator.run_simulation(purchase_plan)
    
    print(f"Final budget after simulation: {final_budget}")
    
    # Write the purchase log (plan) to the output file.
    write_output(output_file, purchase_log)
    print(f"Purchase plan written to {output_file}")

if __name__ == "__main__":
    main()
