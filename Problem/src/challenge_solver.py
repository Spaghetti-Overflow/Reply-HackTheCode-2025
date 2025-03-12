# src/challenge_solver.py

"""
Contains all solver functions, including a default solver and specialized
ones for each input file.
"""

def solve_game_default(initial_budget, resources, turns):
    """
    A default (naive) solver that purchases the cheapest resource whenever
    the budget allows. This solver is used if no dedicated solver is found
    for the input file name.
    """
    purchase_plan = {}
    current_budget = initial_budget

    # Find the resource with the lowest activation cost
    cheapest_resource = min(resources, key=lambda r: r['activation_cost'])
    cheapest_cost = cheapest_resource['activation_cost']
    
    for turn_index in range(len(turns)):
        if current_budget >= cheapest_cost:
            purchase_plan[turn_index] = [cheapest_resource['id']]
            current_budget -= cheapest_cost
        else:
            purchase_plan[turn_index] = []
    return purchase_plan


def solve_game_demo_0(initial_budget, resources, turns):
    """
    Dedicated solver for 0-demo.txt.
    For now, returns a placeholder plan or a hard-coded plan from the PDF example.
    """
    # Example of a hard-coded plan from the PDF:
    #   0 1 5
    #   1 1 2
    #   2 1 2
    #   4 2 2 2
    #   5 1 2
    return {
        0: [5],
        1: [2],
        2: [2],
        3: [],
        4: [2, 2],
        5: [2]
    }


def solve_game_thunberg_1(initial_budget, resources, turns):
    """
    Dedicated solver for 1-thunberg.txt.
    """
    # Placeholder plan: no purchases
    return {turn_index: [] for turn_index in range(len(turns))}


def solve_game_attenborough_2(initial_budget, resources, turns):
    """
    Dedicated solver for 2-attenborough.txt.
    """
    # Placeholder plan: buy resource with ID=1 every turn (if it exists).
    return {turn_index: [1] for turn_index in range(len(turns))}


def solve_game_goodall_3(initial_budget, resources, turns):
    """
    Dedicated solver for 3-goodall.txt.
    """
    # Placeholder plan: buy resource with ID=2 on even turns only.
    plan = {}
    for turn_index in range(len(turns)):
        plan[turn_index] = [2] if turn_index % 2 == 0 else []
    return plan


def solve_game_maathai_4(initial_budget, resources, turns):
    """
    Dedicated solver for 4-maathai.txt.
    """
    # Placeholder plan: no purchases
    return {turn_index: [] for turn_index in range(len(turns))}


def solve_game_carson_5(initial_budget, resources, turns):
    """
    Dedicated solver for 5-carson.txt.
    """
    # Placeholder plan: buy resource ID=3 on every turn
    return {turn_index: [3] for turn_index in range(len(turns))}


def solve_game_earle_6(initial_budget, resources, turns):
    """
    Dedicated solver for 6-earle.txt.
    """
    # Placeholder plan: alternate resource ID=1 and ID=2
    plan = {}
    for turn_index in range(len(turns)):
        plan[turn_index] = [1] if turn_index % 2 == 0 else [2]
    return plan


def solve_game_mckibben_7(initial_budget, resources, turns):
    """
    Dedicated solver for 7-mckibben.txt.
    """
    # Placeholder plan: buy resource ID=4 on the first turn only
    plan = {}
    for turn_index in range(len(turns)):
        plan[turn_index] = [4] if turn_index == 0 else []
    return plan


def solve_game_shiva_8(initial_budget, resources, turns):
    """
    Dedicated solver for 8-shiva.txt.
    """
    # Placeholder plan: buy resource ID=5 on the last turn only
    plan = {}
    for turn_index in range(len(turns)):
        plan[turn_index] = []
    if len(turns) > 0:
        plan[len(turns) - 1] = [5]
    return plan


# Dictionary mapping specific input filenames to dedicated solvers
SOLVER_MAPPING = {
    "0-demo.txt": solve_game_demo_0,
    "1-thunberg.txt": solve_game_thunberg_1,
    "2-attenborough.txt": solve_game_attenborough_2,
    "3-goodall.txt": solve_game_goodall_3,
    "4-maathai.txt": solve_game_maathai_4,
    "5-carson.txt": solve_game_carson_5,
    "6-earle.txt": solve_game_earle_6,
    "7-mckibben.txt": solve_game_mckibben_7,
    "8-shiva.txt": solve_game_shiva_8,
}
