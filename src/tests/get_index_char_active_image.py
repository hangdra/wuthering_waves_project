# @Author  : liuha
# @Time    : 2026/7/18 22:01
# @File    : test_is_index_char_active.py


from pathlib import Path
import os
import json
import time
import matplotlib.pyplot as plt
import cv2
from src.utils.image_dealer import get_search_area, get_sub_image_from_image, template_match_target_new, \
    calculate_target_template_xy, IconPosition, concat_images_with_padding_new, get_rid_light_part_for_matching, \
    get_rid_dark_part_for_matching
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese

template_one = {
    "image_file_from_project_root": "",
    "image_file": "",
    "name": "",
    "target_process_method": "",
    "icon_position_group": "right_top",
    "min_success_score": 0.7,
    "template_window_width": 1600,
    "template_window_height": 900,
    "template_window_target_x": 597,
    "template_window_target_y": 810,
    "template_width": 50,
    "template_height": 50,
    "template_x": 0,
    "template_y": 0,
    "load_image": False
}


def get_123_char_active_img():
    output_dir = "src/tests/images/auto/"
    active_1 = "mc7_1600_900.png"

    image_a1 = imread_chinese(f"{output_dir}{active_1}")

    output_dir = "src/tests/images/template/"
    active_3 = "守岸人169.png"

    image_a3 = imread_chinese(f"{output_dir}{active_3}")
    print("image_a1.shape", image_a1.shape, "image_a3.shape", image_a3.shape)
    filename_this = "char_123_active_grey.png"
    output_img_dir_from_root = "src/assets/images/" + filename_this
    template_info_list = []

    y1, y2, x1, x2 = 177, 192, 1446, 1461
    index = 0
    image_this = image_a3
    tem_w_h, tem_w_w = image_this.shape[:2]
    c1_img = image_this[y1:y2, x1:x2]
    template_one_copy = template_one.copy()
    template_one_copy["image_file_from_project_root"] = output_img_dir_from_root
    template_one_copy["image_file"] = filename_this
    template_one_copy["name"] = "char_" + str(index + 1)
    template_one_copy["target_process_method"] = "get_rid_light_part_for_matching"
    template_one_copy["load_image"] = True
    template_one_copy["template_window_width"] = tem_w_w
    template_one_copy["template_window_height"] = tem_w_h
    template_one_copy["template_window_target_x"] = x1
    template_one_copy["template_window_target_y"] = y1
    template_one_copy["template_width"] = x2 - x1
    template_one_copy["template_height"] = y2 - y1
    template_one_copy["template_x"] = 0 + index * template_one_copy["template_width"]
    template_one_copy["template_y"] = 0
    template_info_list.append(template_one_copy)

    y1, y2, x1, x2 = 287, 302, 1446, 1461
    index = 1
    image_this = image_a3
    tem_w_h, tem_w_w = image_this.shape[:2]
    c2_img = image_this[y1:y2, x1:x2]
    template_one_copy = template_one.copy()
    template_one_copy["image_file_from_project_root"] = output_img_dir_from_root
    template_one_copy["image_file"] = filename_this
    template_one_copy["name"] = "char_" + str(index + 1)
    template_one_copy["target_process_method"] = "get_rid_light_part_for_matching"
    template_one_copy["load_image"] = True
    template_one_copy["template_window_width"] = tem_w_w
    template_one_copy["template_window_height"] = tem_w_h
    template_one_copy["template_window_target_x"] = x1
    template_one_copy["template_window_target_y"] = y1
    template_one_copy["template_width"] = x2 - x1
    template_one_copy["template_height"] = y2 - y1
    template_one_copy["template_x"] = 0 + index * template_one_copy["template_width"]
    template_one_copy["template_y"] = 0
    template_info_list.append(template_one_copy)

    y1, y2, x1, x2 = 397, 412, 1446, 1461
    index = 2
    image_this = image_a1
    tem_w_h, tem_w_w = image_this.shape[:2]
    c3_img = image_this[y1:y2, x1:x2]
    template_one_copy = template_one.copy()
    template_one_copy["image_file_from_project_root"] = output_img_dir_from_root
    template_one_copy["image_file"] = filename_this
    template_one_copy["name"] = "char_" + str(index + 1)
    template_one_copy["target_process_method"] = "get_rid_light_part_for_matching"
    template_one_copy["load_image"] = True
    template_one_copy["template_window_width"] = tem_w_w
    template_one_copy["template_window_height"] = tem_w_h
    template_one_copy["template_window_target_x"] = x1
    template_one_copy["template_window_target_y"] = y1
    template_one_copy["template_width"] = x2 - x1
    template_one_copy["template_height"] = y2 - y1
    template_one_copy["template_x"] = 0 + index * template_one_copy["template_width"]
    template_one_copy["template_y"] = 0
    template_info_list.append(template_one_copy)

    print("c1_img.shape", c1_img.shape, "c2_img.shape", c2_img.shape, "c3_img.shape", c3_img.shape)
    image_template_concat = concat_images_with_padding_new(c1_img, c2_img)
    image_template_concat = concat_images_with_padding_new(image_template_concat, c3_img)
    img_get_rid_of_light_part = get_rid_light_part_for_matching(image_template_concat)
    print("get_rid_light_part_for_matching(image_template_concat).shape",
          get_rid_light_part_for_matching(image_template_concat).shape)
    # cv2.imshow("", image_template_concat)
    # cv2.imshow("", get_rid_light_part_for_matching(image_template_concat))
    # # cv2.imshow("", get_rid_dark_part_for_matching(image_template_concat))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    imwrite_chinese(output_img_dir_from_root, img_get_rid_of_light_part)

    config_name = "char_123_active.json"
    with open('../../src/assets/config/image_info/' + config_name, 'w', encoding='utf-8') as f:
        json.dump(template_info_list, f, indent=2)  # 文件里会写入 "resize": false


get_123_char_active_img()

# # 使用示例
# if __name__ == "__main__":
#
#     project_root = Path(__file__).parent.parent.parent
#     all_template_info_file_name = "src/assets/config/image_info/all_char_head_icon_small2.json"
#     image_abs_path = os.path.join(project_root, all_template_info_file_name)
#     with open(image_abs_path, 'r', encoding='utf-8') as f:
#         head_icon_info = json.load(f)
#
#     output_dir = "src/tests/images/auto/"
#     file_result = {}
#     tar_sub_img = {}
#     time_s = time.perf_counter()
#     counter = 0
#     for filename in os.listdir(project_root / output_dir):
#         if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
