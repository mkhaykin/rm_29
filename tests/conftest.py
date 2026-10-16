import itertools
from typing import Optional

import pytest

from strategy import RequestRaw


@pytest.fixture
def create_requests():
    # генерим список запросов на основании переданных списков.
    # Длины выравниваем по самому большому.
    def _create(
        demand_qty: list[int],
        *,
        priority: Optional[list[int]] = None,
        min_lot: Optional[list[int]] = None,
        rounding_value: Optional[list[int]] = None,
    ) -> list[RequestRaw]:
        requests = []
        d_iter = itertools.chain(demand_qty, itertools.repeat(0))
        p_iter = itertools.chain(priority or [], itertools.repeat(1))
        m_iter = itertools.chain(min_lot or [], itertools.repeat(0))
        r_iter = itertools.chain(rounding_value or [], itertools.repeat(0))

        n = max(len(demand_qty), len(priority or []), len(min_lot or []), len(rounding_value or []))
        _zip = zip(d_iter, p_iter, m_iter, r_iter)
        for i in range(1, n + 1):
            d, p, m, r = next(_zip)
            requests.append(
                RequestRaw(
                    dest_location=f"LOC{i}",
                    case_id="SOME_CASE",
                    request_id=f"R-{i:03}",
                    demand_qty=d,
                    priority=p,
                    min_lot=m,
                    rounding_value=r,
                )
            )
        return requests

    return _create
