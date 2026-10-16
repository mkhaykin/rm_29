from reader import RequestRaw


def penalty(
    requests: list[RequestRaw],
    result: dict[str, int],
) -> int:
    """
    идея в том, что у нас есть некая функция штрафа, для оценки результатов расчета.
    пока принял следующий вариант:
        - не выполнили заказ - 100 очков штрафа;
        - так же к штрафу добавляем процент расхождения. Т.е. штрафуем и за превышение, но
        пока все стратегии не превышают;
        - корректируем на приоритет - один заказ условно равен 10 заказам приоритета ниже
    """
    max_priority = max(request.priority for request in requests)
    ans = 0
    for request in requests:
        request_penalty = 0
        if request.demand_qty != 0:
            if request.demand_qty != result.get(request.request_id, 0):
                ans += 100
                ans += int(
                    100 * abs(result.get(request.request_id, 0) - request.demand_qty) / request.demand_qty,
                )
                request_penalty *= 10 * (max_priority - request.priority)
        ans += request_penalty

    return ans
