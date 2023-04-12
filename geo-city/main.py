import pathlib
import json
import time
import os
from dataclasses import dataclass
from typing import Iterable, Union
from multiprocessing import Process, Queue, Manager
from reader import load_data, prepare_data
from config import Config
from task import calc_task


@dataclass
class TmpMock:
    value: Union[str, float]


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

    stubbed = []
    for i in tmp_data:
        stubbed.append(
            [
                TmpMock(value=i[0]),
                TmpMock(value=0),
                TmpMock(value=0),
                TmpMock(value=i[1]),
                TmpMock(value=i[2]),
            ]
        )

    return iter(stubbed)


def merge_data(base_folder: pathlib.Path):
    file_path: pathlib.Path = base_folder / Config.FILES_FOLDER
    write_file = file_path / "result.txt"
    try:
        os.remove(write_file)
    except FileNotFoundError:
        pass

    for i in range(Config.CPU_COUNT):
        read_file: pathlib.Path = file_path / Config.PROCES_TMP_PATTERN.format(i+1)
        with open(write_file, "a") as w, open(read_file, "r") as r:
            for k in r:
                w.write(k)
            os.remove(read_file)


def prepare_structs(data: Iterable) -> tuple[dict, Queue]:
    _dict: dict = Manager().dict()
    queue: Queue = Queue()
    for i in data:
        d = prepare_data(i)
        queue.put(d)
        _dict[d[0]] = (d[1], d[2],)
    return _dict, queue


def main(base_folder: pathlib.Path):
    print("--- Script started ---")

    data = load_data(base_folder)
    # data = temp_data(base_folder)

    print("--- Data loaded ---")

    d, q = prepare_structs(data)

    print("--- Multiprocessing patterns inited ---")

    processes: list[Process] = []
    for i in range(Config.CPU_COUNT):
        p = Process(target=calc_task, args=(d, q, i+1))
        processes.append(p)

    print("--- Processes created ---")

    for p in processes:
        p.start()

    print("--- Processes started ---")

    while not q.empty():
        print(f"--- Queue size: {q.qsize()} ---")
        time.sleep(Config.SLEEP_TIME)

    print("--- Data calculated ---")
    for p in processes:
        p.join()

    print("--- Processes completed ---")

    for p in processes:
        p.terminate()

    print("--- Processes terminated ---")


if __name__ == "__main__":
    folder: pathlib.Path = pathlib.Path(__file__).parent.resolve()
    main(folder)
    # merge_data(folder)
