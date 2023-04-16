import time
from multiprocessing import Queue, Process, Event
from operator import itemgetter
from copy import deepcopy
from loader import get_data
from process import calculate, write
from config import Config


data_T = list[tuple[str, float, float]]


def run_with_proc(data: data_T, queue: Queue, write_queue: Queue):
    print("--- Multiprocessing patterns inited ---")

    e: Event = Event()
    processes: list[Process] = []
    for i in range(Config.CPU_COUNT):
        p = Process(target=calculate, args=(queue, write_queue, data))
        processes.append(p)
    p_write = Process(target=write, args=(write_queue, data, e))
    processes.append(p_write)

    print("--- Processes created ---")

    for p in processes:
        p.start()

    print("--- Processes started ---")

    while not queue.empty():
        print(f"--- Queue size: {queue.qsize()} ---")
        print(f"--- Write Queue size: {write_queue.qsize()} ---")
        time.sleep(Config.SLEEP_TIME)

    print("--- Data calculated ---")

    while not write_queue.empty():
        print(f"--- Write Queue size: {write_queue.qsize()} ---")
        time.sleep(Config.SLEEP_TIME)

    e.set()
    print(f"--- Event is set: {e.is_set()} ---")
    time.sleep(Config.SLEEP_TIME)
    print("--- Processes completed ---")

    for p in processes:
        p.terminate()

    print("--- Processes terminated ---")


def run_without_proc(data: data_T, queue: Queue, write_queue: Queue):
    p_calc = Process(target=calculate, args=(queue, write_queue, data))
    e: Event = Event()
    p_write = Process(target=write, args=(write_queue, data, e))
    p_calc.start()
    p_write.start()
    print("--- Processes started ---")

    while not queue.empty():
        print(f"--- Queue size: {queue.qsize()} ---")
        print(f"--- Write Queue size: {write_queue.qsize()} ---")
        time.sleep(Config.SLEEP_TIME)

    print("--- Data calculated ---")
    p_calc.terminate()

    while not write_queue.empty():
        print(f"--- Write Queue size: {write_queue.qsize()} ---")
        time.sleep(Config.SLEEP_TIME)

    e.set()
    time.sleep(Config.SLEEP_TIME)
    p_write.terminate()


def main(temp: bool = False, data_count: int = 0, without_proc: bool = False):
    print("--- Script started ---")

    data: data_T = get_data(temp, data_count)
    data = sorted(data, key=itemgetter(0))
    print("--- Data loaded ---")
    print(f"--- Total number of elements: {len(data)} ---")
    queue: Queue = Queue()
    write_queue: Queue = Queue()
    for i in data:
        queue.put(deepcopy(i))

    if without_proc:
        run_without_proc(data, queue, write_queue)
    else:
        run_with_proc(data, queue, write_queue)

    print("--- Script finished ---")

