from typing import Dict, Iterable

from ortools.linear_solver import pywraplp

from print_result import print_result
from reader import RequestRaw, reader


def allocate(available_qty: int, requests: Iterable[RequestRaw]) -> Dict[str, int]:
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return {}

    req_list = list(requests)
    if not req_list or available_qty <= 0:
        return {r.request_id: 0 for r in req_list}

    max_priority = max(r.priority for r in req_list)

    x = {}  # объем отгрузки по каждому заказу
    b = {}  # флаг: отгружаем или нет

    for i, r in enumerate(req_list):
        b[i] = solver.BoolVar(f"b_{r.request_id}")
        x[i] = solver.IntVar(0, r.demand_qty, f"x_{r.request_id}")

        # ограничения:
        # - грузим меньше или столько сколько попросили
        solver.Add(x[i] <= r.demand_qty * b[i])
        #  - партия
        if r.min_lot > 0:
            solver.Add(x[i] >= r.min_lot * b[i])
        #  - кратность
        if r.rounding_value > 1:
            # берем ближайшее меньшее кратное
            max_k = r.demand_qty // r.rounding_value
            k = solver.IntVar(0, max_k, f"k_{r.request_id}")
            solver.Add(x[i] == k * r.rounding_value)

    # ограничения:
    # - суммарный лимит отгрузок
    solver.Add(solver.Sum(x[i] for i in range(len(req_list))) <= available_qty)

    objective = solver.Objective()
    for i, r in enumerate(req_list):
        # тут пытаюсь выкрутиться с приоритетом, 1 - макс приоритет
        # идея со степенью не моя, но должна сработать
        weight = 100 ** (max_priority - r.priority + 1)
        objective.SetCoefficient(x[i], weight)

    objective.SetMaximization()
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        for i, r in enumerate(req_list):
            result[r.request_id] = int(x[i].solution_value())
    else:
        # нет решения
        result = {r.request_id: 0 for r in req_list}

    return result


def main() -> None:
    for supply, requests in reader():
        result = allocate(supply.available_qty, requests)
        print_result(supply, requests, result)


if __name__ == "__main__":
    main()
