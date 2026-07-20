# @Author  : liuha
# @Time    : 2026/7/16 20:39
# @File    : get_file_root_dir.py

import os
from pathlib import Path

# 获取当前脚本所在目录的绝对路径（如 /path/to/project/src）
project_root = Path(__file__).parent.parent.parent
script_dir = os.path.dirname(os.path.abspath(__file__))
# 项目根目录 = 脚本目录的父目录（如 /path/to/project）
# project_root = os.path.dirname(script_dir)

# 拼接相对路径（相对于项目根目录）
relative_path = 'src/assets/images/all_in_one_template.png'
image_abs_path = os.path.join(project_root, relative_path)

# 读取文件
# with open(image_abs_path, 'rb') as f:
#     image_data = f.read()

print("script_dir",script_dir,"project_root",project_root,"image_abs_path",image_abs_path)