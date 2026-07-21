"""
Pre-spacetime constraint experiment.

Research question
-----------------
Can a system begin with only rules distinguishing permitted from forbidden
configurations, and produce an emergent ordering without assuming a clock?

This is a mathematical possibility test, not evidence about the actual
pre-Big-Bang universe.

The model uses established graph theory and partial-order mathematics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


Configuration = FrozenSet[str]


@dataclass(frozen=True)
class ConstraintRule:
    requires: FrozenSet[str]
    forbids: FrozenSet[str]

    def permits(self, state: Configuration) -> bool:
        return (
            self.requires.issubset(state)
            and self.forbids.isdisjoint(state)
        )


def valid_state(
    state: Configuration,
    incompatibilities: set[frozenset[str]],
) -> bool:
    """Return True when no forbidden pair appears together."""
    return all(
        not forbidden_pair.issubset(state)
        for forbidden_pair in incompatibilities
    )


def permitted_transition(
    source: Configuration,
    target: Configuration,
    incompatibilities: set[frozenset[str]],
) -> bool:
    """
    A permitted transition adds exactly one feature and never violates
    a compatibility constraint.

    No time variable is assumed.
    """
    added = target - source
    removed = source - target

    return (
        len(added) == 1
        and not removed
        and valid_state(target, incompatibilities)
    )


def build_transition_graph(
    states: set[Configuration],
    incompatibilities: set[frozenset[str]],
) -> dict[Configuration, set[Configuration]]:
    graph: dict[Configuration, set[Configuration]] = {
        state: set() for state in states
    }

    for source in states:
        for target in states:
            if permitted_transition(
                source,
                target,
                incompatibilities,
            ):
                graph[source].add(target)

    return graph


def emergent_depth(
    graph: dict[Configuration, set[Configuration]],
    origin: Configuration,
) -> dict[Configuration, int]:
    """
    Assign each reachable configuration a depth from the origin.

    Depth is not inserted as physical time. It emerges from the number of
    permitted changes required to reach a configuration.
    """
    depth = {origin: 0}
    frontier = [origin]

    while frontier:
        current = frontier.pop(0)

        for next_state in graph[current]:
            candidate_depth = depth[current] + 1

            if (
                next_state not in depth
                or candidate_depth < depth[next_state]
            ):
                depth[next_state] = candidate_depth
                frontier.append(next_state)

    return depth


def label(state: Configuration) -> str:
    if not state:
        return "∅"

    return "{" + ", ".join(sorted(state)) + "}"


def main() -> None:
    features = {"A", "B", "C"}

    incompatibilities = {
        frozenset({"A", "C"}),
    }

    states: set[Configuration] = set()

    feature_list = sorted(features)

    for mask in range(1 << len(feature_list)):
        state = frozenset(
            feature_list[index]
            for index in range(len(feature_list))
            if mask & (1 << index)
        )

        if valid_state(state, incompatibilities):
            states.add(state)

    graph = build_transition_graph(
        states,
        incompatibilities,
    )

    origin: Configuration = frozenset()
    depth = emergent_depth(graph, origin)

    assert frozenset({"A", "C"}) not in states
    assert depth[frozenset({"A", "B"})] == 2
    assert depth[frozenset({"B", "C"})] == 2

    print("Pre-Spacetime Constraint Experiment")
    print("-----------------------------------")
    print()
    print("Primitive assumptions:")
    print("1. Configurations may be possible or forbidden.")
    print("2. Some changes are permitted and others are not.")
    print("3. No coordinate system or clock is assumed.")
    print()
    print("Forbidden coexistence: A with C")
    print()

    print("Permitted configurations:")
    for state in sorted(
        states,
        key=lambda item: (len(item), sorted(item)),
    ):
        print(
            f"  depth={depth[state]}  state={label(state)}"
        )

    print()
    print("Permitted relations:")
    for source in sorted(
        graph,
        key=lambda item: (len(item), sorted(item)),
    ):
        for target in sorted(
            graph[source],
            key=lambda item: sorted(item),
        ):
            print(f"  {label(source)} -> {label(target)}")

    print()
    print("RESULT:")
    print(
        "An ordering can emerge from permitted relations "
        "without inserting a clock."
    )
    print()
    print("MATHEMATICAL STATUS:")
    print(
        "This construction uses existing graph and partial-order "
        "mathematics."
    )
    print(
        "It demonstrates logical possibility, not that constraints "
        "actually preceded the Big Bang."
    )
    print()
    print("PHYSICS TEST STILL REQUIRED:")
    print(
        "A real theory must derive measurable spacetime behavior and "
        "recover known physics."
    )


if __name__ == "__main__":
    main()
