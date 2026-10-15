import pytest

from strategy import StrategyZero


@pytest.mark.parametrize(
    "available_qty, requested_qty, results",
    [
        (10, (1, 1, 1), (0, 0, 0)),
        (0, (1, 1, 1), (0, 0, 0)),
    ],
)
def test_fafr(
    create_requests,
    available_qty: int,
    requested_qty: tuple[int, ...],
    results: tuple[int, ...],
) -> None:
    strategy = StrategyZero(
        available_qty,
        create_requests(requested_qty),
    )
    ans = list(strategy.calc().values())
    for result, expected in zip(ans, results):
        assert result == expected
