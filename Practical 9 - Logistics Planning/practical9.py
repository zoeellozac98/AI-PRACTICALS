
import heapq
from itertools import count

# AI Practical 9
# Logistics Planning using UCS and STRIPS-style actions


# Road network: each road has a travel cost.
# Roads are bidirectional.
roads = {
    "Warehouse": {"Junction": 2, "Market": 5},
    "Junction": {"Warehouse": 2, "Hospital": 4, "Market": 2},
    "Market": {"Warehouse": 5, "Junction": 2, "Delivery Point": 3},
    "Hospital": {"Junction": 4, "Delivery Point": 2},
    "Delivery Point": {"Market": 3, "Hospital": 2}
}

START = "Warehouse"
DELIVERY = "Delivery Point"


# State = (robot_location, package_delivered)
INITIAL_STATE = (START, False)
GOAL_STATE = (START, True)


def get_actions(state):
    """Return actions whose STRIPS-style preconditions are satisfied."""
    location, delivered = state
    actions = []

    # Move actions: the robot must be at the source,
    # and a road to the destination must exist.
    for destination, cost in roads[location].items():
        actions.append({
            "name": f"Move from {location} to {destination}",
            "preconditions": [
                ("At", location),
                ("Road", location, destination)
            ],
            "add": [("At", destination)],
            "delete": [("At", location)],
            "next_state": (destination, delivered),
            "cost": cost
        })

    # Deliver action: robot must be at the delivery point
    # and the package must not already be delivered.
    if location == DELIVERY and not delivered:
        actions.append({
            "name": "Deliver package",
            "preconditions": [
                ("At", DELIVERY),
                ("PackageDelivered", False)
            ],
            "add": [("PackageDelivered", True)],
            "delete": [("PackageDelivered", False)],
            "next_state": (location, True),
            "cost": 0
        })

    return actions


def uniform_cost_search(initial_state, goal_state):
    """Find the lowest-cost sequence of planning actions."""
    sequence = count()
    frontier = [(0, next(sequence), initial_state, [])]
    best_cost = {initial_state: 0}

    while frontier:
        cost, _, state, path = heapq.heappop(frontier)

        # Ignore outdated entries in the priority queue.
        if cost != best_cost.get(state):
            continue

        # The goal requires both return and completed delivery.
        if state == goal_state:
            return cost, path

        for action in get_actions(state):
            next_state = action["next_state"]
            new_cost = cost + action["cost"]

            if new_cost < best_cost.get(next_state, float("inf")):
                best_cost[next_state] = new_cost
                new_path = path + [action]

                heapq.heappush(
                    frontier,
                    (new_cost, next(sequence), next_state, new_path)
                )

    return None, []


def main():
    print("=" * 55)
    print("PRACTICAL 9: LOGISTICS PLANNING USING UCS AND STRIPS")
    print("=" * 55)

    print(f"Initial state: {INITIAL_STATE}")
    print(f"Goal state:    {GOAL_STATE}")
    print("\nSearching for the minimum-cost delivery plan...\n")

    total_cost, plan = uniform_cost_search(INITIAL_STATE, GOAL_STATE)

    if total_cost is None:
        print("No valid plan found.")
        return

    current_state = INITIAL_STATE
    print("PLAN FOUND:\n")

    for step, action in enumerate(plan, start=1):
        print(f"Step {step}: {action['name']}")
        print(f"  Preconditions: {action['preconditions']}")
        print(f"  Add effects:   {action['add']}")
        print(f"  Delete effects:{action['delete']}")
        print(f"  Action cost:   {action['cost']}")

        current_state = action["next_state"]
        print(f"  New state:     {current_state}\n")

    print("-" * 55)
    print(f"Minimum total travel cost: {total_cost}")
    print(f"Final state: {current_state}")

    if current_state == GOAL_STATE:
        print("Goal achieved: package delivered and robot returned!")
    else:
        print("Goal not achieved.")


if __name__ == "__main__":
    main()
