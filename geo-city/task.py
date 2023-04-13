import pathlib
from queue import Queue as TQueue
from multiprocessing import Queue
from threading import Event, Thread
from config import Config
import harvesine.harvesine as hs


def get_string_format(city_1: str, city_2: str, distance: float) -> str:
    return Config.STRING_PATTERN.format(city_1=city_1, city_2=city_2, distance=distance)


def write_thread(queue: TQueue, e: Event, file_path: pathlib):
    counter: int = 0
    with open(file_path, "w") as f:
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


def calc_task(
    data: dict[str, tuple[float, float]],
    q: Queue,
    file_n: int,
):
    queue, e = TQueue(), Event()
    base_folder: pathlib.Path = pathlib.Path(__file__).parent.resolve()
    file_path: pathlib.Path = base_folder / Config.FILES_FOLDER / Config.PROCES_TMP_PATTERN.format(file_n)
    thread = Thread(target=write_thread, args=(queue, e, file_path))
    thread.start()
    while not q.empty():
        city, lon_1, lat_1 = q.get()
        elements, cities = [], data.keys()
        for i in data.keys():
            lon_2, lat_2 = data[i]
            elements.append(lon_2)
            elements.append(lat_2)

        distances = hs.combinations([lon_1, lat_1], elements, len(elements))
        for _city, distance in zip(cities, distances):
            _str = get_string_format(city, _city, distance)
            queue.put(_str)

    e.set()
    thread.join()
