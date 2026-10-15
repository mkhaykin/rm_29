import pytest

from strategy import StrategyFAFR


@pytest.mark.parametrize(
    "available_qty, requested_qty, results",
    [
        (10, (1, 1, 1), (1, 1, 1)),
        (10, (10, 1, 1), (10, 0, 0)),
        (10, (0, 1, 1), (0, 1, 1)),
        (10, (0, 1, 10), (0, 1, 9)),
        (0, (1, 1, 1), (0, 0, 0)),
    ],
)
def test_fafr(
    create_requests,
    available_qty: int,
    requested_qty: tuple[int, ...],
    results: tuple[int, ...],
) -> None:
    strategy = StrategyFAFR(
        available_qty,
        create_requests(requested_qty),
    )
    ans = list(strategy.calc().values())
    for result, expected in zip(ans, results):
        assert result == expected


def test_fafr_min_lot(
    create_requests,
) -> None:
    """Пропустим первый потому как не хватает"""
    strategy = StrategyFAFR(
        5,
        create_requests(
            (10, 1, 1),
            min_lot=(6, 0, 0),
        ),
    )
    ans = list(strategy.calc().values())
    assert ans[0] == 0
    assert ans[1] == 1
    assert ans[2] == 1


def test_fafr_rounding(
    create_requests,
) -> None:
    """В первом возьмем до кратного"""
    strategy = StrategyFAFR(
        5,
        create_requests(
            (10, 1, 1),
            rounding_value=(2, 0, 0),
        ),
    )
    ans = list(strategy.calc().values())
    assert ans[0] == 4
    assert ans[1] == 1
    assert ans[2] == 0


def test_fafr_combine(
    create_requests,
) -> None:
    """Берем первый, пропускаем второй и сколько можем на третий"""
    strategy = StrategyFAFR(
        7,
        create_requests(
            (10, 1, 10),
            min_lot=(5, 2, 0),
            rounding_value=(2, 0, 0),
        ),
    )
    ans = list(strategy.calc().values())
    assert ans[0] == 6
    assert ans[1] == 0
    assert ans[2] == 1


def test_fafr_combine_skip_first(
    create_requests,
) -> None:
    strategy = StrategyFAFR(
        5,
        create_requests(
            (10, 1, 1),
            min_lot=(5, 0, 0),
            rounding_value=(4, 0, 0),
        ),
    )
    ans = list(strategy.calc().values())
    assert ans[0] == 0
    assert ans[1] == 1
    assert ans[2] == 1
