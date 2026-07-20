# @Author  : liuha
# @Time    : 2026/7/19 04:59
# @File    : test_get_ult_percentage.py




from src.utils.image_dealer import *
from pathlib import Path
import os
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese
from src.assets.config.config_others_all import *

project_root = Path(__file__).parent.parent.parent
output_dir = "src/tests/images/template/"
file_result = {}
tar_sub_img = {}
for filename in os.listdir(project_root / output_dir):
    if filename != "露西03_4k.png" :
        # pass
        continue
    file_result[filename] = {}
    find_char = []
    print(f"{output_dir}{filename}")
    tar_img = imread_chinese(f"{output_dir}{filename}")
    tar_window_h,tar_window_w = tar_img.shape[:2]
    tem_window_w, tem_window_h = 1600, 900
    tem_target_x, tem_target_y = 1478, 771
    tem_w = 69
    tem_h = 69
    position_group = IconPosition.RIGHT_BOTTOM
    print("tar_window_w:",tar_window_w,"tar_window_h:",tar_window_h,"tem_window_w:",tem_window_w,"tem_window_h:",tem_window_h,"tem_target_x:",tem_target_x,"tem_target_y:",tem_target_y,"tem_w:",tem_w,"tem_h:",tem_h)
    roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_are_by_default(tar_window_w, tar_window_h, tem_window_w, tem_window_h, tem_target_x, tem_target_y, tem_w, tem_h, position_group,
                              w_variance=1.2,
                              h_variance=1.2)
    target_img_sub = get_sub_image_from_image(tar_img, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
    tar_s_divided_tem_s = get_tar_s_divided_tem_s(tar_window_w, tar_window_h,
                                                  tem_window_w, tem_window_h)
    print("target_img_sub.shape",target_img_sub.shape)
    tar_w,tar_h = target_img_sub.shape[:2]

    for ele in con_colors_hsv.keys():
        print(ele)
        ele_color = con_colors_hsv[ele]
        percentage = compute_element_fill_ratio(target_img_sub, ele_color,start_angle=90,
                                                outer_radius=round(tem_w * tar_s_divided_tem_s / 2),
                                                inner_radius=round(tem_w * tar_s_divided_tem_s / 2 * 0.8),
                                                visualize=True)        # percentage = calculate_color_percentage(target_img_sub,ele_color)
        file_result[filename][ele] = percentage
        print(f"{output_dir}{filename}")
        print(f"{ele} :{percentage * 100:.4f}%")
        # exit()
        # cv2.imshow(ele+str(percentage), target_img_sub)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

print(file_result)