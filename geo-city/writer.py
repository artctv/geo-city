import csv
import pathlib
from typing import Literal
from multiprocessing import Queue, Event

import config
from utils import CityPoint, CityDistances

predef_fieldname: Literal["Cities"] = "Cities"


def prepare_fieldnames(data: list[CityPoint]) -> list[str]:
    fieldnames: list[str] = [predef_fieldname]
    for i in data:
        fieldnames.append(i.name)
    data.clear()
    del data
    return fieldnames


def write(data: list[CityPoint], write_q: Queue, events: list[Event], lock_e: Event) -> None:
    fieldnames = prepare_fieldnames(data)
    csv_path: pathlib.Path = config.BASE_FOLDER / config.FILES_FOLDER / config.CSV_NAME
    with open(csv_path, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        row: dict[str, str | float] = {}
        bool_events = all(e.is_set() for e in events)
        while not all([bool_events, write_q.empty()]):
            queue_data: CityDistances | None = write_q.get()
            if queue_data:
                row.update(queue_data.cities_distances)
                row[predef_fieldname] = queue_data.city
                writer.writerow(row)
                csvfile.flush()
                row.clear()
                queue_data = None

            if write_q.qsize() >= 200:
                lock_e.set()

            if write_q.qsize() <= 10:
                lock_e.clear()

            bool_events = all(e.is_set() for e in events)

