from abc import ABC, abstractmethod
from typing import Iterable, List

from reader import RequestRaw


class StrategyAbc(ABC):
    _available_qty: int
    _requests: List[RequestRaw]

    def __init__(self, available_qty: int, requests: Iterable[RequestRaw]) -> None:
        self._available_qty = available_qty
        self._requests = list(requests)

    @abstractmethod
    def calc(self) -> dict[str, int]:
        pass


class StrategyZero(StrategyAbc):
    """
    Пустышка, никому ничего не даем.
    """

    def calc(self) -> dict[str, int]:
        return {request.dest_location: 0 for request in self._requests}


class StrategyFAFR(StrategyAbc):
    """
    Первый попросил, первый получил
    """

    def calc(self) -> dict[str, int]:
        balance = self._available_qty
        result = {}
        for request in self._requests:
            count = min(balance, request.demand_qty)

            if request.rounding_value:
                count = count // request.rounding_value * request.rounding_value

            if count < request.min_lot:
                count = 0

            balance -= count
            result[request.dest_location] = count

        return result


class StrategyFAFRPriority(StrategyFAFR):
    """
    Первый попросил, первый получил, но тут мы пересортировываем запросы, так,
    чтобы приоритетные были в начале. Так как сортировка у нас устойчивая, то результат
    будет детерминированный.
    """

    def __init__(self, available_qty: int, requests: Iterable[RequestRaw]) -> None:
        super().__init__(available_qty, requests)
        self._requests.sort(key=lambda request: request.priority)


class StrategyFAFRMinFirst(StrategyFAFR):
    """
    Дополнительно к приоритетам добавляем сортировку по количеству,
    но сначала выполняем маленькие заказы
    """

    def __init__(self, available_qty: int, requests: Iterable[RequestRaw]) -> None:
        super().__init__(available_qty, requests)
        self._requests.sort(key=lambda request: (request.priority, request.demand_qty))


class StrategyFAFRMaxFirst(StrategyFAFR):
    """
    Дополнительно к приоритетам добавляем сортировку по количеству,
    но сначала пытаемся выполнить большие заказы
    """

    def __init__(self, available_qty: int, requests: Iterable[RequestRaw]) -> None:
        super().__init__(available_qty, requests)
        self._requests.sort(key=lambda request: (request.priority, -request.demand_qty))
