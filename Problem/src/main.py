# src/main.py

"""
Main entry point for the Reply Hack the Code challenge solver.
Usage:
    python src/main.py <input_file> <output_file> [--solver auto|default|dedicated]
"""

import os
import sys
import argparse

from src.utils import parse_input, write_output
from src.game_simulator import GameSimulator
from src.challenge_solver import (
    solve_game_default,
    SOLVER_MAPPING
)

def main():
    parser = argparse.ArgumentParser(description="Reply Hack the Code solver")
    parser.add_argument("input_file", type=str, help="Path to input file")
    parser.add_argument("output_file", type=str, help="Path to output file")
    parser.add_argument(
        "--solver",
        choices=["auto", "default", "dedicated"],
        default="auto",
        help="Select solver: auto (use dedicated if available, otherwise default), "
             "default (always use default solver), or dedicated (force dedicated solver)"
    )
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file

    # Parse the challenge input.
    initial_budget, resources, turns = parse_input(input_file)
    file_basename = os.path.basename(input_file)

    # Determine solver based on flag.
    if args.solver == "default":
        solver_func = solve_game_default
        print(f"Using default solver for {file_basename}")
    elif args.solver == "dedicated":
        if file_basename in SOLVER_MAPPING:
            solver_func = SOLVER_MAPPING[file_basename]
            print(f"Using dedicated solver for {file_basename}")
        else:
            print(f"Dedicated solver not found for {file_basename}. Exiting.")
            sys.exit(1)
    else:  # auto mode
        if file_basename in SOLVER_MAPPING:
            solver_func = SOLVER_MAPPING[file_basename]
            print(f"Using dedicated solver for {file_basename}")
        else:
            solver_func = solve_game_default
            print(f"No dedicated solver for {file_basename}, using default solver.")

    # Get the purchase plan from the chosen solver
    purchase_plan = solver_func(initial_budget, resources, turns)

    # Initialize and run the simulation.
    simulator = GameSimulator(initial_budget, resources, turns)
    purchase_log, final_budget = simulator.run_simulation(purchase_plan)
    
    print(f"Final budget after simulation: {final_budget}")

    # Write the purchase plan to the output file.
    write_output(output_file, purchase_log)
    print(f"Purchase plan written to {output_file}")

if __name__ == "__main__":
    main()
