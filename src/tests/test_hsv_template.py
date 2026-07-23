# @Author  : liuha
# @Time    : 2026/7/19 05:37
# @File    : test_hsv.py
from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root, \
    get_test_auto_img_dir_from_root

Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()
Test_img_auto = get_test_auto_img_dir_from_root()


def nothing(x):
    pass


import cv2
import numpy as np
from src.utils.data_store import data_store
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese

from src.assets.config.config_others_all import *

config_name = "con_ult_percentage_no_template_img.json"
init_set["lazy_init"] = True
init_set["img_show"] = True
from src.utils.load_all_template import my_LoadAllTemplate_instance

my_LoadAllTemplate_instance.all_template_one_from_root = (Config_dir + config_name)
my_LoadAllTemplate_instance.load_all_template()

template_name_list = ["con_percentage", "ult_percentage"]
all_issue_list = []
issue_dic = {
    "tar_img_path": "",
    "tem_name": "",
    "issue_parameter": ""
}

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc3_1600_900.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)
issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc_lock_enemy_6_False.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)
issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc5_1600_900.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)
issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc1920_1200.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)
issue_dic1 = {
    "tar_img_path": Test_img_auto + "mctest_1600_900.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "ice"
}
all_issue_list.append(issue_dic1)
issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc8_1600_900.png",
    "tem_name": template_name_list[0],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc8_1600_900.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc电2_1600_900.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "electric"
}
all_issue_list.append(issue_dic1)

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc3440_1440.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc3440_1440.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "fire"
}
all_issue_list.append(issue_dic1)

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc火_1600_900.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc2560_1440.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc2560_1440.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "fire"
}
all_issue_list.append(issue_dic1)

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc丽贝卡_霰弹_1600_900.png",
    "tem_name": template_name_list[0],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)

issue_dic1 = {
    "tar_img_path": Test_img_auto + "mc丽贝卡_霰弹_1600_900.png",
    "tem_name": template_name_list[1],
    "issue_parameter": "spectro"
}
all_issue_list.append(issue_dic1)

choose_ele_type = "spectro"
# todo 完成所有测试 并确认修改 问题 元素的 color_mask
for issue in all_issue_list:

    tar_img = imread_chinese(issue["tar_img_path"])
    tem_name = issue["tem_name"]
    ele_type = issue["issue_parameter"]
    if ele_type != choose_ele_type:
        continue
    data_store.set_name(issue["tar_img_path"] + "  " + tem_name + "  " + ele_type)
    res = my_LoadAllTemplate_instance.get_enery_percentage(tar_img, tem_name, ele_type)

extra_img_list = ["mc_lock_enemy_4_True.png"]
for extra_img in extra_img_list:
    tar_img = imread_chinese(Test_img_auto + extra_img)
    for tem_name in ["con_percentage", "ult_percentage"]:
        data_store.set_name(extra_img + "  " + tem_name + "  " + choose_ele_type)
        my_LoadAllTemplate_instance.get_enery_percentage(tar_img, tem_name, choose_ele_type)

data_store.get_merged_img_and_show(show=False)
img_out_list = data_store.get_out_img()
print("img_out_list", len(img_out_list))
# todo 尝试根据ele_type 分开调色
for img in img_out_list:
    # img = cv2.resize(tar_img, (0, 0),fx=5, fy=5)
    # 读取图像
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 创建一个窗口
    cv2.namedWindow('Trackbars')

    # 创建6个滑块，分别控制H, S, V的下限和上限
    cv2.createTrackbar('H Low', 'Trackbars', 0, 179, nothing)
    cv2.createTrackbar('H High', 'Trackbars', 179, 179, nothing)
    cv2.createTrackbar('S Low', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('S High', 'Trackbars', 255, 255, nothing)
    cv2.createTrackbar('V Low', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('V High', 'Trackbars', 255, 255, nothing)

    while True:
        # 获取滑块当前的值
        h_low = cv2.getTrackbarPos('H Low', 'Trackbars')
        h_high = cv2.getTrackbarPos('H High', 'Trackbars')
        s_low = cv2.getTrackbarPos('S Low', 'Trackbars')
        s_high = cv2.getTrackbarPos('S High', 'Trackbars')
        v_low = cv2.getTrackbarPos('V Low', 'Trackbars')
        v_high = cv2.getTrackbarPos('V High', 'Trackbars')

        # 定义范围并创建掩码
        lower = np.array([h_low, s_low, v_low])
        upper = np.array([h_high, s_high, v_high])
        mask = cv2.inRange(hsv, lower, upper)

        # 显示掩码和原图
        cv2.imshow('Original', img)
        cv2.imshow('Mask', mask)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # 按 'q' 键退出
            break

    cv2.destroyAllWindows()
