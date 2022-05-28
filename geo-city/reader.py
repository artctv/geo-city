import pathlib
from openpyxl import load_workbook, Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

import config
from utils import CityPoint


def get_workbook(file: pathlib.Path) -> Workbook:
    return load_workbook(file, read_only=True, data_only=True, keep_links=False)


def get_worksheet(workbook: Workbook, worksheet: str) -> Worksheet:
    return workbook[worksheet]


def get_data() -> list[CityPoint]:
    excl_path: pathlib.Path = config.BASE_FOLDER / config.FILES_FOLDER / config.EXCEL_NAME
    workbook: Workbook = get_workbook(excl_path)
    worksheet: Worksheet = get_worksheet(workbook, config.WORKSHEET_NAME)
    cities_data: list[CityPoint] = []
    line: tuple[Cell, Cell, Cell, Cell, Cell]
    for line in worksheet.iter_rows(min_row=config.MIN_ROW, min_col=config.MIN_COL, max_col=config.MAX_COL):
        city: Cell
        lon: Cell
        lat: Cell
        city, _, _, lon, lat = line
        cities_data.append(CityPoint(name=city.value, lon=lon.value, lat=lat.value))
    return cities_data



