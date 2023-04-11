from multiprocessing import cpu_count


class Config:
    FILES_FOLDER = "data"
    FILE_NAME = "cities.xlsx"
    WORKSHEET_NAME = "Лист1"
    MIN_ROW = 2  # skip first line from .xlsx file
    MIN_COL = 1
    MAX_COL = 5

    RESULT_CSV = "result.csv"
    RESULT_EXCEL = "result.xlsx"

    CPU_COUNT = cpu_count()
    SLEEP_TIME = 10  # sec

    TMP_FILE = "tmp.json"