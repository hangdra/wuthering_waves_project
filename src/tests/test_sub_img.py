import os

from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root

from src.utils.image_dealer import *
import json
import time

Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()

test_img_dir = "src/tests/images/auto/"
img_name = "mc冰_1600_900.png"

img_this = imread_chinese(test_img_dir+img_name)
# cv2.imshow("", img_this)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


con_img = img_this[813:858,600:645]
con_img_b = cv2.resize(con_img,None,fx=10,fy=10)
# cv2.imshow("con", con_img_b)


ult_img = img_this[771:840,1478:1547]
tem_w,tem_h=69,69
tar_s_divided_tem_s=1

ult_img_b = cv2.resize(ult_img,None,fx=10,fy=10)

ele_color = "ice"
from src.assets.config.config_others_all import *
ult_percentage = compute_element_fill_ratio(ult_img,mask_colors[ele_color] ,
                                                outer_radius=round(tem_w * tar_s_divided_tem_s / 2),
                                                inner_radius=round(tem_w * tar_s_divided_tem_s / 2 * 0.8),
                                                start_angle=90,
                                                visualize=True)
print("ult_percentage",ult_percentage)


cv2.waitKey(0)
cv2.destroyAllWindows()