
import os

from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root
from src.utils.image_dealer import *
import json

Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()

config_list = []
con = {
    "category": "energy_percentage",
    "name": "con_percentage",
    "icon_position_group": "center_bottom",
    "min_success_score": 0.7,
    "template_window_width": 1600,
    "template_window_height": 900,
    "template_window_target_x": 600,
    "template_window_target_y": 813,
    "template_width": 45,
    "template_height": 45,
    "load_image": False,
    "x_variance_factor": 1.4,
    "y_variance_factor": 1.4,
}
config_list.append(con)
ult = {
    "category": "energy_percentage",
    "name": "ult_percentage",
    "icon_position_group": "right_bottom",
    "min_success_score": 0.7,
    "template_window_width": 1600,
    "template_window_height": 900,
    "template_window_target_x": 1478,
    "template_window_target_y": 771,
    "template_width": 69,
    "template_height": 69,
    "load_image": False,
    "x_variance_factor": 1.4,
    "y_variance_factor": 1.4,
}
config_list.append(ult)

config_name = "con_ult_percentage_no_template_img.json"
with open(Root_dir / (Config_dir + config_name), 'w',
          encoding='utf-8') as f:
    json.dump(config_list, f, indent=2)  # 文件里会写入 "resize": false