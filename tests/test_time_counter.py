# @Author  : liuha
# @Time    : 2026/7/13 03:47
# @File    : test_time_counter.py
from time import perf_counter
import time

TEST_COUNT = 30000000


def target_func():
    result = [i * i for i in range(TEST_COUNT)]
    return


def main() -> None:
    time_start = perf_counter()

    result = [i * i for i in range(TEST_COUNT)]

    time_end = perf_counter()
    time_duration = time_end - time_start

    print(f'Duration: {time_duration:.3f} seconds')
    del result
    time.sleep(10)
    time_start = perf_counter()

    target_func()

    time_end = perf_counter()
    time_duration = time_end - time_start

    print(f'Duration: {time_duration:.3f} seconds')


if __name__ == '__main__':
    main()
    pass