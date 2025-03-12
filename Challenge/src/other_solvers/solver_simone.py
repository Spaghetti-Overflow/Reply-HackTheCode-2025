import sys

class Resource:
    def __init__(self, RI, RA, RP, RW, RM, RL, RU, RT, RE):
        self.id = RI
        self.activation_cost = RA
        self.periodic_cost = RP
        self.active_turns = RW
        self.downtime_turns = RM
        self.lifespan = RL
        self.buildings_powered = RU
        self.type = RT
        self.effect = RE
        self.remaining_life = RL
        self.current_state = RW
        self.active = True

def parse_input(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    initial_budget, R, T = map(int, lines[0].split())

    resources = []
    for i in range(1, R + 1):
        parts = lines[i].split()
        RI, RA, RP, RW, RM, RL, RU = map(int, parts[:7])
        RT = parts[7]
        RE = int(parts[8]) if len(parts) > 8 else 0
        resources.append(Resource(RI, RA, RP, RW, RM, RL, RU, RT, RE))

    turns = []
    for line in lines[R + 1:]:
        TM, TX, TR = map(int, line.split())
        turns.append({'TM': TM, 'TX': TX, 'TR': TR})

    return resources, turns, initial_budget


def run_game(resources, turns, initial_budget):
    budget = initial_budget
    acquired_resources = {}
    active_resources = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Buy resources strategically
        affordable_resources = sorted(
            [r for r in resources if r.activation_cost <= budget],
            key=lambda r: (-r.buildings_powered / (r.activation_cost + r.periodic_cost), r.activation_cost)
        )

        total_power = sum(r.buildings_powered for r in active_resources if r.active)

        for res in affordable_resources:
            if total_power >= TM:
                break
            if budget >= res.activation_cost:
                budget -= res.activation_cost
                acquired_resources[t].append(res.id)
                active_resources.append(Resource(
                    res.id, res.activation_cost, res.periodic_cost, res.active_turns,
                    res.downtime_turns, res.lifespan, res.buildings_powered, res.type, res.effect
                ))
                total_power += res.buildings_powered

        # Calculate profit
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res.periodic_cost for res in active_resources if res.active)

        # Update budget
        budget += profit - maintenance

        # Update resource lifespans and active/downtime state
        for res in active_resources[:]:
            res.remaining_life -= 1
            res.current_state -= 1

            if res.remaining_life <= 0:
                active_resources.remove(res)
                continue

            if res.current_state == 0:
                res.active = not res.active
                res.current_state = res.active_turns if res.active else res.downtime_turns

    return acquired_resources


def write_output(output_path, acquired_resources):
    with open(output_path, 'w') as file:
        for turn, resources in sorted(acquired_resources.items()):
            if resources:
                line = f"{turn} {len(resources)} {' '.join(map(str, resources))}\n"
                file.write(line)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python solver.py input.txt output.txt")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]
    resources, turns, initial_budget = parse_input(input_path)

    acquired_resources = run_game(resources, turns, initial_budget)
    write_output(output_path, acquired_resources)
