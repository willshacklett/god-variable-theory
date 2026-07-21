"""
Emergent Dimension Baseline

Research question
-----------------
Can intrinsic dimension be estimated from connectivity alone after a
network has been constructed?

Important:
The example networks are generated from known 1D, 2D, and 3D lattices.
Therefore this experiment does not derive physical dimension from first
principles.

The estimator receives only adjacency relationships. It does not receive
coordinates or the network's known dimension.
"""

from __future__ import annotations

from collections import deque
from math import log
from typing import Hashable


Node = Hashable
Graph = dict[Node, set[Node]]


def add_edge(graph: Graph, first: Node, second: Node) -> None:
    graph.setdefault(first, set()).add(second)
    graph.setdefault(second, set()).add(first)


def build_lattice(dimension: int, width: int) -> Graph:
    if dimension not in {1, 2, 3}:
        raise ValueError("dimension must be 1, 2, or 3")

    graph: Graph = {}

    if dimension == 1:
        nodes = [(x,) for x in range(width)]
    elif dimension == 2:
        nodes = [
            (x, y)
            for x in range(width)
            for y in range(width)
        ]
    else:
        nodes = [
            (x, y, z)
            for x in range(width)
            for y in range(width)
            for z in range(width)
        ]

    node_set = set(nodes)

    for node in nodes:
        graph.setdefault(node, set())

        for axis in range(dimension):
            neighbor = list(node)
            neighbor[axis] += 1
            neighbor_tuple = tuple(neighbor)

            if neighbor_tuple in node_set:
                add_edge(graph, node, neighbor_tuple)

    return graph


def graph_ball_size(
    graph: Graph,
    origin: Node,
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


def estimate_growth_dimension(
    graph: Graph,
    origin: Node,
    radii: range,
) -> tuple[float, list[tuple[int, int]]]:
    samples = [
        (radius, graph_ball_size(graph, origin, radius))
        for radius in radii
    ]

    log_r = [log(radius) for radius, _ in samples]
    log_v = [log(volume) for _, volume in samples]

    mean_r = sum(log_r) / len(log_r)
    mean_v = sum(log_v) / len(log_v)

    numerator = sum(
        (r - mean_r) * (v - mean_v)
        for r, v in zip(log_r, log_v)
    )

    denominator = sum(
        (r - mean_r) ** 2
        for r in log_r
    )

    dimension = numerator / denominator

    return dimension, samples


def center_node(dimension: int, width: int) -> tuple[int, ...]:
    midpoint = width // 2
    return tuple(midpoint for _ in range(dimension))


def main() -> None:
    width = 31
    radii = range(2, 8)

    print("GV Emergent Dimension Baseline")
    print("------------------------------")
    print()
    print("The estimator receives adjacency only.")
    print("It is not told the coordinates or known dimension.")
    print()

    estimates = {}

    for known_dimension in (1, 2, 3):
        graph = build_lattice(
            dimension=known_dimension,
            width=width,
        )

        origin = center_node(
            dimension=known_dimension,
            width=width,
        )

        estimate, samples = estimate_growth_dimension(
            graph,
            origin,
            radii,
        )

        estimates[known_dimension] = estimate

        print(f"Known lattice dimension: {known_dimension}")
        print(f"Estimated growth dimension: {estimate:.3f}")
        print("Radius-volume samples:")

        for radius, volume in samples:
            print(f"  r={radius}  nodes={volume}")

        print()

    assert 0.7 < estimates[1] < 1.4
    assert 1.4 < estimates[2] < 2.5
    assert 2.2 < estimates[3] < 3.6

    print("RESULT:")
    print(
        "Connectivity growth distinguishes networks with different "
        "intrinsic dimensions."
    )
    print()
    print("MATHEMATICAL STATUS:")
    print(
        "This is established graph-growth mathematics, not new "
        "mathematics or new physics."
    )
    print()
    print("LIMITATION:")
    print(
        "The lattices were constructed from known dimensions. "
        "We inferred dimension; we did not derive why a constraint "
        "system should produce a particular dimension."
    )
    print()
    print("NEXT TEST:")
    print(
        "Generate networks from constraint rules alone, then measure "
        "whether a stable dimension appears without selecting one."
    )


if __name__ == "__main__":
    main()
