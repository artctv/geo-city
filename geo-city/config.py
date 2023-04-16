import pathlib
from multiprocessing import cpu_count


class Config:
    BASE_FOLDER: pathlib.Path = pathlib.Path(__file__).parent.resolve()
    FILES_FOLDER: pathlib.Path = BASE_FOLDER / "data"
    TEMP_FOLDER: pathlib.Path = BASE_FOLDER / "temp"
    TEMP_FILE: pathlib.Path = TEMP_FOLDER / "temp.json"
    RESULT_FILE: pathlib.Path = FILES_FOLDER / "result.csv"
    DATA_FILE: pathlib.Path = FILES_FOLDER / "cities.xlsx"
    WORKSHEET_NAME: str = "Лист1"
    MIN_ROW: int = 2  # skip first line from .xlsx file
    MIN_COL: int = 1
    MAX_COL: int = 5

    CPU_COUNT: int = cpu_count()
    SLEEP_TIME: int = 10  # sec
    FLUSH_COUNT: int = 10_000
