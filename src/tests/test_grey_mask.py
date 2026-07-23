# @Author  : liuha
# @Time    : 2026/7/19 05:37
# @File    : test_hsv.py



import cv2
import numpy as np

def nothing(x):
    pass

from src.utils.image_dealer import *
from pathlib import Path
import os
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese
from src.assets.config.config_others_all import *

project_root = Path(__file__).parent.parent.parent
output_dir = "src/tests/images/auto/"
output_dir = "src/tests/images/template/"
file_result = {}
tar_sub_img = {}
# for filename in os.listdir(project_root / output_dir):
    # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
find_char = []
filename = "mc冰_1600_900.png"
filename = "露西满E_4k.png"

file_name = "src/tests/images/template/丽贝卡左键满169.png"
file_name = "src/tests/images/auto/mc_lock_enemy_4_True.png"
# file_name = "src/tests/images/auto/mc_lock_enemy_6_False.png"
tar_img = imread_chinese(file_name)


tar_window_h,tar_window_w = tar_img.shape[:2]
tem_window_w, tem_window_h = 1600, 900
tem_target_x, tem_target_y = 1038, 801
tem_w = 20
tem_h = 20
l ={"template_window_width":1600,"template_window_height":900,"template_area_list":[{"x":1198,"y":801,"skill_no":4},{"x":1118,"y":801,"skill_no":5},{"x":1038,"y":801,"skill_no":6}],"template_width":20,"template_height":20}
target_v = 4
for i in l['template_area_list']:
    if i["skill_no"] == target_v:
        tem_target_x, tem_target_y =i["x"],i["y"]
tem_w = l["template_width"]
tem_h = l["template_height"]
position_group = IconPosition.RIGHT_BOTTOM
print("tar_window_w:",tar_window_w,"tar_window_h:",tar_window_h,"tem_window_w:",tem_window_w,"tem_window_h:",tem_window_h,"tem_target_x:",tem_target_x,"tem_target_y:",tem_target_y,"tem_w:",tem_w,"tem_h:",tem_h)
roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_are_by_default(tar_window_w, tar_window_h, tem_window_w, tem_window_h, tem_target_x, tem_target_y, tem_w, tem_h, position_group,
                          w_variance=3,
                          h_variance=3)
target_img_sub = get_sub_image_from_image(tar_img, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)

# 读取图像
# img = target_img_sub
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



def nothing(x):
    pass


# 读取图片并转为灰度
img = target_img_sub
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 创建窗口和滑块
cv2.namedWindow('Trackbar')
cv2.createTrackbar('Threshold', 'Trackbar', 127, 255, nothing)

while True:
    # 获取滑块值
    thresh = cv2.getTrackbarPos('Threshold', 'Trackbar')

    # 二值化（灰度图只需一个阈值）
    _, mask = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)

    # 显示
    cv2.imshow('Original', gray)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()