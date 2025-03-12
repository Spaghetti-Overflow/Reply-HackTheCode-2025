# src/challenge_solver.py
"""
Implements a simple (baseline) strategy for resource purchasing.
This naive strategy checks if the current budget is sufficient to purchase the cheapest resource,
and if so, purchases it once each turn.
Note: This strategy does not account for maintenance costs, special effects,
or future profits. It can be improved over time.
"""

def solve_game(initial_budget, resources, turns):
    """
    Determine a purchase plan based on a naive strategy.
    Args:
      initial_budget: starting budget (int)
      resources: list of resource definitions (list of dicts)
      turns: list of turn definitions (list of dicts)
    Returns:
      purchase_plan: dictionary mapping turn index to list of resource IDs to purchase.
    """
    purchase_plan = {}
    current_budget = initial_budget
    # Find the resource with the lowest activation cost.
    cheapest_resource = min(resources, key=lambda r: r['activation_cost'])
    cheapest_cost = cheapest_resource['activation_cost']
    
    num_turns = len(turns)
    # For each turn, if budget is at least the cheapest_cost, purchase that resource once.
    for turn in range(num_turns):
        if current_budget >= cheapest_cost:
            purchase_plan[turn] = [cheapest_resource['id']]
            current_budget -= cheapest_cost  # Deduct cost for planning purposes.
        else:
            purchase_plan[turn] = []
        # This strategy is static; a more advanced approach would simulate turn outcomes to adjust the budget.
    return purchase_plan
