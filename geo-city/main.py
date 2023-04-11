import pathlib
import json
from reader import load_data, prepare_data
from config import Config


def temp_data(base_folder: pathlib.Path):
    tmp_file: pathlib.Path = base_folder / Config.FILES_FOLDER / Config.TMP_FILE
    tmp_data = []
    if not tmp_file.is_file():
        data = load_data(base_folder)
        i: tuple
        for n, i in enumerate(data, start=1):
            tmp_data.append(prepare_data(i))
            if n == 100:
                break
        with open(tmp_file, "w") as f:
            json.dump(tmp_data, f, ensure_ascii=False, indent=4)
    else:
        with open(tmp_file, "r") as f:
            tmp_data = json.load(f)
    return tmp_data


def main():
    base_folder: pathlib.Path = pathlib.Path(__file__).parent.resolve()
    # data = load_data(base_folder)
    data = temp_data(base_folder)



if __name__ == "__main__":
    main()