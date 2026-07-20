# @Author  : liuha
# @Time    : 2026/7/18 03:55
# @File    : tools.py

import time
from src.utils.log import logger
from pathlib import Path

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 记录开始时间[reference:4]
        result = func(*args, **kwargs)  # 执行原函数[reference:5]
        end_time = time.perf_counter()  # 记录结束时间[reference:6]
        logger.debug(f"{func.__name__} 耗时: {end_time - start_time:.4f} 秒")  # 打印耗时[reference:7]
        return result  # 返回原函数的结果[reference:8]

    return wrapper

def get_root_dir(_file,max_iter= 10):
    root_dir_name = "wuthering_waves_ok_copy"
    dir_now = Path(_file)
    step = 0
    while not str(dir_now).endswith(root_dir_name) and step < max_iter:
        step+=1
        dir_now = dir_now.parent
    if step>=max_iter:
        raise Exception(f"get_root_dir step above {max_iter}")
        return None
    else:
        return dir_now
