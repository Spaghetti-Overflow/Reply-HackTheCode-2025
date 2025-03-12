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
        self.current_state = RW  # Starts active
        self.active = True

def parse_input(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    initial_budget, R, T = map(int, lines[0].split())
    resources = []
    for i in range(1, R + 1):
        parts = lines[i].split()
        RI = int(parts[0])
        RA = int(parts[1])
        RP = int(parts[2])
        RW = int(parts[3])
        RM = int(parts[4])
        RL = int(parts[5])
        RU = int(parts[6])
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
    accumulator_charge = 0  # Track stored buildings
    type_priority = {'B': 0, 'A': 1, 'D': 2, 'C': 3, 'E': 4, 'X': 5}

    for t, turn in enumerate(turns):
        TM, TX, TR = turn['TM'], turn['TX'], turn['TR']
        acquired_resources[t] = []

        # Calculate active resources' contributions and apply effects
        total_power = 0
        a_effect = 1.0  # Multiplier for total_power (A-type)
        b_effect = 1.0  # Multiplier for TM and TX (B-type)
        d_effect = 1.0  # Multiplier for TR (D-type)
        e_active = False

        for res in active_resources:
            if not res.active:
                continue
            total_power += res.buildings_powered
            # Apply special effects
            if res.type == 'A':
                a_effect *= (1 + res.effect / 100)
            elif res.type == 'B':
                b_effect *= (1 + res.effect / 100)
            elif res.type == 'D':
                d_effect *= (1 + res.effect / 100)
            elif res.type == 'E':
                e_active = True

        # Apply B-type effect first (modifies TM and TX)
        TM = max(0, int(TM * b_effect))
        TX = max(TM, int(TX * b_effect))  # Ensure TX >= TM

        # Apply A-type effect (modifies total_power)
        total_power = int(total_power * a_effect)

        # Apply D-type effect (modifies TR)
        TR = max(0, int(TR * d_effect))

        # Check if we can use accumulator to meet TM
        if e_active:
            surplus = total_power - TX
            if surplus > 0:
                accumulator_charge += surplus
            if total_power < TM:
                needed = TM - total_power
                use_charge = min(needed, accumulator_charge)
                total_power += use_charge
                accumulator_charge -= use_charge

        # Calculate profit before purchasing new resources
        buildings_served = min(total_power, TX)
        profit = buildings_served * TR if buildings_served >= TM else 0

        # Maintenance costs
        maintenance = sum(res.periodic_cost for res in active_resources if res.active)
        budget += profit - maintenance

        # Purchase new resources
        affordable = [r for r in resources if r.activation_cost <= budget and r.remaining_life > 0]
        affordable.sort(key=lambda x: (
            type_priority.get(x.type, 5),
            -1 if x.effect > 0 else 0,  # Green first
            -calculate_score(x, TR, a_effect, d_effect, e_active)
        ))

        purchased = []
        for res in affordable:
            if budget < res.activation_cost:
                continue

            # Apply C-type effects to new resource's lifespan
            c_modifier = 1.0
            for c_res in active_resources:
                if c_res.type == 'C' and c_res.active and c_res.effect > 0:
                    c_modifier *= (1 + c_res.effect / 100)
            new_rl = max(1, int(res.lifespan * c_modifier))
            new_res = Resource(
                res.id,
                res.activation_cost,
                res.periodic_cost,
                res.active_turns,
                res.downtime_turns,
                new_rl,
                res.buildings_powered,
                res.type,
                res.effect
            )
            new_res.remaining_life = new_rl

            if budget >= new_res.activation_cost:
                budget -= new_res.activation_cost
                purchased.append(new_res.id)
                active_resources.append(new_res)
                # Apply immediate effects if active
                if new_res.active:
                    if new_res.type == 'A':
                        a_effect *= (1 + new_res.effect / 100)
                    elif new_res.type == 'B':
                        b_effect *= (1 + new_res.effect / 100)
                        TM = max(0, int(TM * (1 + new_res.effect / 100)))
                        TX = max(TM, int(TX * (1 + new_res.effect / 100)))
                    elif new_res.type == 'D':
                        d_effect *= (1 + new_res.effect / 100)
                    elif new_res.type == 'E':
                        e_active = True

        acquired_resources[t] = purchased

        # Update resource states and lifespan
        for res in active_resources[:]:
            res.remaining_life -= 1
            res.current_state -= 1

            if res.remaining_life <= 0:
                if res.type == 'E':
                    has_e = any(r.type == 'E' and r.remaining_life > 0 for r in active_resources if r != res)
                    if not has_e:
                        accumulator_charge = 0
                active_resources.remove(res)
                continue

            if res.current_state == 0:
                res.active = not res.active
                res.current_state = res.active_turns if res.active else res.downtime_turns

    return acquired_resources

def calculate_score(resource, TR, a_effect, d_effect, e_active):
    base_profit = resource.buildings_powered * TR * a_effect * d_effect
    lifespan_value = resource.lifespan / (resource.active_turns + resource.downtime_turns)
    cost_penalty = resource.activation_cost + resource.periodic_cost * resource.lifespan

    effect_bonus = 1.0
    if resource.type == 'B':
        effect_bonus *= (1 + resource.effect / 100) if resource.effect > 0 else 0.5
    elif resource.type == 'C' and resource.effect > 0:
        effect_bonus *= 1.5
    elif resource.type == 'E' and e_active:
        effect_bonus *= 2.0
    elif resource.type in ['A', 'D']:
        effect_bonus *= 1.2 if resource.effect > 0 else 0.8

    score = (base_profit * lifespan_value * effect_bonus) / (cost_penalty + 1)
    return score

def write_output(output_path, acquired_resources):
    with open(output_path, 'w') as file:
        for turn in sorted(acquired_resources.keys()):
            resources = acquired_resources[turn]
            if resources:
                file.write(f"{turn} {len(resources)} {' '.join(map(str, resources))}\n")