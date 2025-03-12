# src/utils.py

"""
Utility functions for parsing input and writing output.
"""

import os

def parse_input(file_path):
    """
    Parse the challenge input file.
    Expected format:
      - First line: D R T (initial budget, number of resources, number of turns)
      - Next R lines: resource definitions
      - Next T lines: turn definitions
    Returns:
      initial_budget (int), resources (list of dict), turns (list of dict)
    """
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # First line: initial budget, number of resources, number of turns.
    first_line = lines[0].split()
    initial_budget = int(first_line[0])
    num_resources = int(first_line[1])
    num_turns = int(first_line[2])
    
    # Parse resource definitions: next num_resources lines.
    resources = []
    for i in range(1, 1 + num_resources):
        resource = parse_resource_line(lines[i])
        resources.append(resource)
    
    # Parse turn definitions: next num_turns lines.
    turns = []
    for i in range(1 + num_resources, 1 + num_resources + num_turns):
        turn = parse_turn_line(lines[i])
        turns.append(turn)
    
    return initial_budget, resources, turns

def parse_resource_line(line):
    """
    Parse a single resource definition line.
    Expected format: 
      RIr RAr RPr RWr RMr RLr RUr RTr REr
    where RTr is a letter and REr is an integer (the special effect percentage).
    Returns:
      Dictionary with resource parameters.
    """
    parts = line.split()
    resource = {
        'id': int(parts[0]),
        'activation_cost': int(parts[1]),
        'periodic_cost': int(parts[2]),
        'active_duration': int(parts[3]),
        'downtime': int(parts[4]),
        'lifecycle': int(parts[5]),
        'buildings_powered': int(parts[6]),
        'resource_type': parts[7],
        'special_effect': int(parts[8]) if len(parts) > 8 else 0
    }
    return resource

def parse_turn_line(line):
    """
    Parse a single turn definition line.
    Expected format: 
      TM TX TR
    where TM = minimum buildings to power, TX = maximum buildings, TR = profit per building.
    Returns:
      Dictionary with turn parameters.
    """
    parts = line.split()
    turn = {
        'TM': int(parts[0]),
        'TX': int(parts[1]),
        'TR': int(parts[2])
    }
    return turn

def write_output(file_path, purchase_plan):
    """
    Write the purchase plan to the output file.
    purchase_plan is a list of tuples: (turn_index, [resource ids purchased]).
    Each output line has the format:
      t Rt RI1 RI2 ... RIRt
    where t is the turn number and Rt is the count of resources purchased in that turn.
    """
    with open(file_path, 'w') as f:
        for turn, resources in purchase_plan:
            line = f"{turn} {len(resources)} " + " ".join(map(str, resources))
            f.write(line + "\n")
