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
    """
    
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r['activation_cost'] <= budget],
            key=lambda r: (-r['buildings_powered'] / (r['activation_cost'] + r['periodic_cost']), r['activation_cost'])
        )

        total_power = sum(r['buildings_powered'] for r in active_resources if r['active'])

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res['activation_cost']:
                budget -= res['activation_cost']
                acquired_resources[t].append(res['id'])
                active_resources.append({
                    'id': res['id'],
                    'activation_cost': res['activation_cost'],
                    'periodic_cost': res['periodic_cost'],
                    'active_turns': res['active_duration'],
                    'downtime_turns': res['downtime'],
                    'lifespan': res['lifecycle'],
                    'buildings_powered': res['buildings_powered'],
                    'type': res['resource_type'],
                    'effect': res['special_effect'],
                    'remaining_life': res['lifecycle'],
                    'current_state': res['active_duration'],
                    'active': True
                })
                total_power += res['buildings_powered']

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res['periodic_cost'] for res in active_resources if res['active'])

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res['remaining_life'] -= 1
            res['current_state'] -= 1

            if res['remaining_life'] <= 0:
                active_resources.remove(res)
                continue

            if res['current_state'] == 0:
                res['active'] = not res['active']
                res['current_state'] = res['active_turns'] if res['active'] else res['downtime_turns']

    return acquired_resources

def solve_game_thunberg_1(initial_budget, resources, turns):
    """
    Dedicated solver for 1-thunberg.txt.
    """
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r['activation_cost'] <= budget],
            key=lambda r: (-r['buildings_powered'] / (r['activation_cost'] + r['periodic_cost']), r['activation_cost'])
        )

        total_power = sum(r['buildings_powered'] for r in active_resources if r['active'])

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res['activation_cost']:
                budget -= res['activation_cost']
                acquired_resources[t].append(res['id'])
                active_resources.append({
                    'id': res['id'],
                    'activation_cost': res['activation_cost'],
                    'periodic_cost': res['periodic_cost'],
                    'active_turns': res['active_duration'],
                    'downtime_turns': res['downtime'],
                    'lifespan': res['lifecycle'],
                    'buildings_powered': res['buildings_powered'],
                    'type': res['resource_type'],
                    'effect': res['special_effect'],
                    'remaining_life': res['lifecycle'],
                    'current_state': res['active_duration'],
                    'active': True
                })
                total_power += res['buildings_powered']

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res['periodic_cost'] for res in active_resources if res['active'])

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res['remaining_life'] -= 1
            res['current_state'] -= 1

            if res['remaining_life'] <= 0:
                active_resources.remove(res)
                continue

            if res['current_state'] == 0:
                res['active'] = not res['active']
                res['current_state'] = res['active_turns'] if res['active'] else res['downtime_turns']

    return acquired_resources

def solve_game_attenborough_2(initial_budget, resources, turns):
    """
    Dedicated solver for 2-attenborough.txt.
    """
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r['activation_cost'] <= budget],
            key=lambda r: (-r['buildings_powered'] / (r['activation_cost'] + r['periodic_cost']), r['activation_cost'])
        )

        total_power = sum(r['buildings_powered'] for r in active_resources if r['active'])

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res['activation_cost']:
                budget -= res['activation_cost']
                acquired_resources[t].append(res['id'])
                active_resources.append({
                    'id': res['id'],
                    'activation_cost': res['activation_cost'],
                    'periodic_cost': res['periodic_cost'],
                    'active_turns': res['active_duration'],
                    'downtime_turns': res['downtime'],
                    'lifespan': res['lifecycle'],
                    'buildings_powered': res['buildings_powered'],
                    'type': res['resource_type'],
                    'effect': res['special_effect'],
                    'remaining_life': res['lifecycle'],
                    'current_state': res['active_duration'],
                    'active': True
                })
                total_power += res['buildings_powered']

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res['periodic_cost'] for res in active_resources if res['active'])

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res['remaining_life'] -= 1
            res['current_state'] -= 1

            if res['remaining_life'] <= 0:
                active_resources.remove(res)
                continue

            if res['current_state'] == 0:
                res['active'] = not res['active']
                res['current_state'] = res['active_turns'] if res['active'] else res['downtime_turns']

    return acquired_resources

def solve_game_goodall_3(initial_budget, resources, turns):
    """
    Dedicated solver for 3-goodall.txt.
    """
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r['activation_cost'] <= budget],
            key=lambda r: (-r['buildings_powered'] / (r['activation_cost'] + r['periodic_cost']), r['activation_cost'])
        )

        total_power = sum(r['buildings_powered'] for r in active_resources if r['active'])

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res['activation_cost']:
                budget -= res['activation_cost']
                acquired_resources[t].append(res['id'])
                active_resources.append({
                    'id': res['id'],
                    'activation_cost': res['activation_cost'],
                    'periodic_cost': res['periodic_cost'],
                    'active_turns': res['active_duration'],
                    'downtime_turns': res['downtime'],
                    'lifespan': res['lifecycle'],
                    'buildings_powered': res['buildings_powered'],
                    'type': res['resource_type'],
                    'effect': res['special_effect'],
                    'remaining_life': res['lifecycle'],
                    'current_state': res['active_duration'],
                    'active': True
                })
                total_power += res['buildings_powered']

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res['periodic_cost'] for res in active_resources if res['active'])

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res['remaining_life'] -= 1
            res['current_state'] -= 1

            if res['remaining_life'] <= 0:
                active_resources.remove(res)
                continue

            if res['current_state'] == 0:
                res['active'] = not res['active']
                res['current_state'] = res['active_turns'] if res['active'] else res['downtime_turns']

    return acquired_resources

def solve_game_maathai_4(initial_budget, resources, turns):
    """
    Dedicated solver for 4-maathai.txt.
    """
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r['activation_cost'] <= budget],
            key=lambda r: (-r['buildings_powered'] / (r['activation_cost'] + r['periodic_cost']), r['activation_cost'])
        )

        total_power = sum(r['buildings_powered'] for r in active_resources if r['active'])

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res['activation_cost']:
                budget -= res['activation_cost']
                acquired_resources[t].append(res['id'])
                active_resources.append({
                    'id': res['id'],
                    'activation_cost': res['activation_cost'],
                    'periodic_cost': res['periodic_cost'],
                    'active_turns': res['active_duration'],
                    'downtime_turns': res['downtime'],
                    'lifespan': res['lifecycle'],
                    'buildings_powered': res['buildings_powered'],
                    'type': res['resource_type'],
                    'effect': res['special_effect'],
                    'remaining_life': res['lifecycle'],
                    'current_state': res['active_duration'],
                    'active': True
                })
                total_power += res['buildings_powered']

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res['periodic_cost'] for res in active_resources if res['active'])

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res['remaining_life'] -= 1
            res['current_state'] -= 1

            if res['remaining_life'] <= 0:
                active_resources.remove(res)
                continue

            if res['current_state'] == 0:
                res['active'] = not res['active']
                res['current_state'] = res['active_turns'] if res['active'] else res['downtime_turns']

    return acquired_resources

def solve_game_carson_5(initial_budget, resources, turns):
    """
    Dedicated solver for 5-carson.txt.
    """
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r['activation_cost'] <= budget],
            key=lambda r: (-r['buildings_powered'] / (r['activation_cost'] + r['periodic_cost']), r['activation_cost'])
        )

        total_power = sum(r['buildings_powered'] for r in active_resources if r['active'])

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res['activation_cost']:
                budget -= res['activation_cost']
                acquired_resources[t].append(res['id'])
                active_resources.append({
                    'id': res['id'],
                    'activation_cost': res['activation_cost'],
                    'periodic_cost': res['periodic_cost'],
                    'active_turns': res['active_duration'],
                    'downtime_turns': res['downtime'],
                    'lifespan': res['lifecycle'],
                    'buildings_powered': res['buildings_powered'],
                    'type': res['resource_type'],
                    'effect': res['special_effect'],
                    'remaining_life': res['lifecycle'],
                    'current_state': res['active_duration'],
                    'active': True
                })
                total_power += res['buildings_powered']

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res['periodic_cost'] for res in active_resources if res['active'])

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res['remaining_life'] -= 1
            res['current_state'] -= 1

            if res['remaining_life'] <= 0:
                active_resources.remove(res)
                continue

            if res['current_state'] == 0:
                res['active'] = not res['active']
                res['current_state'] = res['active_turns'] if res['active'] else res['downtime_turns']

    return acquired_resources

def solve_game_earle_6(initial_budget, resources, turns):
    """
    Dedicated solver for 6-earle.txt.
    """
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r['activation_cost'] <= budget],
            key=lambda r: (-r['buildings_powered'] / (r['activation_cost'] + r['periodic_cost']), r['activation_cost'])
        )

        total_power = sum(r['buildings_powered'] for r in active_resources if r['active'])

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res['activation_cost']:
                budget -= res['activation_cost']
                acquired_resources[t].append(res['id'])
                active_resources.append({
                    'id': res['id'],
                    'activation_cost': res['activation_cost'],
                    'periodic_cost': res['periodic_cost'],
                    'active_turns': res['active_duration'],
                    'downtime_turns': res['downtime'],
                    'lifespan': res['lifecycle'],
                    'buildings_powered': res['buildings_powered'],
                    'type': res['resource_type'],
                    'effect': res['special_effect'],
                    'remaining_life': res['lifecycle'],
                    'current_state': res['active_duration'],
                    'active': True
                })
                total_power += res['buildings_powered']

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res['periodic_cost'] for res in active_resources if res['active'])

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res['remaining_life'] -= 1
            res['current_state'] -= 1

            if res['remaining_life'] <= 0:
                active_resources.remove(res)
                continue

            if res['current_state'] == 0:
                res['active'] = not res['active']
                res['current_state'] = res['active_turns'] if res['active'] else res['downtime_turns']

    return acquired_resources

def solve_game_mckibben_7(initial_budget, resources, turns):
    """
    Dedicated solver for 7-mckibben.txt.
    """
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r['activation_cost'] <= budget],
            key=lambda r: (-r['buildings_powered'] / (r['activation_cost'] + r['periodic_cost']), r['activation_cost'])
        )

        total_power = sum(r['buildings_powered'] for r in active_resources if r['active'])

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res['activation_cost']:
                budget -= res['activation_cost']
                acquired_resources[t].append(res['id'])
                active_resources.append({
                    'id': res['id'],
                    'activation_cost': res['activation_cost'],
                    'periodic_cost': res['periodic_cost'],
                    'active_turns': res['active_duration'],
                    'downtime_turns': res['downtime'],
                    'lifespan': res['lifecycle'],
                    'buildings_powered': res['buildings_powered'],
                    'type': res['resource_type'],
                    'effect': res['special_effect'],
                    'remaining_life': res['lifecycle'],
                    'current_state': res['active_duration'],
                    'active': True
                })
                total_power += res['buildings_powered']

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res['periodic_cost'] for res in active_resources if res['active'])

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res['remaining_life'] -= 1
            res['current_state'] -= 1

            if res['remaining_life'] <= 0:
                active_resources.remove(res)
                continue

            if res['current_state'] == 0:
                res['active'] = not res['active']
                res['current_state'] = res['active_turns'] if res['active'] else res['downtime_turns']

    return acquired_resources

def solve_game_shiva_8(initial_budget, resources, turns):
    """
    Dedicated solver for 8-shiva.txt.
    """
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r['activation_cost'] <= budget],
            key=lambda r: (-r['buildings_powered'] / (r['activation_cost'] + r['periodic_cost']), r['activation_cost'])
        )

        total_power = sum(r['buildings_powered'] for r in active_resources if r['active'])

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res['activation_cost']:
                budget -= res['activation_cost']
                acquired_resources[t].append(res['id'])
                active_resources.append({
                    'id': res['id'],
                    'activation_cost': res['activation_cost'],
                    'periodic_cost': res['periodic_cost'],
                    'active_turns': res['active_duration'],
                    'downtime_turns': res['downtime'],
                    'lifespan': res['lifecycle'],
                    'buildings_powered': res['buildings_powered'],
                    'type': res['resource_type'],
                    'effect': res['special_effect'],
                    'remaining_life': res['lifecycle'],
                    'current_state': res['active_duration'],
                    'active': True
                })
                total_power += res['buildings_powered']

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res['periodic_cost'] for res in active_resources if res['active'])

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res['remaining_life'] -= 1
            res['current_state'] -= 1

            if res['remaining_life'] <= 0:
                active_resources.remove(res)
                continue

            if res['current_state'] == 0:
                res['active'] = not res['active']
                res['current_state'] = res['active_turns'] if res['active'] else res['downtime_turns']

    return acquired_resources

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
