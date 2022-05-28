from math import radians, cos, sin, asin, sqrt
from multiprocessing import Queue, Event
from typing import Final

from utils import CityPoint, CityDistances

EARTH_RADIUS: Final[float] = 6371  # km


def haversine(lon_1: float, lat_1: float, lon_2: float, lat_2: float) -> float:
    lon_1, lat_1, lon_2, lat_2 = map(radians, [lon_1, lat_1, lon_2, lat_2])

    # haversine formula
    dlon, dlat = lon_2 - lon_1, lat_2 - lat_1
    angle = sin(dlat/2)**2 + cos(lat_1) * cos(lat_2) * sin(dlon/2)**2
    angle_asin = 2 * asin(sqrt(angle))
    return angle_asin * EARTH_RADIUS


def prepare_data(data: list[CityPoint]) -> dict[CityPoint, None]:
    cities_data = dict.fromkeys(data)
    data.clear()
    del data
    return cities_data


def calculate(data: list[CityPoint], read_q: Queue, write_q: Queue, event: Event()):
    cities_data = prepare_data(data)

    cities_distances: dict[str, float] = {}
    while not read_q.empty():
        cities_distances.clear()
        city_point: CityPoint = read_q.get()  # get from queue
        if city_point:
            i: CityPoint
            for i in cities_data.keys():
                distance: float = haversine(
                    lon_1=city_point.lon, lat_1=city_point.lat,
                    lon_2=i.lon, lat_2=i.lat
                )
                cities_distances[i.name] = distance
            _ = cities_data.pop(city_point, None)
            cities_distances[city_point.name] = 0
            city_distances = CityDistances(city=city_point.name, cities_distances=cities_distances)
            write_q.put(city_distances)
    else:
        event.set()
