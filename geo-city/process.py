from multiprocessing import Queue
import array
from config import Config
from calculation.calculation import combinations


def get_string_format(city_1: str, city_2: str, distance: float) -> str:
    return Config.STRING_PATTERN.format(city_1=city_1, city_2=city_2, distance=distance)


def calculate(
    queue: Queue,
    data: list[tuple[str, float, float]]
):
    counter: int = 0
    cities, coordinates = [], []
    for i in data:
        cities.append(i[0])
        coordinates.append(i[1])
        coordinates.append(i[2])

    values: array.array = array.array("d", coordinates)
    values_size = len(coordinates)
    coordinates.clear()
    result_array: array.array = array.array("i", [0 for i in range(values_size)])

    while not queue.empty():
        city, lon_1, lat_1 = queue.get()
        distances = combinations(lon_1, lat_1, values, values_size, result_array)
        for city_2, distance in zip(cities, distances):
            print(city, city_2, distance)

