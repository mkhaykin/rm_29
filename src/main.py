"""
Общая идея решения:
- как решать не понятно;
- можно придумать несколько вариантов распределения: начать с того, кто просит больше,
или с того, кто просит меньше. Здесь стоит пообщаться с заказчиком, но мы считаем, что
надо сделать как-то и потом уже обсудить, а том ли мы сделали;
- так же у нас нет критерия оценки хорошее получилось распределение или нет, то этот
критерий тоже надо придумать.

Исходные данные, при чтении csv все отрицательные значения устанавливаются в 0. В теории
надо уточнить по очистке и не означает ли это желание вернуть товар, но пока так.

Поэтому попробую реализовать следующий подход:
- придумаем несколько стратегий распределения;
- произведем расчет по этим стратегиям;
- полученные результаты прогоним через функцию "насколько вы удовлетворены результатом"
и выберем лучшее.

Что не сделано:
- в исходных у нас такой игрушечный пример, в котором фактически одна позиция и даты можно
игнорировать, собственно это в коде я и сделал;
- технически у нас какие стратегии могут считаться очень долго, поэтому в "реальной" жизни
можно ограничить время на обсчет. Если стратегия не справилась, то значит в результате ее
не рассматриваем.
"""

import logging
from multiprocessing import Pool
from pathlib import Path
from typing import List, Type

from penalty import penalty
from reader import RequestRaw, read_request_csv, read_supply_csv
from strategy import (
    StrategyAbc,
    StrategyFAFR,
    StrategyFAFRMaxFirst,
    StrategyFAFRMinFirst,
    StrategyFAFRPriority,
    StrategyZero,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def worker(
    strategy_cls: Type[StrategyAbc],
    available_qty: int,
    requests: list[RequestRaw],
) -> dict:
    obj = strategy_cls(available_qty, requests)
    return obj.calc()


def main() -> None:
    strategies: List[Type[StrategyAbc]] = [
        StrategyZero,
        StrategyFAFR,
        StrategyFAFRPriority,
        StrategyFAFRMinFirst,
        StrategyFAFRMaxFirst,
    ]
    path_to_data = Path(__file__).parent.parent / "data"

    supply_file = path_to_data / "supply.csv"
    requests_file = path_to_data / "requests.csv"

    for supply, requests in zip(
        read_supply_csv(supply_file),
        read_request_csv(requests_file),
        strict=True,
    ):
        with Pool(processes=len(strategies)) as pool:
            params = [(strategy, supply.available_qty, requests) for strategy in strategies]
            results = pool.starmap(worker, params)
            if not results:
                logger.error("Вообще не получил результатов, но идем дальше")
                continue

            best_result = results[0]
            best_penalty = penalty(requests, results[0])
            for result in results[1:]:
                if penalty(requests, result) < best_penalty:
                    best_result = result

            print(best_result)


if __name__ == "__main__":
    main()
