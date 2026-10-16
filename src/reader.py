"""
тут просто читаем csv и отдаем в некоторой структуре
"""

import csv
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
from typing import Generator, List, Optional, Type


@dataclass(slots=True, frozen=True)
class RequestRaw:
    case_id: str
    request_id: str
    dest_location: str
    priority: int
    demand_qty: int
    min_lot: int
    rounding_value: int


@dataclass(slots=True, frozen=True)
class SupplyRaw:
    case_id: str
    period: str
    item: str
    source_location: str
    available_qty: int


def _raw_to_dataclass[T](row: dict, model: Type[T], int_fields: Optional[set] = None) -> T:
    if int_fields is None:
        int_fields = set()

    fixed_row = {k: (int(v) if int(v) >= 0 else 0) if k in int_fields else v for k, v in row.items()}
    return model(**fixed_row)


def read_supply_csv(file_path: str | Path) -> Generator[SupplyRaw, None, None]:
    int_fields = {"available_qty"}

    with open(file_path, mode="r", encoding="utf-8") as fr:
        reader = csv.DictReader(fr)
        for row in reader:
            yield _raw_to_dataclass(row, SupplyRaw, int_fields)


def read_request_csv(file_path: str | Path) -> Generator[List[RequestRaw], None, None]:
    int_fields = {"priority", "demand_qty", "min_lot", "rounding_value"}

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for _, group in groupby(reader, key=lambda r: r["case_id"]):
            yield [_raw_to_dataclass(row, RequestRaw, int_fields) for row in group]


def reader() -> Generator[tuple[SupplyRaw, List[RequestRaw]], None, None]:
    path_to_data = Path(__file__).parent.parent / "data"

    supply_file = path_to_data / "supply.csv"
    requests_file = path_to_data / "requests.csv"

    for supply, requests in zip(
        read_supply_csv(supply_file),
        read_request_csv(requests_file),
        strict=True,
    ):
        yield supply, requests
