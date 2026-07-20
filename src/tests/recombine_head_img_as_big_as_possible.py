# @Author  : liuha
# @Time    : 2026/7/20 03:14
# @File    : recombine_head_img_as_big_as_possible.py
from src.utils.image_dealer import remove_part_of_img, concat_images_with_padding_new, calculate_target_template_xy, \
    get_position_group, get_search_area, get_sub_image_from_image, match_template_probability, pad_image
from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir
import cv2

project_root = get_root_dir(__file__)
import cv2
import numpy as np
from typing import List, Tuple, Union

import cv2
import numpy as np
from typing import List, Tuple, Union
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese

def concat_images_grid_with_rects(
        images: List[np.ndarray],
        max_width: int,
        align: str = 'top',
        fill_color: Union[int, tuple] = (0, 0, 0, 255)
) -> Tuple[np.ndarray, List[Tuple[int, int, int, int]]]:
    """
    水平拼接图像，超出 max_width 时自动换行，并返回每个原图在最终图像中的位置。

    参数：
        images: 图像列表 (numpy array)
        max_width: 每行最大宽度（像素）
        align: 垂直对齐方式，'top' / 'bottom' / 'center'
        fill_color: 填充颜色，自动适配通道数

    返回：
        (result_image, rects_list)
        - result_image: 拼接后的最终图像
        - rects_list: 列表，每个元素为 (x, y, w, h)，对应 images 中相同顺序的图像
                      (x, y) 是左上角坐标，(w, h) 是原始图像的宽高（未缩放）
    """
    if not images:
        raise ValueError("图像列表为空")

    # ---------- 1. 统一通道数 ----------
    def get_dims(img):
        if len(img.shape) == 2:
            return img.shape[0], img.shape[1], 1
        else:
            return img.shape[0], img.shape[1], img.shape[2]

    # 收集所有图像通道数
    c_list = [get_dims(img)[2] for img in images]
    target_c = max(c_list)

    def convert_to_channels(img, target_c):
        h, w, c = get_dims(img)
        if c == target_c:
            return img
        if target_c == 1:
            if c == 3:
                return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            elif c == 4:
                return cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGRA2BGR), cv2.COLOR_BGR2GRAY)
            else:
                return img
        elif target_c == 3:
            if c == 1:
                return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif c == 4:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                return img
        elif target_c == 4:
            if c == 1:
                bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                return cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
            elif c == 3:
                return cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            else:
                return img
        else:
            raise ValueError(f"不支持的通道数: {target_c}")

    unified_images = [convert_to_channels(img, target_c) for img in images]

    # 适配 fill_color 到目标通道
    if isinstance(fill_color, (int, float)):
        fill_color = (fill_color,) * target_c
    else:
        fill_color = tuple(fill_color)
        if len(fill_color) < target_c:
            fill_color = fill_color + (fill_color[-1],) * (target_c - len(fill_color))
        elif len(fill_color) > target_c:
            fill_color = fill_color[:target_c]
    fill_color = tuple(int(c) for c in fill_color)

    # ---------- 2. 按行分组 ----------
    rows = []  # 每行是一个图像列表
    current_row = []
    current_width = 0

    for img in unified_images:
        h, w = img.shape[:2]
        if not current_row:
            current_row.append(img)
            current_width = w
        else:
            if current_width + w > max_width:
                rows.append(current_row)
                current_row = [img]
                current_width = w
            else:
                current_row.append(img)
                current_width += w
    if current_row:
        rows.append(current_row)

    # ---------- 3. 处理每一行，生成行图像及该行内每个子图的矩形 ----------
    # 存储所有行的图像和每个子图的全局矩形（相对于最终画布）
    row_images = []
    all_rects = []  # 最终返回的矩形列表，与原始 images 顺序一致
    y_offset = 0  # 当前行在最终画布中的垂直偏移

    for row in rows:
        # 计算该行最大高度
        max_h = max([img.shape[0] for img in row])

        # 存储本行的 pad 后图像以及每个子图在行图像中的偏移 (x, top, w, h)
        padded_imgs = []
        row_rects = []  # 本行每个子图在行图像中的矩形 (x, top, w, h)
        x_offset = 0

        for img in row:
            h, w = img.shape[:2]
            # 计算垂直补边
            if align == 'top':
                top = 0
                bottom = max_h - h
            elif align == 'bottom':
                top = max_h - h
                bottom = 0
            else:  # center
                top = (max_h - h) // 2
                bottom = max_h - h - top

            # 补边生成 pad 图像
            pad_img = cv2.copyMakeBorder(img, top, bottom, 0, 0,
                                         cv2.BORDER_CONSTANT, value=fill_color)
            padded_imgs.append(pad_img)
            # 记录该子图在行图像中的位置（x, y, 原始宽, 原始高）
            row_rects.append((x_offset, top, w, h))
            x_offset += w  # 水平拼接时宽度不变，直接累加

        # 水平拼接本行所有 pad 图像
        row_image = np.hstack(padded_imgs)
        row_images.append(row_image)

        # 将该行每个子图的坐标转换为全局坐标（加上当前 y_offset）
        for (x, top, w, h) in row_rects:
            all_rects.append((x, y_offset + top, w, h))

        # 更新 y_offset 为下一行做准备（累加本行高度）
        y_offset += row_image.shape[0]

    # ---------- 4. 将所有行垂直拼接，并统一宽度（右侧补白） ----------
    # 计算最大行宽
    max_row_width = max([img.shape[1] for img in row_images])

    # 将每行宽度补齐到 max_row_width（右侧补白）
    padded_rows = []
    for img in row_images:
        h, w = img.shape[:2]
        if w < max_row_width:
            pad_right = max_row_width - w
            img_padded = cv2.copyMakeBorder(img, 0, 0, 0, pad_right,
                                            cv2.BORDER_CONSTANT, value=fill_color)
            padded_rows.append(img_padded)
        else:
            padded_rows.append(img)

    result = np.vstack(padded_rows)
    result = np.ascontiguousarray(result)

    return result, all_rects


names = ["秧秧·玄翎", "丽贝卡", "西格莉卡", "莫宁", "仇远", "洛瑟菈", "达妮娅", "陆·赫斯", "琳奈", "嘉贝莉娜", "露西",
         "绯雪", "爱弥斯",
         "千咲", "尤诺", "奥古斯塔", "弗洛洛", "露帕", "卡提希娅", "夏空", "赞妮", "坎特雷拉", "布兰特", "菲比",
         "洛可可", "珂莱塔", "椿",
         "守岸人", "相里要", "折枝", "长离", "今汐", "吟霖", "忌炎", "卡卡罗", "凌阳", "鉴心", "维里奈", "安可",
         "漂泊者", "卜灵", "灯灯",
         "釉瑚", "渊武", "丹瑾", "散华", "莫特斐", "桃祈", "秋水", "白芷", "秧秧", "炽霞"]
# names_pinyin = []
# for name in names:
#     names_pinyin.append(get_str_combine(lazy_pinyin(name)))
# print(names_pinyin)
names_pinyin = ['yangyang·xuanling', 'libeika', 'xigelika', 'moning', 'chouyuan', 'luosela', 'daniya', 'lu·hesi',
                'linnai', 'jiabeilina', 'luxi', 'feixue', 'aimisi', 'qianxiao', 'younuo', 'aogusita', 'fuluoluo',
                'lupa', 'katixiya', 'xiakong', 'zanni', 'kanteleila', 'bulante', 'feibi', 'luokeke', 'kelaita', 'chun',
                'shouanren', 'xiangliyao', 'zhezhi', 'changli', 'jinxi', 'yinlin', 'jiyan', 'kakaluo', 'lingyang',
                'jianxin', 'weilinai', 'anke', 'piaobozhe', 'buling', 'dengdeng', 'youhu', 'yuanwu', 'danjin', 'sanhua',
                'motefei', 'taoqi', 'qiushui', 'baizhi', 'yangyang', 'chixia']

names_need_cut_off_left = ["陆·赫斯", "琳奈", "露帕", "赞妮", "布兰特", "珂莱塔", "釉瑚", "渊武", "秋水", "忌炎",
                           "卡卡罗"]
names_need_cut_off_top = ["珂莱塔"]
names_need_cut_off_right = ["仇远", "陆·赫斯"]
names_need_cut_off_bottom = ["椿", "釉瑚", "渊武", "忌炎", "卡卡罗", "布兰特"]

special_remove = {"安可":[0.01,0.01,0.01,0.01]}

def get_img_and_recombine(default_remove_percentage = 0.05):
    w_tem_o, h_tem_o = 46, 49
    all_head_img = imread_chinese("src/assets/images/all_char_head_icon.png")

    combine_img_inner = None
    combine_config_info = []
    last_x_for_new_tem = 0
    images = []  # 列表
    images_bigger = []
    tem_w_h, tem_w_w = all_head_img.shape[:2]
    img_no = int(tem_w_w / w_tem_o)
    for i in range(img_no):
        config_info_one = {}

        img_this = all_head_img[:h_tem_o, i * w_tem_o:(i + 1) * w_tem_o]
        left_tem = img_this
        remove_left = default_remove_percentage
        remove_top = default_remove_percentage
        remove_right = default_remove_percentage
        remove_bottom = default_remove_percentage
        if names[i] in names_need_cut_off_left:
            remove_left = 0.15
        if names[i] in names_need_cut_off_top:
            remove_top = 0.15
        if names[i] in names_need_cut_off_right:
            remove_right = 0.15
        if names[i] in names_need_cut_off_bottom:
            remove_bottom = 0.15
        if names[i] in special_remove:
            remove_left = special_remove[names[i]][0]
            remove_top = special_remove[names[i]][1]
            remove_right = special_remove[names[i]][2]
            remove_bottom = special_remove[names[i]][3]
        left_tem = remove_part_of_img(left_tem, remove_left, remove_bottom, remove_top, remove_right)
        # left_tem = cv2.resize(left_tem, None, fx=3, fy=3)
        images_bigger.append(cv2.resize(left_tem, None, fx=3, fy=3))
        images.append(left_tem)

        # TODO
        # print(names[i])
        # print("combine_img_inner.shape", combine_img_inner.shape)

    # 设置最大宽度，例如 1920（屏幕宽度），或自行指定
    MAX_WIDTH = 2560  # 根据实际情况调整

    # 拼接并自动换行
    combined, rects = concat_images_grid_with_rects(images, max_width=MAX_WIDTH, align='top', fill_color=(0, 0, 0, 255))

    combined_b, rects_b = concat_images_grid_with_rects(images_bigger, max_width=MAX_WIDTH, align='top', fill_color=(255, 255, 255, 255))
    print(rects)
    for i, (x, y, w, h) in enumerate(rects_b):
        print(f"Image {i}: 左上角 ({x}, {y}), 宽 {w}, 高 {h}")
        cv2.rectangle(combined_b, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(combined_b, str(f"{names_pinyin[i][:10]} "), (x, y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    # 显示
    # cv2.imshow("Grid", combined)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # 打印每个图像的坐标和尺寸
    combined_c = combined.copy()
    for i, (x, y, w, h) in enumerate(rects):
        print(f"Image {i}: 左上角 ({x}, {y}), 宽 {w}, 高 {h}")
        # cv2.rectangle(combined_c, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText(combined_c, str(f"{names_pinyin[i][:10]} "), (x, y + 20),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        config_info_one = {"name": names[i], "name_pinyin": names_pinyin[i], "min_success_score": 0.7,
                           "x_variance_factor": 2,
                           "y_variance_factor": 2,
                           "icon_position_group": "right_top", "template_window_width": 1600,
                           "template_window_height": 900,
                           "template_x": x,
                           "template_y": y,
                           "template_width": w,
                           "template_height": h,
                           "template_area_list": [
                               {
                                   "x": 1478,
                                   "y": 191,
                                   "index": 1
                               },
                               {
                                   "x": 1478,
                                   "y": 301,
                                   "index": 2
                               },
                               {
                                   "x": 1478,
                                   "y": 411,
                                   "index": 3
                               }
                           ],
                           "load_image": True, "target_search_type": "multiple_match", "category": "all_char_head_icon"}
        combine_config_info.append(config_info_one)
    # 例如，您可以在最终图像上绘制矩形框来验证
    # for (x, y, w, h) in rects:
    #     cv2.rectangle(combined, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Verification", combined_b)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return combined, combine_config_info

remove_percentage = 0.01
remove_percentage_str = str(remove_percentage).split(".")[1]
img_a, config_a = get_img_and_recombine(remove_percentage)
print(config_a)

import os
import json
import time

tar_img_dir = "src/tests/images/auto/chars/"
file_result = {}
tar_sub_img = {}
counter = 0
time_s = time.perf_counter()
do_work = True

if not do_work:
    exit()
for filename in os.listdir(project_root / tar_img_dir):
    # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
    if filename.startswith("mc"):
        if filename != "mc1920_1080.png":
            # continue
            pass

        counter = counter + 1
        file_result[filename] = {}
        find_char = []
        tar_img = imread_chinese(f"{tar_img_dir}{filename}")
        print(tar_img.shape)
        tar_window_height, tar_window_width = tar_img.shape[:2]

        for tem_config in config_a:
            tem_x, tem_y, tem_w, tem_h, template_window_width, template_window_height = tem_config["template_x"], \
            tem_config["template_y"], tem_config[
                "template_width"], tem_config["template_height"], tem_config["template_window_width"], tem_config[
                "template_window_height"]
            tem_img = img_a[tem_y:tem_y + tem_h, tem_x:tem_x + tem_w]
            tem_search_area_list = tem_config["template_area_list"]
            position_group = get_position_group(tem_config["icon_position_group"])
            x_variance_factor, y_variance_factor = tem_config["x_variance_factor"], tem_config["y_variance_factor"]
            if tem_search_area_list is not None:
                for search_area in tem_search_area_list:
                    search_index = search_area["index"]
                    tem_tar_x, tem_tar_y = search_area["x"], search_area["y"]
                    target_x, target_y, tar_s_divided_tem_s = calculate_target_template_xy(tar_window_width,
                                                                                           tar_window_height,
                                                                                           template_window_width,
                                                                                           template_window_height,
                                                                                           tem_tar_x, tem_tar_y,
                                                                                           position_group)
                    x_variance_factor, y_variance_factor = 1.5, 1.5
                    roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_area(target_x, target_y,
                                                                                 tar_window_width,
                                                                                 tar_window_height,
                                                                                 tem_w, tem_h,
                                                                                 tar_s_divided_tem_s, x_variance_factor,
                                                                                 y_variance_factor)
                    target_img_sub = get_sub_image_from_image(tar_img, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
                    tar_sub_img[filename + str(search_index)] = target_img_sub
                    resized = cv2.resize(tem_img, None, fx=tar_s_divided_tem_s,fy=tar_s_divided_tem_s)
                    # cv2.imshow(tem_config["name_pinyin"], resized)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                    use_color_img = False
                    use_canny_in = False
                    cv_method = "TM_CCOEFF_NORMED_use_canny" + str(use_canny_in)+"_use_color_"+str(use_color_img)
                    res = match_template_probability(resized, target_img_sub, use_color=use_color_img,
                                                     use_canny=use_canny_in,
                                                     visualize_path="src/tests/images/auto/matches/" +
                                                                    filename.split("_")[0] + "_" + str(
                                                         search_index) + "_" + tem_config["name"],
                                                     method=cv2.TM_CCOEFF_NORMED)


                    print("匹配分数:", res['score'])
                    print("缩放比例:", res['scale'])
                    print("位置:", res['top_left'], res['bottom_right'])
                    candidates = {"name": tem_config["name"], "index": str(search_index), "confidence": res['score'],
                                  "scale": res['scale'], "top_left": res['top_left'],
                                  "bottom_right": res['bottom_right']}
                    if (str(search_index) not in file_result[filename]) or (
                            candidates["confidence"] > file_result[filename][str(search_index)]["confidence"]):
                        file_result[filename][str(search_index)] = candidates
                    # 测试匹配效果
                    # if filename == "mc1600_900_守岸人.png" and (
                    #         tem_config["name"] == "露西" ):
                    #     # 绘制匹配结果
                    #     img_out = concat_images_with_padding_new(target_img_sub, resized).copy()
                    #     top_left, bottom_right = res['top_left'], res['bottom_right']
                    #     cv2.rectangle(img_out, top_left, bottom_right, (0, 255, 0), 2)
                    #     cv2.putText(img_out, str(f"{candidates["confidence"]:0.4f} {candidates["name"]}"),
                    #                 (0, 15),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    #     cv2.imshow(tem_config["name_pinyin"], img_out)
                    #     cv2.waitKey(0)
                    #     cv2.destroyAllWindows()
time_e = time.perf_counter()
avg_time = (time_e - time_s) / counter if counter > 0 else 0.0
print(f"all match done {counter}/{counter} time cost : {(time_e - time_s):.4f}, average time cost :{avg_time:.4f} ")
print(file_result)
padding_image = None
for filename in file_result.keys():
    file_result_item = file_result[filename]
    counter = 0
    for index in file_result_item.keys():
        counter += 1
        item = file_result_item[index]
        vis = tar_sub_img[filename + str(index)].copy()
        hv,wv = vis.shape[:2]
        if counter==3:
            mr = 60
        else:
            mr = 30
        bottom_add = 30
        left_tem = pad_image(vis, 0, bottom_add, 0, mr)
        cv2.rectangle(left_tem, item["top_left"], item["bottom_right"], (0, 255, 0), 2)
        cv2.putText(left_tem, str(f"{item["confidence"]:0.6f} "), (0, bottom_add+hv-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(left_tem, str(f"{item["name"]}"), (0, bottom_add+hv-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        # imwrite_chinese(
        #     "src/tests/images/auto/matches/" + filename.split("_")[0] + "_" + str(index) + "_" + item[
        #         "name"] + f"{item["confidence"]:0.4f}.png", vis)
        if padding_image is None:
            padding_image = left_tem
        else:
            padding_image = concat_images_with_padding_new(padding_image, left_tem)
imwrite_chinese(
    "src/tests/images/auto/matches/all_matches"+remove_percentage_str+"_"+cv_method+".png", padding_image)