# @Author  : liuha
# @Time    : 2026/7/18 03:27
# @File    : test_match_char.py
import time

from src.utils.load_all_template import my_LoadAllTemplate_instance

from pathlib import Path
import os
import json
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese

project_root = Path(__file__).parent.parent.parent
# all_template_info_file_name = "src/assets/config/image_info/all_char_head_icon_small2.json"
# image_abs_path = os.path.join(project_root, all_template_info_file_name)
# with open(image_abs_path, 'r', encoding='utf-8') as f:
#     head_icon_info = json.load(f)

output_dir = "src/tests/images/auto/"
file_result = {}
tar_sub_img = {}
for filename in os.listdir(project_root / output_dir):
    if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):

        file_result[filename] = {}
        find_char = []
        print(f"{output_dir}{filename}")
        tar_img = imread_chinese(f"{output_dir}{filename}")
        time_s = time.perf_counter()
        target_char_dic = my_LoadAllTemplate_instance.get_match_char_template_head_icon(tar_img,find_and_return_once=False)
        time_e = time.perf_counter()
        print(f"get_match_char_template_head_icon time cost : {(time_e-time_s):.4f}")
        print("filename", filename)
        print("result", target_char_dic)
        file_result[filename] = target_char_dic

print(file_result)