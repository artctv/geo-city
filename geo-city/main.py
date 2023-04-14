import time
from multiprocessing import Queue, Process
from copy import deepcopy
from loader import get_data
from process import calculate
from config import Config


def main(temp: bool = False, data_count: int = 0):
    print("--- Script started ---")

    data = get_data(temp, data_count)
    print("--- Data loaded ---")

    queue: Queue = Queue()
    for i in data:
        queue.put(deepcopy(i))
    print("--- Multiprocessing patterns inited ---")

    processes: list[Process] = []
    for i in range(Config.CPU_COUNT):
        p = Process(target=calculate, args=(i+1, queue, data))
        processes.append(p)

    print("--- Processes created ---")

    for p in processes:
        p.start()

    print("--- Processes started ---")

    while not queue.empty():
        print(f"--- Queue size: {queue.qsize()} ---")
        time.sleep(Config.SLEEP_TIME)

    print("--- Data calculated ---")
    for p in processes:
        p.join()

    print("--- Processes completed ---")

    for p in processes:
        p.terminate()

    print("--- Processes terminated ---")

