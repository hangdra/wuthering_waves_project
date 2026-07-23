# @Author  : liuha
# @Time    : 2026/7/18 13:37
# @File    : test_cordinate_transform.py
from src.assets.config.config_others_all import mask_colors
from src.utils.image_dealer import *

tar_window_w, tar_window_h = 3440, 1440
tem_window_w, tem_window_h = 1600, 900
tem_target_x, tem_target_y = 600, 813
tem_w = 45
tem_h = 45
# tar_s_divided_tem_s_in = get_tar_s_divided_tem_s(tar_window_w, tar_window_h, tem_window_w, tem_window_h)
template_position = IconPosition.CENTER_BOTTOM
res = calculate_target_template_xy(tar_window_w, tar_window_h, tem_window_w, tem_window_h,
                                   tem_target_x, tem_target_y,
                                   template_position)

white_color = {  # 用于检测UI元素可用状态的白色颜色范围。
    'r': (253, 255),  # Red range
    'g': (253, 255),  # Green range
    'b': (253, 255)  # Blue range
}

con_colors = {  # 不同角色属性的协奏值能量环的颜色范围列表。
    "spectro": {
        'r': (205, 235),
        'g': (190, 222),  # for yellow spectro
        'b': (90, 130)
    },
    "electric": {
        'r': (150, 190),  # Red range
        'g': (95, 140),  # Green range for purple electric
        'b': (210, 249)  # Blue range
    },
    "fire": {
        'r': (200, 230),  # Red range
        'g': (100, 130),  # Green range    for red fire
        'b': (75, 105)  # Blue range
    },
    "ice": {
        'r': (60, 95),  # Red range
        'g': (150, 180),  # Green range    for blue ice
        'b': (210, 245)  # Blue range
    },
    "wind": {
        'r': (70, 110),  # Red range
        'g': (215, 250),  # Green range    for green wind
        'b': (155, 190)  # Blue range
    },
    "havoc": {
        'r': (190, 220),  # Red range
        'g': (65, 105),  # Green range    for havoc
        'b': (145, 175)  # Blue range
    }
}


def calculate_color_percentage(image, color_ranges):
    print("color_ranges", color_ranges)
    mask = cv2.inRange(image, (color_ranges['b'][0], color_ranges['g'][0], color_ranges['r'][0]),
                       (color_ranges['b'][1], color_ranges['g'][1], color_ranges['r'][1]))
    target_pixels = cv2.countNonZero(mask)
    total_pixels = image.size / 3
    percentage = target_pixels / total_pixels
    return percentage


import cv2


from pathlib import Path
import os
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese
import math

project_root = Path(__file__).parent.parent.parent
output_dir = "src/tests/images/template/"
file_result = {}
tar_sub_img = {}
for filename in os.listdir(project_root / output_dir):
    # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
    if filename != "露西满E_4k.png":
        pass
        # continue
    file_result[filename] = {}
    find_char = []
    print(f"{output_dir}{filename}")
    tar_img = imread_chinese(f"{output_dir}{filename}")
    tar_window_h, tar_window_w = tar_img.shape[:2]
    tem_window_w, tem_window_h = 1600, 900
    tem_target_x, tem_target_y = 600, 813
    tem_w = 45
    tem_h = 45
    position_group = IconPosition.CENTER_BOTTOM
    print("tar_window_w:", tar_window_w, "tar_window_h:", tar_window_h, "tem_window_w:", tem_window_w, "tem_window_h:",
          tem_window_h, "tem_target_x:", tem_target_x, "tem_target_y:", tem_target_y, "tem_w:", tem_w, "tem_h:", tem_h)
    roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_are_by_default(tar_window_w, tar_window_h, tem_window_w,
                                                                           tem_window_h, tem_target_x, tem_target_y,
                                                                           tem_w, tem_h, position_group,
                                                                           w_variance=1.4,
                                                                           h_variance=1.4)
    target_img_sub = get_sub_image_from_image(tar_img, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
    tar_s_divided_tem_s = get_tar_s_divided_tem_s(tar_window_w, tar_window_h,
                                                  tem_window_w, tem_window_h)
    print("tar_s_divided_tem_s", tar_s_divided_tem_s)

    print("target_img_sub.shape", target_img_sub.shape)
    for ele in con_colors.keys():
        print(ele)
        ele_color = mask_colors[ele]
        percentage = compute_element_fill_ratio(target_img_sub, ele_color,
                                                outer_radius=round(tem_w * tar_s_divided_tem_s / 2),
                                                inner_radius=round(tem_w * tar_s_divided_tem_s / 2 * 0.8),
                                                visualize=False)
        # percentage = calculate_color_percentage(target_img_sub,ele_color)
        file_result[filename][ele] = percentage
        print(f"{output_dir}{filename}")
        print(f"{ele} :{percentage * 100:.4f}%")
        # exit()
        # cv2.imshow(ele+str(percentage), target_img_sub)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

print(file_result)
