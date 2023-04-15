import pathlib
from multiprocessing import cpu_count


class Config:
    BASE_FOLDER: pathlib.Path = pathlib.Path(__file__).parent.resolve()
    FILES_FOLDER = BASE_FOLDER / "data"
    TEMP_FOLDER = BASE_FOLDER / "temp"
    TEMP_FILE = TEMP_FOLDER / "temp.json"
    RESULT_FILE = FILES_FOLDER / "result.csv"
    DATA_FILE = FILES_FOLDER / "cities.xlsx"
    WORKSHEET_NAME = "Лист1"
    MIN_ROW = 2  # skip first line from .xlsx file
    MIN_COL = 1
    MAX_COL = 5

    CPU_COUNT = cpu_count()
    SLEEP_TIME = 30  # sec
    FLUSH_COUNT = 1_000_000
    PROCES_TMP_PATTERN = "process_{}.csv"
    STRING_PATTERN = "{city_1}||{city_2}||{distance}\n"

