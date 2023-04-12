import pathlib
from multiprocessing import Queue
from config import Config
import harvesine.harvesine as hs


def get_string_format(city_1: str, city_2: str, distance: float) -> str:
    return Config.STRING_PATTERN.format(city_1=city_1, city_2=city_2, distance=distance)


def calc_task(
    data: dict[str, tuple[float, float]],
    q: Queue,
    file_n: int,
):
    base_folder: pathlib.Path = pathlib.Path(__file__).parent.resolve()
    file_path: pathlib.Path = base_folder / Config.FILES_FOLDER / Config.PROCES_TMP_PATTERN.format(file_n)
    counter: int = 0
    with open(file_path, "w") as f:
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
                f.write(_str)
                counter += 1

            if counter >= Config.FLUSH_COUNT:
                f.flush()

