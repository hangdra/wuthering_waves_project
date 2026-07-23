# @Author  : liuha
# @Time    : 2026/7/18 12:54
# @File    : test_template.py


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

all_template_name = ["e_forte_not_ready", "e_forte", "mouse_forte", "mouse_forte_not_ready", "char_1", "char_2",
                     "char_3"]
all_template_name = ["char_1", "char_2", "char_3"]

output_dir = "src/tests/images/template/"
file_result = {}
tar_sub_img = {}
for filename in os.listdir(project_root / output_dir):
    # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):

    file_result[filename] = {}
    find_char = []
    print(f"{output_dir}{filename}")
    tar_img = imread_chinese(f"{output_dir}{filename}")
    image_template_result = {}
    file_result[filename] = image_template_result
    for template_name in all_template_name:
        print("template_name", template_name)
        time_s = time.perf_counter()
        res = my_LoadAllTemplate_instance.match_template_by_name_default(tar_img, template_name)
        time_e = time.perf_counter()
        print(f"get_match_char_template_head_icon time cost : {(time_e - time_s):.4f}")
        image_template_result[template_name] = res
        # image_template_result[template_name + "max_score"] = res[1]
        # print("filename", filename,"template_name")
        # print("result", res)
print(file_result)
