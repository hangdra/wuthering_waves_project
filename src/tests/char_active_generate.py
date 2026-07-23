# @Author  : liuha
# @Time    : 2026/7/18 22:01
# @File    : test_is_index_char_active.py


import os
import json
import cv2

from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese
from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root

from src.utils.image_dealer import *
Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()

template_one = {
    "image_file_from_project_root": "",
    "image_file": "",
    "category": "char_active",

    "name": "",
    "target_search_type": "single_match",
    "target_process_method": "",
    "mask_color": "char_active",
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
    filename_this = "char_123_active.png"
    filename_this_grey = "char_123_active_grey.png"
    output_img_dir_from_root = "src/assets/images/" + filename_this
    output_img_dir_from_root_grey = "src/assets/images/" + filename_this_grey
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
    # img_get_rid_of_light_part = get_rid_light_part_for_matching(image_template_concat)
    print("get_rid_light_part_for_matching(image_template_concat).shape",
          get_rid_light_part_for_matching(image_template_concat).shape)
    # cv2.imshow("", image_template_concat)
    # cv2.imshow("", get_rid_light_part_for_matching(image_template_concat))
    # # cv2.imshow("", get_rid_dark_part_for_matching(image_template_concat))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    imwrite_chinese(output_img_dir_from_root, image_template_concat)
    # imwrite_chinese(output_img_dir_from_root_grey, img_get_rid_of_light_part)

    config_name = "char_123_active.json"
    with open(Root_dir / (Config_dir + config_name), 'w',encoding='utf-8') as f:
        json.dump(template_info_list, f, indent=2)  # 文件里会写入 "resize": false

    filename_this_grey = "char_123_active_grey.png"
    config_g = template_info_list.copy()
    filename_grey = Img_dir + filename_this_grey
    filename_t = os.path.basename(filename_grey)
    for item in config_g:
        item["image_file_from_project_root"] = filename_grey
        item["image_file"] = filename_t
        item["force_grey"] = True
        item["mask_color"] = None
        item["target_process_method"] = "get_rid_light_part_for_matching"

    # img_grey = cv2.cvtColor(image_template_concat, cv2.COLOR_BGR2GRAY)
    img_grey = get_rid_light_part_for_matching(image_template_concat)
    imwrite_chinese(filename_grey, img_grey)
    config_name = "char_123_active_grey.json"
    with open(Root_dir / (Config_dir + config_name), 'w',encoding='utf-8') as f:
        json.dump(config_g, f, indent=2)  # 文件里会写入 "resize": false



get_123_char_active_img()

