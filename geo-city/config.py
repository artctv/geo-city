import pathlib
from multiprocessing import cpu_count


BASE_FOLDER = pathlib.Path(__file__).parent.resolve()
FILES_FOLDER = "data"
EXCEL_NAME = "cities.xlsx"
WORKSHEET_NAME = "Лист1"
CSV_NAME = "result.csv"
RESULT_NAME = "result.xlsx"

MIN_ROW = 2  # skip first line
MIN_COL = 1
MAX_COL = 5

MP_COUNT = cpu_count() - 1
