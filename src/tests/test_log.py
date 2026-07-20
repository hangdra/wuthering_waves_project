# @Author  : liuha
# @Time    : 2026/7/18 05:14
# @File    : test_log.py
import logging

logger = logging.getLogger("my_app")
logger.setLevel(logging.WARNING)  # 👈 全局设为了 30

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)   # 👈 控制台设为了 10

logger.addHandler(console)

logger.debug("调试")   # ❌ 不输出，因为 logger 级别 (30) > debug (10)，在进入 handler 前就被拦截了
logger.warning("警告") # ✅ 输出，因为 30 >= 30