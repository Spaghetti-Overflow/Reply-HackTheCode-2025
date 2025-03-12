import numpy as np

# Load the data from the input file
def load_game_data(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    # Read the initial budget, number of resources, and number of turns
    D, R, T = map(int, lines[0].split())

    # Read the available resources
    resources = []
    for i in range(1, R + 1):
        data = lines[i].split()
        resource = {
            "RI": int(data[0]),
            "RA": int(data[1]),
            "RP": int(data[2]),
            "RW": int(data[3]),
            "RM": int(data[4]),
            "RL": int(data[5]),
            "RU": int(data[6]),
            "RT": data[7],
            "RE": int(data[8]) if len(data) > 8 else 0
        }
        resources.append(resource)

    # Read the turns
    turns = []
    for i in range(R + 1, R + 1 + T):
        TM, TX, TR = map(int, lines[i].split())
        turns.append({"TM": TM, "TX": TX, "TR": TR})

    return D, resources, turns

# Simulate the game
def simulate_game(D, resources, turns):
    active_resources = []
    budget = D
    output = []

    for t, turn in enumerate(turns):
        TM, TX, TR = turn["TM"], turn["TX"], turn["TR"]

        # Activate new resources if possible
        affordable_resources = [r for r in resources if r["RA"] <= budget]
        affordable_resources.sort(key=lambda r: r["RU"] / r["RP"], reverse=True)  # Sort by efficiency

        purchased = []
        while affordable_resources and budget > 0:
            best_resource = affordable_resources.pop(0)
            if budget >= best_resource["RA"]:
                budget -= best_resource["RA"]
                active_resources.append({
                    "RI": best_resource["RI"],
                    "RU": best_resource["RU"],
                    "RW": best_resource["RW"],
                    "RP": best_resource["RP"],
                    "remaining_life": best_resource["RL"],
                    "remaining_active_turns": best_resource["RW"]
                })
                purchased.append(best_resource["RI"])

        if purchased:
            output.append(f"{t} {len(purchased)} " + " ".join(map(str, purchased)))

        # Calculate the number of buildings powered
        active_resources = [r for r in active_resources if r["remaining_life"] > 0]
        total_powered = sum(r["RU"] for r in active_resources if r["remaining_active_turns"] > 0)

        if total_powered >= TM:
            profit = min(total_powered, TX) * TR
        else:
            profit = 0

        # Update the budget and active resources
        maintenance_cost = sum(r["RP"] for r in active_resources if r["remaining_active_turns"] > 0)
        budget += profit - maintenance_cost

        for r in active_resources:
            r["remaining_life"] -= 1
            if r["remaining_active_turns"] > 0:
                r["remaining_active_turns"] -= 1
            elif r["remaining_active_turns"] == 0:
                r["remaining_active_turns"] = r["RW"]

    return output

# Run the code
# filename = "0-demo.txt"
# filename = "1-thunberg.txt"
# filename = "2-attenborough.txt"
filename = "3-goodall.txt"
# filename = "4-maathai.txt"
# filename = "6-earle.txt"
# filename = "8-shiva.txt"

D, resources, turns = load_game_data(filename)
output = simulate_game(D, resources, turns)

# Print
for line in output:
    print(line)

# Save the output to a text file
output_filename = filename.replace(".txt", "_output.txt")

with open(output_filename, "w", encoding="utf-8") as f:
    for line in output:
        f.write(line + "\n")

print(f"Output saved in {output_filename}")
