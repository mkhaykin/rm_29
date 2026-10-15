from reader import RequestRaw


def penalty(
    requests: list[RequestRaw],
    result: dict[str, int],
) -> int:
    """
    идея в том, что у нас есть некая функция штрафа, для оценки результатов расчета.
    пока принял следующий вариант:
        не выполнили заказ - 100 очков штрафа;
        так же к штрафу добавляем процент расхождения. Т.е. штрафуем и за превышение, но
        пока все стратегии не превышают.
    """
    ans = 0
    for request in requests:
        if request.demand_qty != 0:
            if request.demand_qty != result.get(request.dest_location, 0):
                ans += 100
                ans += int(
                    100 * abs(result.get(request.dest_location, 0) - request.demand_qty) / request.demand_qty,
                )

    return ans
