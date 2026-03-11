import random

WORLD_SIZE = 12
FOOD_COUNT = 25
STARTING_AGENTS = 6
ROUNDS = 60

REPRODUCE_ENERGY = 18
START_ENERGY = 10
FOOD_ENERGY = 6


class Agent:
    def __init__(self, x, y, move_bias=None):
        self.x = x
        self.y = y
        self.energy = START_ENERGY

        # move_bias controls how likely the agent is to move
        # 0.0 = rests more, 1.0 = moves a lot
        if move_bias is None:
            self.move_bias = random.uniform(0.3, 0.9)
        else:
            self.move_bias = move_bias

    def act(self):
        # sometimes rest, sometimes move
        if random.random() < self.move_bias:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            self.x = max(0, min(WORLD_SIZE - 1, self.x + dx))
            self.y = max(0, min(WORLD_SIZE - 1, self.y + dy))
            self.energy -= 1
            return "move"
        else:
            self.energy -= 0.3
            return "rest"

    def can_reproduce(self):
        return self.energy >= REPRODUCE_ENERGY

    def reproduce(self):
        # parent gives some energy to child
        self.energy -= 8

        # mutation: child gets slightly changed move_bias
        child_bias = self.move_bias + random.uniform(-0.1, 0.1)
        child_bias = max(0.05, min(0.95, child_bias))

        child = Agent(self.x, self.y, move_bias=child_bias)
        child.energy = 8
        return child


def create_food():
    food = set()
    while len(food) < FOOD_COUNT:
        food.add((
            random.randint(0, WORLD_SIZE - 1),
            random.randint(0, WORLD_SIZE - 1)
        ))
    return food


def create_agents():
    agents = []
    for _ in range(STARTING_AGENTS):
        agents.append(
            Agent(
                random.randint(0, WORLD_SIZE - 1),
                random.randint(0, WORLD_SIZE - 1)
            )
        )
    return agents


def show_stats(round_num, agents, food):
    print(f"\n===== ROUND {round_num} =====")
    print("Agents alive:", len(agents))
    print("Food on map:", len(food))

    if agents:
        avg_energy = sum(a.energy for a in agents) / len(agents)
        avg_bias = sum(a.move_bias for a in agents) / len(agents)
        print("Average energy:", round(avg_energy, 2))
        print("Average move bias:", round(avg_bias, 2))

        top = sorted(agents, key=lambda a: a.energy, reverse=True)[:3]
        print("Top agents:")
        for i, a in enumerate(top, start=1):
            print(
                f"  {i}. Pos=({a.x},{a.y}) "
                f"Energy={round(a.energy,1)} "
                f"MoveBias={round(a.move_bias,2)}"
            )


def run():
    agents = create_agents()
    food = create_food()

    for round_num in range(1, ROUNDS + 1):
        newborns = []

        for agent in agents:
            agent.act()

            # eat if food is on current tile
            if (agent.x, agent.y) in food:
                agent.energy += FOOD_ENERGY
                food.remove((agent.x, agent.y))
                print(
                    f"Agent at ({agent.x},{agent.y}) ate food. "
                    f"Energy now {round(agent.energy,1)}"
                )

            # reproduce if strong enough
            if agent.can_reproduce():
                child = agent.reproduce()
                newborns.append(child)
                print(
                    f"Agent at ({agent.x},{agent.y}) reproduced. "
                    f"Child move_bias={round(child.move_bias,2)}"
                )

        # add children
        agents.extend(newborns)

        # remove dead agents
        agents = [a for a in agents if a.energy > 0]

        # refill food
        while len(food) < FOOD_COUNT:
            food.add((
                random.randint(0, WORLD_SIZE - 1),
                random.randint(0, WORLD_SIZE - 1)
            ))

        show_stats(round_num, agents, food)

        if not agents:
            print("\nAll agents died.")
            break

    print("\n===== FINAL RESULT =====")
    print("Final population:", len(agents))
    if agents:
        best = max(agents, key=lambda a: a.energy)
        print(
            f"Strongest agent -> Energy: {round(best.energy,1)}, "
            f"MoveBias: {round(best.move_bias,2)}, "
            f"Position: ({best.x},{best.y})"
        )


if __name__ == "__main__":
    run()
