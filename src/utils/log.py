# @Author  : liuha
# @Time    : 2026/7/12 22:55
# @File    : test_log.py

import logging
from pathlib import Path

# 1. 创建 Logger 对象（名字建议用 __name__）
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 2. 创建 文件处理器 (写入文件)
project_root = Path(__file__).parent.parent.parent  # 假设当前文件在 src/utils/ 下，向上三级到达根目录
logs_dir = project_root / 'logs'
logs_dir.mkdir(exist_ok=True)  # 确保目录存在
print(type(logs_dir))
log_file_path = logs_dir / 'project.log'
file_handler = logging.FileHandler(str(log_file_path), encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 3. 创建 控制台处理器 (打印到屏幕)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 4. 定义日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 5. 将处理器添加到 logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 使用
# logger.debug("调试信息（只在控制台看）")
# logger.info("关键业务流程记录（写入文件）")




# # 或者更灵活：向上搜索直到找到某个标志文件（如 .git、setup.py）
# def find_project_root(current_path, marker='.git'):
#     for parent in current_path.parents:
#         if (parent / marker).exists():
#             return parent
#     return current_path.parent  # 未找到时返回最上层

# project_root = find_project_root(Path(__file__).resolve())


