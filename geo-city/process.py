from queue import Queue as TQueue
from multiprocessing import Queue
from threading import Event, Thread
import array
import pathlib
from config import Config
from calculation.calculation import combinations


def get_string_format(city_1: str, city_2: str, distance: float) -> str:
    return Config.STRING_PATTERN.format(city_1=city_1, city_2=city_2, distance=distance)


def write_thread(queue: TQueue, e: Event, file: pathlib.Path):
    counter: int = 0
    with open(file, "w") as f:
        while True:
            _str = queue.get()
            if _str:
                f.write(_str)
                counter += 1

            if counter >= Config.FLUSH_COUNT:
                f.flush()
                counter = 0

            if e.is_set():
                break


def calculate(
    n: int,
    queue: Queue,
    data: list[tuple[str, float, float]]
):
    cities, coordinates = [], []
    file = Config.TEMP_FOLDER / Config.PROCES_TMP_PATTERN.format(n)

    for i in data:
        cities.append(i[0])
        coordinates.append(i[1])
        coordinates.append(i[2])

    values: array.array = array.array("d", coordinates)
    values_size = len(coordinates)
    coordinates.clear()
    result_array: array.array = array.array("i", [0 for i in range(values_size)])

    t_queue, e = TQueue(), Event()
    thread = Thread(target=write_thread, args=(t_queue, e, file))
    thread.start()

    while not queue.empty():
        city, lon_1, lat_1 = queue.get()
        distances = combinations(lon_1, lat_1, values, values_size, result_array)

        for city_2, distance in zip(cities, distances):
            _str = get_string_format(city, city_2, distance)
            t_queue.put(_str)

    e.set()
    thread.join()

