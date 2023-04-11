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
    cities = data.keys()
    with open(file_path, "w") as f:
        counter: int = 0
        while not q.empty():
            city, lon_1, lat_1 = q.get()
            for i in cities:
                lon_2, lat_2 = data[i]
                distance = hs.calculate(lon_1, lat_1, lon_2, lat_2)
                _str = get_string_format(city, i, distance)
                f.write(_str)
                counter += 1

            if counter >= Config.FLUSH_COUNT:
                f.flush()
