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

output_dir = "src/tests/images/auto/"
# test_cases = ["mc_lock_enemy_4_True.png", "mc_lock_enemy_5_False.png", "mc_lock_enemy_6_False.png"]

filename = "mc_lock_enemy_5_False.png"
img_c = imread_chinese(f"{output_dir}{filename}")
tar_window_h, tar_window_w = img_c.shape[:2]
tem_window_w, tem_window_h = 1600, 900
l = {"template_window_width": 1600, "template_window_height": 900,
     "template_area_list": [{"x": 1198, "y": 801, "skill_no": 4}, {"x": 1118, "y": 801, "skill_no": 5},
                            {"x": 1038, "y": 801, "skill_no": 6}], "template_width": 20, "template_height": 20}
target_v = int(filename.split("_")[3])
for i in l['template_area_list']:
    if i["skill_no"] == target_v:
        tem_target_x, tem_target_y = i["x"], i["y"]
tem_w = l["template_width"]
tem_h = l["template_height"]
position_group = IconPosition.RIGHT_BOTTOM
print("tar_window_w:", tar_window_w, "tar_window_h:", tar_window_h, "tem_window_w:", tem_window_w,
      "tem_window_h:", tem_window_h, "tem_target_x:", tem_target_x, "tem_target_y:", tem_target_y, "tem_w:",
      tem_w, "tem_h:", tem_h)
roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_are_by_default(tar_window_w, tar_window_h, tem_window_w,
                                                                       tem_window_h, tem_target_x, tem_target_y,
                                                                       tem_w, tem_h, position_group,
                                                                       w_variance=1,
                                                                       h_variance=1)

target_img_sub = get_sub_image_from_image(img_c, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
target_img_sub = cv2.resize(target_img_sub,None,fx=5,fy=5)
# 读取图像
img = target_img_sub
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
    if key == ord('q'): # 按 'q' 键退出
        break

cv2.destroyAllWindows()