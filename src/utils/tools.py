# @Author  : liuha
# @Time    : 2026/7/18 03:55
# @File    : tools.py

import time
from src.utils.log import logger
from functools import wraps
from pathlib import Path


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 记录开始时间[reference:4]
        result = func(*args, **kwargs)  # 执行原函数[reference:5]
        end_time = time.perf_counter()  # 记录结束时间[reference:6]
        logger.debug(f"{func.__name__} 耗时: {end_time - start_time:.4f} 秒")  # 打印耗时[reference:7]
        return result  # 返回原函数的结果[reference:8]

    return wrapper


import time
from functools import wraps
import statistics  # 用于计算分位数（Python 3.8+），或使用 numpy


def stats_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 初始化（首次调用）
        if not hasattr(wrapper, 'calls'):
            wrapper.calls = 0
            wrapper.total_time = 0.0
            wrapper.times = []  # 存储每次耗时（秒）

        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        wrapper.calls += 1
        wrapper.total_time += elapsed
        wrapper.times.append(elapsed)

        # 可选：打印基础信息（不打印分位数，避免开销）
        avg = wrapper.total_time / wrapper.calls
        # print(f"[{func.__name__}] 调用 #{wrapper.calls}, 本次: {elapsed:.4f}s, 平均: {avg:.4f}s")

        return result

    # 获取统计信息（包含分位数）
    def get_stats():
        times = wrapper.times
        if not times:
            return {'calls': 0, 'total_time': 0.0, 'avg_time': 0.0,
                    'max': 0.0, 'p99': 0.0, 'p90': 0.0, 'p1': 0.0}
        sorted_times = sorted(times)
        n = len(sorted_times)
        return {
            'calls': wrapper.calls,
            'total_time': f"{wrapper.total_time:.5f}",
            'avg_time': f"{wrapper.total_time / wrapper.calls:.5f}",
            'max': f"{max(times):.5f}",
            'p99': f"{sorted_times[int(0.99 * n)] if n > 1 else sorted_times[0]:.5f}",
            'p90': f"{sorted_times[int(0.90 * n)] if n > 1 else sorted_times[0]:.5f}",
            'p1': f"{sorted_times[int(0.01 * n)] if n > 1 else sorted_times[0]:.5f}",
        }

    # 重置统计（清空列表）
    def reset_stats():
        wrapper.calls = 0
        wrapper.total_time = 0.0
        wrapper.times.clear()

    wrapper.get_stats = get_stats
    wrapper.reset_stats = reset_stats
    return wrapper


def get_root_dir(_file, max_iter=10):
    root_dir_name = "wuthering_waves_project"
    dir_now = Path(_file)
    step = 0
    while not str(dir_now).endswith(root_dir_name) and step < max_iter:
        step += 1
        dir_now = dir_now.parent
    if step >= max_iter:
        raise Exception(f"get_root_dir step above {max_iter}")
        return None
    else:
        return dir_now


def get_config_dir_from_root():
    return "src/assets/config/image_info/"


def get_template_img_dir_from_root():
    return "src/assets/images/"

def get_test_auto_img_dir_from_root():
    return "src/tests/images/auto/"
