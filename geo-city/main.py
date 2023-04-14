from multiprocessing import Queue
from copy import deepcopy
from loader import get_data
from process import calculate


def main(temp: bool = False, data_count: int = 0):
    data = get_data(temp, data_count)

    queue: Queue = Queue()
    for i in data:
        queue.put(deepcopy(i))

    calculate(queue, data)

