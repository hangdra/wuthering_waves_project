import os

from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root
from src.utils.image_dealer import *
import json

Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()

template_one = {
    "image_file_from_project_root": "src/assets/images/char_head_small_0_15.png",
    "image_grey_file_from_project_root": "src/assets/images/char_head_small_0_15_grey.png",
    "image_file": "all_char_head_icon_grey.png",
    "category": "char_head_icon",
    "name": "\u79e7\u79e7\u00b7\u7384\u7fce",
    "name_pinyin": "yangyang\u00b7xuanling",
    "target_process_method": "",
    "template_process_method": "",
    "icon_position_group": "right_top",
    "min_success_score": 0.7,
    "template_window_width": 1600,
    "template_window_height": 900,
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
    "template_x": 0,
    "template_y": 0,
    "target_search_type": "multiple_match",
    "target_search_return": "index",
    "x_variance_factor": 2,
    "y_variance_factor": 2,
    "template_width": 34,
    "template_height": 34
}

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

special_remove = {"安可": [0.05, 0.01, 0.01, 0.01]}


def get_img_and_recombine(default_remove_percentage=0.05, file_path=None):
    w_tem_o, h_tem_o = 46, 49
    all_head_img = imread_chinese("src/assets/images/all_char_head_icon.png")

    combine_img_inner = None
    combine_config_info = []
    last_x_for_new_tem = 0
    images = []  # 列表
    images_bigger = []
    tem_w_h, tem_w_w = all_head_img.shape[:2]
    img_no = int(tem_w_w / w_tem_o)
    remove_per_char = {}
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
        print(names[i])
        print("before,left_tem.shape", left_tem.shape)
        left_tem, start_xy = remove_part_of_img(left_tem, remove_left, remove_bottom, remove_top, remove_right)
        print("after,left_tem.shape", left_tem.shape, start_xy)
        remove_per_char[names[i]] = start_xy
        # left_tem = cv2.resize(left_tem, None, fx=3, fy=3)
        images_bigger.append(cv2.resize(left_tem, None, fx=3, fy=3))
        images.append(left_tem)

        # TODO
        # print(names[i])
        # print("combine_img_inner.shape", combine_img_inner.shape)

    # 设置最大宽度，例如 1920（屏幕宽度），或自行指定
    MAX_WIDTH = 2560  # 根据实际情况调整

    # 拼接并自动换行
    combined, rects = concat_images_grid_with_rects(images, max_width=MAX_WIDTH, align='top', fill_color=(0, 0, 0))

    combined_b, rects_b = concat_images_grid_with_rects(images_bigger, max_width=MAX_WIDTH, align='top',
                                                        fill_color=(255, 255, 255, 255))
    print(rects)
    for i, (x, y, w, h) in enumerate(rects_b):
        # print(f"Image {i}: 左上角 ({x}, {y}), 宽 {w}, 高 {h}")
        cv2.rectangle(combined_b, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(combined_b, str(f"{names_pinyin[i][:10]} "), (x, y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    # 显示
    # cv2.imshow("Grid", combined)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # 打印每个图像的坐标和尺寸
    combined_c = combined.copy()
    origin_tem_w, origin_tem_w = 34, 34
    print("_______remove_per_char", remove_per_char)
    filename_t = os.path.basename(file_path)
    for i, (x, y, w, h) in enumerate(rects):
        # print(f"Image {i}: 左上角 ({x}, {y}), 宽 {w}, 高 {h}")
        # cv2.rectangle(combined_c, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText(combined_c, str(f"{names_pinyin[i][:10]} "), (x, y + 20),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        config_info_one = {"image_file_from_project_root": file_path,
                           "image_file": filename_t,
                           "name": names[i], "name_pinyin": names_pinyin[i], "min_success_score": 0.7,
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
                                   "x": 1478 + remove_per_char[names[i]][0],
                                   "y": 191 + remove_per_char[names[i]][1],
                                   "index": 1
                               },
                               {
                                   "x": 1478 + remove_per_char[names[i]][0],
                                   "y": 301 + remove_per_char[names[i]][1],
                                   "index": 2
                               },
                               {
                                   "x": 1478 + remove_per_char[names[i]][0],
                                   "y": 411 + remove_per_char[names[i]][1],
                                   "index": 3
                               }
                           ],
                           "load_image": True, "target_search_type": "multiple_match", "category": "all_char_head_icon",
                           "target_search_return": "index"}
        combine_config_info.append(config_info_one)
    # 例如，您可以在最终图像上绘制矩形框来验证
    # cv2.imshow("Verification", combined_b)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return combined, combine_config_info


r_per_list = [0.15]
for remove_percentage in r_per_list:
    remove_percentage_str = str(remove_percentage).split(".")[1]
    if len(remove_percentage_str) == 1:
        remove_percentage_str = remove_percentage_str + "0"
    output_img_dir = Img_dir + "all_char_head_icon_small_" + remove_percentage_str + ".png"
    img_a, config_a = get_img_and_recombine(remove_percentage, output_img_dir)
    print("img_a.shape", img_a.shape)
    imwrite_chinese(output_img_dir, img_a)


    with open(Root_dir / (Config_dir + 'all_char_head_icon_small_' + remove_percentage_str + '.json'), 'w',
              encoding='utf-8') as f:
        json.dump(config_a, f, indent=2)  # 文件里会写入 "resize": false

    config_g = config_a.copy()
    filename_grey = Img_dir + "all_char_head_icon_small_" + remove_percentage_str + "_grey.png"
    filename_t = os.path.basename(filename_grey)
    for item in config_g:
        item["image_file_from_project_root"] = filename_grey
        item["image_file"] = filename_t
        item["force_grey"] = True

    img_grey = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    imwrite_chinese(filename_grey, img_grey)
    with open(Root_dir / (Config_dir + 'all_char_head_icon_small_' + remove_percentage_str + '_grey.json'), 'w',
              encoding='utf-8') as f:
        json.dump(config_g, f, indent=2)  # 文件里会写入 "resize": false

print("over")
