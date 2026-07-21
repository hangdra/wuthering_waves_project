# @Author  : liuha
# @Time    : 2026/7/16 18:16
# @File    : capture_image.py
import cv2

from src.core.input.input_sim import InputUtils
from src.core.vision.wgc import ZBLWindowGrabber
from src.core.vision.window_capture import WindowCapture
from src.utils.get_game_window_id import GetGameWindowId
from src.utils.read_write_image_from_filesys import imwrite_chinese,imread_chinese
from PIL import Image
import win32gui
import win32api
import time
from src.utils.image_dealer import hconcat_pad, get_grey_image, pad_image, \
    concat_images_with_padding_new
from src.utils.log import logger


import cv2
import numpy as np

from src.utils.tools import get_root_dir


def get_str(*args):
    str_list = ""
    for arg in args:
        str_list= str_list+str(arg)
    return str_list



def test_capture_image(name="test_out"):
    window_name = "鸣潮  "
    game_window_instance = GetGameWindowId(window_name=window_name)
    input_instance = InputUtils(game_window_instance)
    # window_capture_old = WindowCapture(game_window_instance)
    window_capture = ZBLWindowGrabber(game_window_instance)
    img = window_capture.get_frame()
    height, width = img.shape[:2]
    # img_old = window_capture_old.capture_fast_numpy()

    output_dir = "src/tests/images/auto/chars/"
    output_name = name+str(width)+"_"+str(height)
    if img is not None:
        if isinstance(img, Image.Image):
            img.save(f"{output_dir}{output_name}.png")
        else:
            imwrite_chinese(f"{output_dir}{output_name}.png", img)
    window_capture.close()
    # output_name = "test_out_old"
    # if img_old is not None:
    #     if isinstance(img_old, Image.Image):
    #         img_old.save(f"{output_dir}frame_{output_name}.png")
    #     else:
    #         imwrite_chinese(f"{output_dir}frame_{output_name}.png", img_old)
    # window_capture_old.close()


def get_image_xy_wh(x, y, x2, y2):
    window_name = "鸣潮  "
    game_window_instance = GetGameWindowId(window_name=window_name)
    input_instance = InputUtils(game_window_instance)
    window_capture = ZBLWindowGrabber(game_window_instance)
    img = window_capture.get_frame()
    window_capture.close()
    return img[y:y2, x:x2]


def test_move_mouse():
    window_name = "鸣潮  "
    game_window_instance = GetGameWindowId(window_name=window_name)
    input_instance = InputUtils(game_window_instance)
    logger.info("test_move_mouse===================================")
    game_window_instance.reget_hwnd_id()
    hwnd = game_window_instance.hwnd_id
    # x, y = 1435, 452
    # input_instance.click(x, y)
    # exit()
    start_x, start_y = 66, 200
    item_x = 1
    item_y = 5
    start_item_x, start_item_y = 0, 4
    # item_x = 1
    # item_y = 2
    x_delta = 109
    y_delta = 126

    output_dir = "src/tests/images/auto/"
    output_name = "all_char_pic"
    image_template_concat = imread_chinese(f"{output_dir}frame_{output_name}.png")
    logger.info("image_template_concat.shape" + str(image_template_concat.shape))
    for y_i in range(start_item_y,item_y):
        print("y_i________________________________", y_i)
        for x_i in range(item_x):
            x_new = start_x + x_delta * x_i
            y_new = start_y + y_delta * y_i
            # abs_x, abs_y = win32gui.ClientToScreen(hwnd, (int(x_new), int(y_new)))
            input_instance.click(x_new, y_new)
            print("x_i", x_i, "y_i", y_i, "over")
            time.sleep(0.5)
            print("_______________________________char detail")

            x, y = 1378, 452  # 1
            input_instance.click(x, y)
            x, y = 1392, 452  # 2
            input_instance.click(x, y)
            x, y = 1406, 452  # 3
            input_instance.click(x, y)
            x, y = 1420, 452  # 3.5-4
            input_instance.click(x, y)
            x, y = 1434, 452  # 4.5
            input_instance.click(x, y)
            # time.sleep(0.2)
            # x, y = 1429, 445
            # input_instance.click(x, y)
            print("_______________________________char detail over")
            time.sleep(1.5)
            # if image_template_concat is not None:
            #     logger.info("image_template_concat is not None" + str(image_template_concat[0:1, 0:1]))

            image_char = get_image_xy_wh(1485, 156, 1531, 205)#46，49
            # if image_template_concat is not None:
                # logger.info("image_template_concat is not None after get_image_xy_wh" + str(image_template_concat[0:1, 0:1]))
            # logger.info("new image_char"+str(image_char[0:1, 0:1]))
            # if image_template_concat is not None:
            #     logger.info("image_template_concat is not None" + str(image_template_concat[0:1, 0:1]))
                # cv2.imshow("", image_template_concat)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            if image_template_concat is None:
                image_template_concat = image_char
                # cv2.imshow("", image_template_concat)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            else:
                str_log = get_str("_________image_template_concat", x_i, y_i, image_template_concat[0:1, 0:1], " image_char",image_char[0:1, 0:1])
                # logger.info(str_log)
                image_template_concat = concat_images_with_padding_new(image_template_concat, image_char)
            # logger.info("finished,image_template_concat"+str(image_template_concat[0:1, 0:1]))
            # cv2.imshow("", image_template_concat)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # cv2.imshow("", image_template_concat)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            x, y = 1510, 54
            input_instance.click(x, y)

            time.sleep(2)
    # output_dir = "src/tests/images/auto/"
    # output_name = "all_char_pic"
    imwrite_chinese(f"{output_dir}frame_{output_name}.png", image_template_concat)

from pathlib import Path
import os
import json
import matplotlib.pyplot as plt
from src.utils.image_dealer import remove_part_of_img
project_root = get_root_dir(__file__)

def remove_and_recombine_img():
    project_root = Path(__file__).parent.parent.parent
    all_template_info_file_name = "src/assets/config/image_info/all_char_head_icon_small2.json"
    image_abs_path = os.path.join(project_root, all_template_info_file_name)
    with open(image_abs_path, 'r', encoding='utf-8') as f:
        head_icon_info = json.load(f)

    all_head_icon_data = imread_chinese(head_icon_info[0]["image_file_from_project_root"])#F:\code\wuthering_waves_ok_copy\src\tests\images\auto\frame_all_char_pic.png
    # all_head_icon_data = imread_chinese("src/assets/images/all_char_head_icon.png")
    print("all_head_icon_data.shape" + str(all_head_icon_data.shape))
    image_template_concat = None
    for i in range(len(head_icon_info)):
        item = head_icon_info[i]
        item["template_img_data"] = all_head_icon_data[
            item["template_y"]:item["template_y"] + item["template_height"],
            item["template_x"]:item["template_x"] + item["template_width"]]
        left_tem = remove_part_of_img(item["template_img_data"],remove_left_percentage=0.15,remove_bottom_percentage=0.15)
        print("left_tem", left_tem.shape)
        if image_template_concat is None:
            image_template_concat = left_tem
        else:
            image_template_concat = concat_images_with_padding_new(image_template_concat, left_tem)
    output_dir = "src/tests/images/auto/"
    output_name = "all_char_pic_remove_part"
    imwrite_chinese(f"{output_dir}frame_{output_name}.png", image_template_concat)


def show_every_char():
    project_root = Path(__file__).parent.parent.parent
    all_template_info_file_name = "src/assets/config/image_info/all_char_head_icon_small2.json"
    image_abs_path = os.path.join(project_root, all_template_info_file_name)
    with open(image_abs_path, 'r', encoding='utf-8') as f:
        head_icon_info = json.load(f)

    all_head_icon_data = imread_chinese(head_icon_info[0]["image_file_from_project_root"])
    image_template_concat = None
    for i in range(len(head_icon_info)):
        item = head_icon_info[i]
        item["template_img_data"] = all_head_icon_data[
            item["template_y"]:item["template_y"] + item["template_height"],
            item["template_x"]:item["template_x"] + item["template_width"]]
        left_tem = remove_part_of_img(item["template_img_data"],remove_left_percentage=0.15,remove_bottom_percentage=0.15)
        left_tem = pad_image(left_tem,0,20,0,60)
        cv2.putText(left_tem, str(f"{item["name_pinyin"]}"),
                    (0, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        if image_template_concat is None:
            image_template_concat = left_tem
        else:
            image_template_concat = concat_images_with_padding_new(image_template_concat, left_tem)
    output_dir = "src/tests/images/auto/"
    output_name = "all_char_with_pinyin_name"
    imwrite_chinese(f"{output_dir}frame_{output_name}.png", image_template_concat)

    cv2.imshow("", image_template_concat)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
img_dic = {}
def load_img( path, flag=cv2.IMREAD_COLOR):
    if path not in img_dic:
        img_dic[path] = imread_chinese(path,flag=flag)
    return img_dic[path]

def show_config_image(config_filename):
    project_root = Path(__file__).parent.parent.parent
    all_template_info_file_name = "src/assets/config/image_info/"+config_filename
    image_abs_path = os.path.join(project_root, all_template_info_file_name)
    with open(image_abs_path, 'r', encoding='utf-8') as f:
        head_icon_info = json.load(f)

    image_template_concat = None
    for i in range(len(head_icon_info)):
        all_head_icon_data = load_img(head_icon_info[i]["image_file_from_project_root"])
        item = head_icon_info[i]
        item["template_img_data"] = all_head_icon_data[
            item["template_y"]:item["template_y"] + item["template_height"],
            item["template_x"]:item["template_x"] + item["template_width"]]
        left_tem = remove_part_of_img(item["template_img_data"], remove_left_percentage=0.15,
                                      remove_bottom_percentage=0.15)
        left_tem = pad_image(left_tem, 0, 20, 0, 60)
        name_show = "name"
        if "name_pinyin" in item:
            name_show = "name_pinyin"
        cv2.putText(left_tem, str(f"{item[name_show]}"),
                    (0, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        if image_template_concat is None:
            image_template_concat = left_tem
        else:
            image_template_concat = concat_images_with_padding_new(image_template_concat, left_tem)
    output_dir = "src/tests/images/auto/"

    output_name = config_filename.split(".")[0]
    imwrite_chinese(f"{output_dir}frame_{output_name}.png", image_template_concat)

    cv2.imshow("", image_template_concat)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
from src.utils.load_all_template import my_LoadAllTemplate_instance
def capture_image_and_check_char(name=""):
    window_name = "鸣潮  "
    game_window_instance = GetGameWindowId(window_name=window_name)
    # window_capture_old = WindowCapture(game_window_instance)
    window_capture = ZBLWindowGrabber(game_window_instance)
    while True:
        img = window_capture.get_frame()
        height, width = img.shape[:2]
        # img_old = window_capture_old.capture_fast_numpy()
        target_char_dic = my_LoadAllTemplate_instance.get_match_char_template_head_icon(img)
        print("len(target_char_dic):", len(target_char_dic))
        char_out = ""
        for i in range(1,4,1):
            if str(i) in target_char_dic:
                char_out = char_out + target_char_dic[str(i)]["name"]+"_"
        output_dir = "src/tests/images/auto/chars/"
        output_name = name+char_out+str(width)+"_"+str(height)
        output_full_name = f"{output_dir}{output_name}.png"
        if len(target_char_dic)!=3:
            time.sleep(1)
            continue
        if not Path(output_full_name).exists():
            if img is not None:
                if isinstance(img, Image.Image):
                    img.save(f"{output_dir}{char_out}.png")
                else:
                    imwrite_chinese(output_full_name, img)
        time.sleep(0.5)
    window_capture.close()

# test_move_mouse(test_move_mouse)

test_capture_image(name="mc_技能cd")
# capture_image_and_check_char("mc_技能cd")
# import shutil
# remove_and_recombine_img()
# image_template_concat = imread_chinese(f"src/tests/images/auto/frame_all_char_pic_remove_part.png")
# imwrite_chinese(f"src/tests/images/auto/frame_all_char_pic_remove_part_grey.png", get_grey_image(image_template_concat))
# # 复制到当前目录并重命名
# shutil.copy(project_root/"src/tests/images/auto/frame_all_char_pic_remove_part.png", project_root/"src/assets/images/char_head_small_0_15.png")
# shutil.copy(project_root/"src/tests/images/auto/frame_all_char_pic_remove_part_grey.png", project_root/"src/assets/images/char_head_small_0_15_grey.png")

# show_config_image("image_template_info.json")
# show_every_char()
# output_dir = "src/tests/images/auto/"
# output_name = "frame_all_char_pic_remove_part.png"



# x, y = 1429, 445
# x, y = 1510, 54
# x, y = 1406, 452
# abs_x, abs_y = win32gui.ClientToScreen(game_window_instance.hwnd_id, (int(x), int(y)))
# print("_______cursor abs_x,abs_y", abs_x, abs_y)
# # abs_x, abs_y = (1471,799)
# win32api.SetCursorPos((abs_x,abs_y))
# print("over")
# time.sleep(2)
# print("sleep over")
# win32api.SetCursorPos((abs_x,abs_y))
# print("_______cursor abs_x,abs_y", abs_x, abs_y)
# print("over")
