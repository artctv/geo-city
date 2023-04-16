import csv
import array
from typing import Union, Final, Literal
from copy import deepcopy
from multiprocessing import Queue, Event
from config import Config
from calculation.calculation import combinations


data_T = list[tuple[str, float, float]]


def write(queue: Queue, data: data_T, e: Event):
    counter: int = 0
    file = Config.TEMP_FOLDER / Config.RESULT_FILE
    angle_key: Final[Literal["City/City"]] = "City/City"
    cities: list[str] = [angle_key]  # for element in A:1 in csv file
    for i in data:
        cities.append(deepcopy(i[0]))

    cities: dict[str, Union[str, int]] = dict.fromkeys(cities, 0)

    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(
            csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(cities.keys())

        print("--- Writing started ---")
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


def calculate(
    queue: Queue,
    write_queue: Queue,
    data: data_T
):
    cities, coordinates = [], []
    for i in data:
        cities.append(deepcopy(i[0]))
        coordinates.append(i[1])
        coordinates.append(i[2])

    values: array.array = array.array("d", coordinates)
    values_size = len(coordinates)
    coordinates.clear()
    result_array: array.array = array.array("i", [0 for i in range(values_size)])
    to_write_queue: dict[str, list[tuple[str, int]]] = {}
    while not queue.empty():
        city_1, lon_1, lat_1 = queue.get()
        distances = combinations(lon_1, lat_1, values, values_size, result_array)
        buff: list[tuple[str, int]] = []
        for city_2, distance in zip(cities, distances):
            buff.append((city_2, distance,))  # noqa
        to_write_queue[city_1] = buff
        write_queue.put(deepcopy(to_write_queue))
        to_write_queue.clear()
