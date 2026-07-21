"""
Relational spacetime experiment.

Question
--------
Can permitted constraint relations generate structures resembling:

1. causal order;
2. relational distance;
3. causal separation;

without assuming coordinates, meters, or an external clock?

This is a mathematical model using directed graphs and partial orders.
It is not evidence that physical spacetime actually emerged this way.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import FrozenSet


Configuration = FrozenSet[str]


@dataclass(frozen=True)
class RelationResult:
    source: Configuration
    target: Configuration
    reachable: bool
    distance: int | None


def label(state: Configuration) -> str:
    if not state:
        return "∅"

    return "{" + ", ".join(sorted(state)) + "}"


def valid_state(
    state: Configuration,
    forbidden_pairs: set[FrozenSet[str]],
) -> bool:
    return all(
        not pair.issubset(state)
        for pair in forbidden_pairs
    )


def build_states(
    features: set[str],
    forbidden_pairs: set[FrozenSet[str]],
) -> set[Configuration]:
    feature_list = sorted(features)
    states: set[Configuration] = set()

    for mask in range(1 << len(feature_list)):
        state = frozenset(
            feature_list[index]
            for index in range(len(feature_list))
            if mask & (1 << index)
        )

        if valid_state(state, forbidden_pairs):
            states.add(state)

    return states


def permitted_transition(
    source: Configuration,
    target: Configuration,
    forbidden_pairs: set[FrozenSet[str]],
) -> bool:
    added = target - source
    removed = source - target

    return (
        len(added) == 1
        and not removed
        and valid_state(target, forbidden_pairs)
    )


def build_graph(
    states: set[Configuration],
    forbidden_pairs: set[FrozenSet[str]],
) -> dict[Configuration, set[Configuration]]:
    return {
        source: {
            target
            for target in states
            if permitted_transition(
                source,
                target,
                forbidden_pairs,
            )
        }
        for source in states
    }


def relational_distance(
    graph: dict[Configuration, set[Configuration]],
    source: Configuration,
    target: Configuration,
) -> RelationResult:
    if source == target:
        return RelationResult(source, target, True, 0)

    queue = deque([(source, 0)])
    visited = {source}

    while queue:
        current, distance = queue.popleft()

        for neighbor in graph[current]:
            if neighbor == target:
                return RelationResult(
                    source,
                    target,
                    True,
                    distance + 1,
                )

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

    return RelationResult(source, target, False, None)


def main() -> None:
    features = {"A", "B", "C", "D"}

    forbidden_pairs = {
        frozenset({"A", "C"}),
        frozenset({"B", "D"}),
    }

    states = build_states(
        features,
        forbidden_pairs,
    )

    graph = build_graph(
        states,
        forbidden_pairs,
    )

    origin = frozenset()
    ab = frozenset({"A", "B"})
    cd = frozenset({"C", "D"})
    a = frozenset({"A"})

    origin_to_ab = relational_distance(
        graph,
        origin,
        ab,
    )

    a_to_ab = relational_distance(
        graph,
        a,
        ab,
    )

    ab_to_cd = relational_distance(
        graph,
        ab,
        cd,
    )

    assert origin_to_ab.reachable
    assert origin_to_ab.distance == 2

    assert a_to_ab.reachable
    assert a_to_ab.distance == 1

    assert not ab_to_cd.reachable
    assert ab_to_cd.distance is None

    print("GV Relational Spacetime Experiment")
    print("----------------------------------")
    print()
    print("No coordinates were assigned.")
    print("No external clock was assigned.")
    print("Only permitted and forbidden relations were defined.")
    print()

    print("RELATIONAL DISTANCE")
    print(
        f"{label(origin)} -> {label(ab)}"
        f" = {origin_to_ab.distance} permitted changes"
    )
    print(
        f"{label(a)} -> {label(ab)}"
        f" = {a_to_ab.distance} permitted change"
    )
    print()

    print("CAUSAL SEPARATION")
    print(
        f"{label(ab)} -> {label(cd)}"
        f" reachable = {ab_to_cd.reachable}"
    )
    print()

    print("RESULT:")
    print(
        "Permitted relations generate an ordering and a "
        "shortest-path distance."
    )
    print(
        "Some configurations are causally connected; "
        "others are separated."
    )
    print()

    print("MATHEMATICAL STATUS:")
    print(
        "These structures are already described by directed "
        "graphs, partial orders, and graph metrics."
    )
    print(
        "This is a relational precursor to spacetime, "
        "not physical spacetime itself."
    )
    print()

    print("NEXT PHYSICS HURDLE:")
    print(
        "Derive a continuum limit, invariant causal structure, "
        "and behavior resembling known spacetime geometry."
    )


if __name__ == "__main__":
    main()
