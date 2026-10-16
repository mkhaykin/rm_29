from typing import List

from reader import RequestRaw, SupplyRaw


def print_result(
    supply: SupplyRaw,
    requests: List[RequestRaw],
    result: dict[str, int],
) -> None:
    if len(requests) != len(result):
        raise ValueError("Проблема размерности запросов и результата")

    print(f"{'запрос':<10} | {'запрошено':<10} | {'получено':<10} | {'дельта':<10} |")
    sum_delivered_qty = 0
    sum_demand_qty = 0
    for request in requests:
        sum_delivered_qty += result[request.request_id]
        sum_demand_qty += request.demand_qty
        print(
            f"{request.request_id:<10} | "
            f"{request.demand_qty:>10} | "
            f"{result[request.request_id]:>10} | "
            f"{(request.demand_qty - result[request.request_id]):>10} |",
        )
    print(
        f"Запрошено всего: {sum_demand_qty}, "
        f"распределено {sum_delivered_qty}, "
        f"остаток {supply.available_qty - sum_delivered_qty}",
    )
    print("=" * 51)
