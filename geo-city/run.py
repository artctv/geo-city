from multiprocessing import Process, Event, Queue, Lock
import config
from utils import CityPoint
from reader import get_data
from writer import write
from calc import calculate
import time


def get_processes():
    write_pc = 1
    calc_pc = config.MP_COUNT - write_pc
    return calc_pc


def main():
    print("--- Script started ---")

    calc_pc = get_processes()
    data: list[CityPoint] = get_data()
    print("--- Data loaded ---")

    read_q, write_q = Queue(), Queue()
    lock_e: Event = Event()
    events: list[Event] = []
    processes: list[Process] = []
    print("--- Multiprocessing patterns inited ---")

    i: CityPoint
    for count, city_point in enumerate(data):
        read_q.put(city_point)

    for i in range(calc_pc):
        event = Event()
        calc_process = Process(target=calculate, args=(data, read_q, write_q, event, lock_e))
        events.append(event)
        processes.append(calc_process)

    write_process = Process(target=write, args=(data, write_q, events, lock_e))
    processes.append(write_process)

    print("--- Processes created ---")

    p: Process
    for p in processes:
        p.start()

    print("--- Processes started ---")
    print(f"--- Events statuses: {all(e.is_set() for e in events)}")

    while not read_q.empty():
        print(f"--- Read queue size: {read_q.qsize()} | Write queue size: {write_q.qsize()} ---")
        print(f"--- Events statuses: {all(e.is_set() for e in events)}")
        print(f"--- Lock event status: {lock_e.is_set()}")

        time.sleep(config.SLEEP_TIME)

    print("--- Data calculated ---")
    for p in processes:
        p.join()

    print("--- Processes completed ---")

    for p in processes:
        p.terminate()

    print("--- Processes terminated ---")


if __name__ == "__main__":
    main()
