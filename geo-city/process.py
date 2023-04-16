import csv
import array
from typing import Union, Final, Literal
from copy import deepcopy
from multiprocessing import Queue, Event
from config import Config
from calculation.calculation import combinations


data_T = list[tuple[str, float, float]]


def write(queue: Queue, data: data_T, e: Event):
    angle_key: Final[Literal["City/City"]] = "City/City"
    cities: list[str] = [angle_key]  # for element in A:1 in csv file
    for i in data:
        cities.append(deepcopy(i[0]))
    cities: dict[str, Union[str, int]] = dict.fromkeys(cities, 0)
    with open(Config.RESULT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(
            csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(cities.keys())

        counter: int = 0
        obj: dict[str, list[tuple[str, int]]]
        while not e.is_set():
            obj = queue.get()
            city_1 = list(obj.keys())[0]
            cities[angle_key] = city_1
            for city_2, distance in obj[city_1]:
                cities[city_2] = distance
            writer.writerow(cities.values())
            counter += 1

            if counter >= Config.FLUSH_COUNT:
                csvfile.flush()
                print("--- Flushed to file ---")
                counter = 0


def calculate(queue: Queue, write_queue: Queue, data: data_T):
    cities, coordinates = [], []  # noqa
    for i in data:
        cities.append(deepcopy(i))
        coordinates.append(i[1])
        coordinates.append(i[2])

    size: int = len(coordinates)
    coordinates: array.array = array.array("d", coordinates)
    result: array.array = array.array("i", [0 for _ in range(size)])
    data.clear()

    to_write: dict[str, list[tuple[str, int]]] = {}
    buff: list[tuple[str, int]] = []
    while not queue.empty():
        city_1, lon_1, lat_1 = queue.get()
        distances = combinations(lon_1, lat_1, coordinates, size, result)
        for city_2, distance in zip(cities, distances):
            buff.append((city_2, distance,))

        to_write[city_1] = deepcopy(buff)
        write_queue.put(deepcopy(to_write))
        to_write.clear()
        buff.clear()

