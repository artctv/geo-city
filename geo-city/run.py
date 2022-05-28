from multiprocessing import Process, Event, Queue
import config
from utils import CityPoint
from reader import get_data
from writer import write
from calc import calculate


def get_processes():
    write_pc = 1
    calc_pc = config.MP_COUNT - write_pc
    return calc_pc


def main():
    calc_pc = get_processes()
    data: list[CityPoint] = get_data()

    read_q, write_q = Queue(), Queue()
    events: list[Event] = []
    processes: list[Process] = []

    i: CityPoint
    for i in data:
        read_q.put(i)

    for i in range(calc_pc):
        event = Event()
        calc_process = Process(target=calculate, args=(data, read_q, write_q, event))
        events.append(event)
        processes.append(calc_process)

    write_process = Process(target=write, args=(data, write_q, events))
    processes.append(write_process)

    p: Process
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    for p in processes:
        p.close()


# def test_main():
    # data: list[CityPoint] = []
    # for i in range(1000):
    #     city_point = CityPoint(
    #         name=utils.strig_generator(),
    #         lon=utils.float_generator(),
    #         lat=utils.float_generator()
    #     )
    #     data.append(city_point)
    # d = calculate(data)
    # write(data, d)


if __name__ == "__main__":
    main()
