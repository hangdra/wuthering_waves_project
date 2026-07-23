import os

from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir, get_config_dir_from_root
from src.utils.image_dealer import *
import json

Root_dir = get_root_dir(__file__)

template_one = {
    "image_file_from_project_root": "src/assets/images/",
    "image_file": "",
    "category": "enemy_lock",
    # "name": "enemy_lock",
    "target_search_type": "multiple_match",
    # "template_no":2,
    # "template_list":[],
    "target_search_return": "skill_no",
    "target_process_method": "",
    "template_process_method": "",
    "force_grey": False,
    "use_canny": False,
    "icon_position_group": "right_top",
    "min_success_score": 0.7,
    "template_window_width": 1600,
    "template_window_height": 900,
    "template_area_list": [
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
    ],

    "x_variance_factor": 2,
    "y_variance_factor": 2,
}

# tem_img_true_big = cv2.resize(tem_img_true, None,fx=3, fy=3)
# tem_img_false_big = cv2.resize(tem_img_false, None,fx=3, fy=3)
# tem_img_big_combine = concat_images_grid_with_rects([tem_img_true_big, tem_img_false_big])
# cv2.imshow("", tem_img_big_combine[0])
# cv2.waitKey(0)
# cv2.destroyAllWindows()


output_img_dir = "src/assets/images/enemy_lock.png"
filename_t = os.path.basename(output_img_dir)

config_out = []
template_one_c = template_one.copy()
sub_item = {"name": "enemy_lock_on", "template_width": 20, "template_height": 20,"mask_color":"lock_on",
            "template_x": 0, "template_y": 0, "image_file_from_project_root": output_img_dir, "image_file": filename_t}
template_one_c.update(sub_item)

template_one_c2 = template_one.copy()
sub_item2 = {"name": "enemy_lock_off", "template_width": 20, "template_height": 20,"mask_color":"lock_off",
             "template_x": 20, "template_y": 0, "image_file_from_project_root": output_img_dir,
             "image_file": filename_t}
template_one_c2.update(sub_item2)

# template_one_c["template_no"] = len(template_one_c["template_list"])
# template_one_c2 = template_one.copy()
# template_one_c2["name"] = "enemy_lock_off"
# template_one_c2["mask_color"] = "lock_off"
# template_one_c2["template_x"] = template_one_c["template_x"]+template_one_c["template_width"]
# template_one_c2["template_y"] = 0
# config_out.append(template_one_c2)
config_out.append(template_one_c)
config_out.append(template_one_c2)

template_img_dir = "src/tests/images/auto/mc_lock_enemy_4_True.png"
img_skill_no_4 = 4
skill_4_enemy_lock_true_img = imread_chinese(template_img_dir)

template_img_dir = "src/tests/images/auto/mc丽贝卡_双枪_1600_900.png"
img_skill_no_6 = 6
skill_6_enemy_lock_false_img = imread_chinese(template_img_dir)

tem_w, tem_h = sub_item["template_width"], sub_item["template_width"]
for item in template_one_c["template_area_list"]:
    if item["skill_no"] == img_skill_no_4:
        tem_tar_x = item["x"]
        tem_tar_y = item["y"]

tem_img_true = skill_4_enemy_lock_true_img[tem_tar_y:tem_tar_y + tem_h, tem_tar_x:tem_tar_x + tem_w]

for item in template_one_c["template_area_list"]:
    if item["skill_no"] == img_skill_no_6:
        tem_tar_x = item["x"]
        tem_tar_y = item["y"]

tem_img_false = skill_6_enemy_lock_false_img[tem_tar_y:tem_tar_y + tem_h, tem_tar_x:tem_tar_x + tem_w]

tem_img_combine = concat_images_grid_with_rects([tem_img_true, tem_img_false])

# output_img_dir = "src/assets/images/enemy_lock.png"
# template_one_c["image_file_from_project_root"] = output_img_dir
# filename_t = os.path.basename(output_img_dir)
# template_one_c["image_file"] = filename_t

# output
# img
imwrite_chinese(output_img_dir, tem_img_combine[0])
# config
output_conf_name = "enemy_lock.json"

with open(Root_dir / (get_config_dir_from_root() + output_conf_name), 'w', encoding='utf-8') as f:
    json.dump(config_out, f, indent=2)  # 文件里会写入 "resize": false
