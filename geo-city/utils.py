import random
import string
import csv
import pathlib
from dataclasses import dataclass
from openpyxl import Workbook

import config


def strig_generator(size=12, chars=string.ascii_uppercase) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


def float_generator(min_: float = 10.0, max_: float = 100.0) -> float:
    return random.uniform(min_, max_)


@dataclass(eq=True, frozen=True)
class CityDistances:
    city: str
    cities_distances: dict[str, float]


@dataclass(eq=True, frozen=True)
class CityPoint:
    name: str
    lon: float
    lat: float

#     def __eq__(self, other: "CityPoint") -> bool:
#         if not isinstance(other, CityPoint):
#             return False
#         if self.name == other.name and self.lon == other.lon and self.lat == other.lat:
#             return True
#         return False
#
#     def __ne__(self, other: "CityPoint") -> bool:
#         if not isinstance(other, CityPoint):
#             return False
#         return not self.__eq__(other)


def converter():
    wb = Workbook()
    ws = wb.active

    xlsx_path: pathlib.Path = config.BASE_FOLDER / config.FILES_FOLDER / config.RESULT_NAME
    csv_path: pathlib.Path = config.BASE_FOLDER / config.FILES_FOLDER / config.CSV_NAME
    with open(csv_path, "r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            ws.append(row)

    wb.save(filename=xlsx_path)


if __name__ == "__main__":
    converter()
