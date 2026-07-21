"""
Spontaneous Dimension Audit

Research question
-----------------
Can simple local constraint rules generate a network with a stable,
finite effective dimension without specifying that dimension in advance?

No coordinates, lattice, or target dimension are supplied.

Important
---------
This is an exploratory graph experiment using established mathematics.
A stable estimate would not prove physical spacetime emerged.
An unstable estimate is also valuable: it shows that generic constraints
alone are insufficient to produce geometric structure.
"""

from __future__ import annotations

from collections import deque
from math import log
from random import Random


Graph = dict[int, set[int]]


def add_edge(graph: Graph, first: int, second: int) -> None:
    if first == second:
        return

    graph.setdefault(first, set()).add(second)
    graph.setdefault(second, set()).add(first)


def generate_constraint_network(
    node_count: int,
    maximum_degree: int,
    seed: int,
) -> Graph:
    """
    Grow a graph using only a local capacity constraint.

    Each new node:
    - attaches to one or two existing nodes;
    - cannot connect to nodes already at maximum degree;
    - favors lower-degree nodes.

    No spatial coordinates are used.
    """
    if node_count < 2:
        raise ValueError("node_count must be at least 2")

    if maximum_degree < 2:
        raise ValueError("maximum_degree must be at least 2")

    rng = Random(seed)
    graph: Graph = {0: set(), 1: set()}
    add_edge(graph, 0, 1)

    for new_node in range(2, node_count):
        graph[new_node] = set()

        eligible = [
            node
            for node in range(new_node)
            if len(graph[node]) < maximum_degree
        ]

        if not eligible:
            raise RuntimeError("no eligible attachment nodes remain")

        attachment_count = 1

        if len(eligible) > 1 and rng.random() < 0.45:
            attachment_count = 2

        weighted_pool: list[int] = []

        for node in eligible:
            remaining_capacity = maximum_degree - len(graph[node])
            weighted_pool.extend([node] * remaining_capacity)

        chosen: set[int] = set()

        while (
            weighted_pool
            and len(chosen) < attachment_count
        ):
            chosen.add(rng.choice(weighted_pool))

        for target in chosen:
            add_edge(graph, new_node, target)

    return graph


def graph_ball_size(
    graph: Graph,
    origin: int,
    radius: int,
) -> int:
    visited = {origin}
    queue = deque([(origin, 0)])

    while queue:
        node, distance = queue.popleft()

        if distance >= radius:
            continue

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

    return len(visited)


def local_dimension_estimates(
    graph: Graph,
    origin: int,
    radii: range,
) -> list[tuple[int, int, float | None]]:
    samples = [
        (radius, graph_ball_size(graph, origin, radius))
        for radius in radii
    ]

    results: list[tuple[int, int, float | None]] = []

    previous_radius = None
    previous_volume = None

    for radius, volume in samples:
        estimate = None

        if (
            previous_radius is not None
            and previous_volume is not None
            and volume > previous_volume
        ):
            estimate = (
                log(volume / previous_volume)
                / log(radius / previous_radius)
            )

        results.append((radius, volume, estimate))
        previous_radius = radius
        previous_volume = volume

    return results


def estimate_stability(
    estimates: list[float],
) -> tuple[float, float]:
    mean = sum(estimates) / len(estimates)

    spread = max(estimates) - min(estimates)

    return mean, spread


def main() -> None:
    node_count = 2500
    maximum_degree = 4
    seeds = (7, 19, 41)
    radii = range(2, 9)

    print("GV Spontaneous Dimension Audit")
    print("------------------------------")
    print()
    print(f"Nodes              : {node_count}")
    print(f"Maximum degree     : {maximum_degree}")
    print("Coordinates        : none")
    print("Target dimension   : none")
    print()

    run_means: list[float] = []
    run_spreads: list[float] = []

    for seed in seeds:
        graph = generate_constraint_network(
            node_count=node_count,
            maximum_degree=maximum_degree,
            seed=seed,
        )

        origin = 0

        results = local_dimension_estimates(
            graph,
            origin,
            radii,
        )

        numerical_estimates = [
            estimate
            for _, _, estimate in results
            if estimate is not None
        ]

        mean, spread = estimate_stability(
            numerical_estimates
        )

        run_means.append(mean)
        run_spreads.append(spread)

        print(f"Seed {seed}")
        print("radius  reachable  local dimension")

        for radius, volume, estimate in results:
            estimate_text = (
                "---"
                if estimate is None
                else f"{estimate:.3f}"
            )

            print(
                f"{radius:>6}"
                f"{volume:>11}"
                f"{estimate_text:>17}"
            )

        print(f"Mean estimate       : {mean:.3f}")
        print(f"Within-run spread   : {spread:.3f}")
        print()

    between_run_spread = max(run_means) - min(run_means)
    average_local_spread = sum(run_spreads) / len(run_spreads)

    stable = (
        between_run_spread < 0.35
        and average_local_spread < 0.75
    )

    print("CROSS-RUN AUDIT")
    print(f"Between-run spread  : {between_run_spread:.3f}")
    print(f"Average local spread: {average_local_spread:.3f}")
    print(f"Stable dimension    : {stable}")
    print()

    print("VERDICT:")

    if stable:
        print(
            "These local rules produced an approximately stable "
            "effective growth dimension."
        )
        print(
            "The result must still be tested across network sizes, "
            "rules, and alternative estimators."
        )
    else:
        print(
            "These generic local constraints did not produce a "
            "stable finite dimension."
        )
        print(
            "Constraint alone is insufficient; additional organizing "
            "principles would be required."
        )

    print()
    print("MATHEMATICAL STATUS:")
    print(
        "This is ordinary random-graph growth analysis."
    )
    print(
        "It tests whether dimension appears; it does not assume "
        "that appearance proves new mathematics or physics."
    )


if __name__ == "__main__":
    main()
