# @Author  : liuha
# @Time    : 2026/7/19 14:31
# @File    : test_add_template_to_config.py
import os
import json
from pathlib import Path

from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir
from src.utils.image_dealer import *

project_root = Path(__file__).parent.parent.parent

template_one = {
    "image_file_from_project_root": "",
    "image_file": "",
    "name": "",
    "template_type": "",
    "target_process_method": "",
    "icon_position_group": "",
    "min_success_score": 0.7,
    "template_window_width": 1600,
    "template_window_height": 900,
    "template_window_target_x": -1,
    "template_window_target_y": -1,
    "template_width": -1,
    "template_height": -1,
    "template_x": -1,
    "template_y": 0,
    "x_variance_factor": 2,
    "y_variance_factor": 2,
    "load_image": True

}

img_dic = {}


def load_img(path, flag=cv2.IMREAD_GRAYSCALE):
    if path not in img_dic:
        img_dic[path] = imread_chinese(path, flag=flag)
    return img_dic[path]


def check_config(config1):
    config1_last_x = 0
    config1_img_data = None
    config1_last_image_file = None
    for item in config1:
        image_file = item["image_file_from_project_root"]
        if config1_last_image_file is None:
            config1_img_data = load_img(item["image_file_from_project_root"])
            config1_last_image_file = image_file
        elif image_file != config1_last_image_file:
            raise Exception("has two img file to read ", image_file, "and", config1_last_image_file)
        x_end_here = item["template_x"] + item["template_width"]
        if x_end_here > config1_last_x:
            config1_last_x = x_end_here
    config1_oi_h, config1_oi_w = config1_img_data.shape[:2]
    if config1_oi_w != config1_last_x:
        raise Exception("config1_oi_w!=last_x oi_w", config1_oi_w, " config1_last_x", config1_last_x)
    return config1_img_data


def combine_two_config_and_image_from_file(config_list_in, output_img_dir_in):
    item_img_list = []
    for item in config_list_in:
        item_img = check_config(item)
        item_img_list.append(item_img)

    template_new = config_list_in[0].copy()
    combine_img_inner = None
    for i in range(len(item_img_list)):
        if combine_img_inner is None:
            combine_img_inner = item_img_list[i]
        else:
            h, w = combine_img_inner.shape[:2]
            last_x_for_new_tem = w
            for item in config_list_in[i]:
                item["template_x"] = last_x_for_new_tem
                item["template_y"] = 0
                last_x_for_new_tem = last_x_for_new_tem + item["template_width"]
                template_new.append(item.copy())

            combine_img_inner = concat_images_with_padding_new(combine_img_inner, item_img_list[i])

    for item in template_new:
        item["image_file_from_project_root"] = str(output_img_dir_in)
        item["image_file"] = os.path.basename(output_img_dir_in)

    return template_new, combine_img_inner


def merge_two_config_and_img(old_template_info_list, new_tem_obj, new_img_data, output_img_dir):
    # with open(template_config_origin, 'r', encoding='utf-8') as f:
    #     template_info_list = json.load(f)
    last_x = 0
    y_c = 0
    old_img_data = None
    last_image_file = None
    for item in old_template_info_list:
        image_file = item["image_file_from_project_root"]
        if last_image_file is None:
            old_img_data = load_img(item["image_file_from_project_root"])
            last_image_file = image_file
        elif image_file != last_image_file:
            raise Exception("has two img file to read ", image_file, "and", last_image_file)
        x_end_here = item["template_x"] + item["template_width"]
        if x_end_here > last_x:
            last_x = x_end_here
    oi_h, oi_w = old_img_data.shape[:2]
    if oi_w != last_x:
        raise Exception("oi_w!=last_x oi_w", oi_w, " last_x", last_x)

    old_template_info_list_c = old_template_info_list.copy()
    combine_img = concat_images_with_padding_new(old_img_data, new_img_data)
    c_h, c_w = combine_img.shape[:2]
    last_x_for_new_tem = last_x
    item = new_tem_obj
    item["image_file_from_project_root"] = output_img_dir
    item["image_file"] = os.path.basename(output_img_dir)
    item["template_x"] = last_x_for_new_tem
    item["template_y"] = y_c
    last_x_for_new_tem = last_x_for_new_tem + item["template_width"]
    old_template_info_list_c.append(item.copy())

    if c_w != last_x_for_new_tem:
        raise Exception(f"after combine img c_w {c_w}!= last_x_for_new_tem{last_x_for_new_tem}")

    return old_template_info_list_c, combine_img
    with open(output_config, 'w', encoding='utf-8') as f:
        json.dump(old_template_info_list_c, f, indent=2)  # 文件里会写入 "resize": false
    imwrite_chinese(output_img, combine_img)


def get_new_item_template(tem_origin_img_file_dir, template_one_in, img_process_method_name=None, test_show=True):
    # with open(template_config_origin, 'r', encoding='utf-8') as f:
    #     template_info_list = json.load(f)

    image_before_tem = imread_chinese(f"{tem_origin_img_file_dir}")
    tem_w_h, tem_w_w = image_before_tem.shape[:2]
    template_window_target_x = template_one_in["template_window_target_x"]
    template_window_target_y = template_one_in["template_window_target_y"]
    tem_w = template_one_in["template_width"]
    tem_h = template_one_in["template_height"]
    template_one_in["template_window_width"] = tem_w_w
    template_one_in["template_window_height"] = tem_w_h
    if img_process_method_name != "" and img_process_method_name is not None:
        template_one_in["target_process_method"] = img_process_method_name
    tem_img = image_before_tem[template_window_target_y:template_window_target_y + tem_h,
              template_window_target_x:template_window_target_x + tem_w]
    img_process_method = get_process_method(img_process_method_name)
    tem_img = img_process_method(tem_img)
    if test_show:
        cv2.imshow(template_one_in["name"], tem_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return template_one_in, tem_img


config_dir = project_root / "src/assets/config/image_info/image_template_info.json"
new_template_img_file_dir = "src/tests/images/template/丽贝卡左键满169.png"
img_process_method_name = "get_rid_dark_part_for_matching"
template_one_c = template_one.copy()
template_one_c["name"] = "lock_enemy_icon"
template_one_c["template_window_target_x"] = 1038
template_one_c["template_window_target_y"] = 801
template_one_c["template_width"] = 19
template_one_c["template_height"] = 19
template_one_c["target_search_type"] = "multiple_match"
template_one_c["target_search_return"] = "skill_no"
template_one_c["template_area_list"] = [
    {
        "x": 1198,
        "y": 801,
        "skill_no": 4
    },
    {
        "x": 1118,
        "y": 801,
        "skill_no": 5
    },
    {
        "x": 1038,
        "y": 801,
        "skill_no": 6
    }
]

show_image = True
out_put_file = False
output_file_dir = ""
# new_item,tem_img = get_new_item_template(new_template_img_file_dir,template_one_c,img_process_method_name,test_show= show_image)
# with open(config_dir, 'r', encoding='utf-8') as f:
#     template_info_list = json.load(f)
#
# output_img_dir = project_root/"src/assets/images/new_all_in_one_template.png"
# new_template_info_list,combine_img=merge_two_config_and_img(template_info_list,new_item,tem_img,output_img_dir)
#
# new_config_dir = project_root/"src/assets/config/image_info/image_template_info_new.json"
# with open(new_config_dir, 'w', encoding='utf-8') as f:
#     json.dump(new_template_info_list, f, indent=2)  # 文件里会写入 "resize": false
# imwrite_chinese(output_img_dir, combine_img)
#
# print(new_item)


config1_dir = project_root / "src/assets/config/image_info/image_template_info.json"
config2_dir = project_root / "src/assets/config/image_info/char_123_active.json"
config3_dir = project_root / "src/assets/config/image_info/all_char_head_icon_small2.json"

config_list = []
with open(config1_dir, 'r', encoding='utf-8') as f:
    config_list.append(json.load(f))
with open(config2_dir, 'r', encoding='utf-8') as f:
    config_list.append(json.load(f))
with open(config3_dir, 'r', encoding='utf-8') as f:
    config_list.append(json.load(f))

for item in config_list[0]:
    item["target_search_type"] = "single_match"
    item["load_image"] = True
    item["category"] = "reinforce_active"
for item in config_list[1]:
    item["target_search_type"] = "single_match"
    item["load_image"] = True
    item["category"] = "char_absent"
for item in config_list[2]:
    item["target_search_type"] = "multiple_match"
    item["load_image"] = True
    item["category"] = "all_char_head_icon"
output_img_dir = "src/assets/images/new_all_in_one_template.png"
template_new_r, combine_img_r = combine_two_config_and_image_from_file(config_list, output_img_dir)

new_config_path = project_root / "src/assets/config/image_info/new_image_template_info.json"
with open(new_config_path, 'w', encoding='utf-8') as f:
    json.dump(template_new_r, f, indent=2)  # 文件里会写入 "resize": false
imwrite_chinese(output_img_dir, combine_img_r)

# 一次性的
# def old_config_add_new_shit():
#     with open(config_dir, 'r', encoding='utf-8') as f:
#         template_info_list = json.load(f)
#         for info in template_info_list:
#             if "target_search_type" not in info:
#                 if "template_area_list" not in info:
#                     info["target_search_type"] = "single_target"
#                 else:
#                     if len(info["template_area_list"]) == 1:
#                         info["target_search_type"] = "single_target"
#                         if "target_search_return" not in info:
#                             info["target_search_return"] = "index"
#                     elif len(info["template_area_list"]) >1:
#                         info["target_search_type"] = "multiple_targets"
#                         if "target_search_return" not in info:
#                             info["target_search_return"] = "index"
#
#     with open(project_root/"src/assets/config/image_info/image_template_info2.json", 'w', encoding='utf-8') as f:
#         json.dump(template_info_list, f, indent=2)  # 文件里会写入 "resize": false

# old_config_add_new_shit()
