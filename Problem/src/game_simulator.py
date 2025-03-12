# src/game_simulator.py
"""
Simulate the game mechanics turn by turn. The simulator handles resource purchases,
maintenance costs, power production, profit calculation, and resource state updates.
"""

from src.resource import Resource

class GameSimulator:
    def __init__(self, initial_budget, resources_def, turns):
        """
        Initialize the simulator.
          - initial_budget: starting budget (int)
          - resources_def: list of resource definitions (each is a dict)
          - turns: list of turn definitions (each is a dict with keys 'TM', 'TX', 'TR')
        """
        self.initial_budget = initial_budget
        self.budget = initial_budget
        self.turns = turns
        self.resources_def = resources_def
        self.active_resources = []  # List of Resource instances currently in play
        self.purchase_log = []      # List of tuples: (turn, [resource ids purchased])

    def purchase_resources(self, turn_index, resource_ids):
        """
        Attempt to purchase a list of resources at the beginning of a turn.
        resource_ids: list of resource IDs to purchase.
        Returns:
          True if purchase is successful (i.e. activation cost <= budget), else False.
        """
        total_cost = 0
        new_resources = []
        for rid in resource_ids:
            # Find the resource definition by id.
            res_def = next((r for r in self.resources_def if r['id'] == rid), None)
            if res_def is None:
                continue
            total_cost += res_def['activation_cost']
            new_resource = Resource(res_def)
            new_resources.append(new_resource)
        
        if total_cost > self.budget:
            # Not enough budget to purchase these resources.
            return False
        
        self.budget -= total_cost
        self.active_resources.extend(new_resources)
        self.purchase_log.append((turn_index, resource_ids))
        return True

    def simulate_turn(self, turn_index, purchase_ids):
        """
        Simulate a single turn:
          1. Purchase phase.
          2. Maintenance: sum the maintenance costs of all resources.
          3. Production: sum the number of buildings powered by active resources.
          4. Profit calculation: if powered buildings ≥ TM, profit = min(power, TX) * TR.
          5. Update budget and resource states.
        Returns:
          Dictionary summarizing turn results.
        """
        # Purchase phase.
        if purchase_ids:
            success = self.purchase_resources(turn_index, purchase_ids)
            if not success:
                print(f"Turn {turn_index}: Purchase failed due to insufficient budget.")

        # Calculate total maintenance cost.
        total_maintenance = sum(res.get_maintenance_cost() for res in self.active_resources)
        
        # Calculate total power produced.
        total_power = sum(res.get_power() for res in self.active_resources)
        
        # Get current turn parameters.
        turn_params = self.turns[turn_index]
        TM = turn_params['TM']
        TX = turn_params['TX']
        TR = turn_params['TR']
        
        # Calculate profit if minimum threshold is met.
        profit = min(total_power, TX) * TR if total_power >= TM else 0
        
        # Update budget.
        self.budget += profit - total_maintenance
        
        # Update resource states and remove expired ones.
        alive_resources = []
        for res in self.active_resources:
            if res.update_state():
                alive_resources.append(res)
        self.active_resources = alive_resources
        
        # Return a summary for debugging.
        return {
            'turn': turn_index,
            'purchases': purchase_ids,
            'maintenance': total_maintenance,
            'total_power': total_power,
            'profit': profit,
            'budget': self.budget
        }

    def run_simulation(self, purchase_plan):
        """
        Run the simulation over all turns using the provided purchase plan.
        purchase_plan: dictionary mapping turn index to a list of resource IDs to purchase.
        Returns:
          Tuple (purchase_log, final_budget)
        """
        num_turns = len(self.turns)
        for turn in range(num_turns):
            purchases = purchase_plan.get(turn, [])
            summary = self.simulate_turn(turn, purchases)
            print(f"Turn {turn}: {summary}")  # Debug output for each turn.
        return self.purchase_log, self.budget
