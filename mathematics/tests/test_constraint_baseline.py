from mathematics.constraint_algebra import Constraint


UNIVERSE = {"stable", "degraded", "recovering", "failed"}


def c(*states: str) -> Constraint:
    return Constraint(UNIVERSE, states)


def test_merge_is_intersection():
    first = c("stable", "degraded", "recovering")
    second = c("stable", "recovering")

    result = first.merge(second)

    assert result.allowed == frozenset(
        {"stable", "recovering"}
    )


def test_release_is_union():
    first = c("stable", "degraded")
    second = c("recovering")

    result = first.release(second)

    assert result.allowed == frozenset(
        {"stable", "degraded", "recovering"}
    )


def test_merge_is_commutative():
    first = c("stable", "degraded")
    second = c("stable", "recovering")

    assert first.merge(second) == second.merge(first)


def test_merge_is_associative():
    first = c("stable", "degraded", "recovering")
    second = c("stable", "recovering")
    third = c("stable")

    left = first.merge(second).merge(third)
    right = first.merge(second.merge(third))

    assert left == right


def test_merge_is_idempotent():
    item = c("stable", "recovering")

    assert item.merge(item) == item


def test_additional_constraint_never_increases_capacity():
    first = c("stable", "degraded", "recovering")
    second = c("stable", "recovering")

    result = first.merge(second)

    assert result.capacity <= first.capacity
    assert result.capacity <= second.capacity


def test_pressure_rises_when_states_are_removed():
    weaker = c("stable", "degraded", "recovering")
    stronger = c("stable")

    assert stronger.pressure > weaker.pressure


def test_impossible_state_is_not_viable():
    impossible = c()

    assert impossible.viable is False
    assert impossible.pressure == 1.0
