# @Author  : liuha
# @Time    : 2026/7/12 11:02
# @File    : test_read_file.py
import json
#
# data = {
#     "resize": False,
#     "min_success_score": 0.7
# }
#
# with open('../src/assets/config/config.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, indent=2)  # 文件里会写入 "resize": false
#
#
#
# with open('../src/assets/config/template_info.json', 'r', encoding='utf-8') as f:
#     config = json.load(f)
#
#
# for i in config:
#     # print(i)
#     print(i['name'], i['resize'])

from pypinyin import lazy_pinyin

from src.utils.image_dealer import IconPosition

text = "你好世界"
pinyin_list = lazy_pinyin(text)


def get_str_combine(list_str):
    result = ""
    for item in list_str:
        result += item
    return result


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

icon_json_one = {
    "image_file_from_project_root": "src/assets/images/all_char_head_icon2.png",
    "image_grey_file_from_project_root": "src/assets/images/all_char_head_icon_grey2.png",
    "image_file": "all_char_head_icon_grey.png",
    "category":"char_head_icon",
    "name": "",
    "name_pinyin": "",
    "target_process_method": "",
    "template_process_method":"",
    "icon_position_group": "right_top",
    "min_success_score": 0.7,
    "template_window_width": 1600,
    "template_window_height": 900,
    # "template_search_area_method": -1,
    # "template_match_method": -1,
    "template_area_list":[{
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
      }],
    "resize": False,
    "template_x": 0,
    "template_y": 0
}
all_icon_json_list = []
for i in range(0, len(names)):
    icon_json_copy = icon_json_one.copy()
    icon_json_copy["name"] = names[i]
    icon_json_copy["name_pinyin"] = names_pinyin[i]
    # icon_json_copy["template_width"] = 46
    # icon_json_copy["template_height"] = 49
    icon_json_copy["image_file_from_project_root"] = "src/assets/images/char_head_small_0_15.png"
    icon_json_copy["image_grey_file_from_project_root"] = "src/assets/images/char_head_small_0_15_grey.png"

    icon_json_copy["x_variance_factor"]=2
    icon_json_copy["y_variance_factor"]=2
    icon_json_copy["template_width"] = 34
    icon_json_copy["template_height"] = 34
    icon_json_copy["template_x"] = 0 + i * icon_json_copy["template_width"]
    all_icon_json_list.append(icon_json_copy)

with open('../src/assets/config/image_info/all_char_head_icon_small3.json', 'w', encoding='utf-8') as f:
    json.dump(all_icon_json_list, f, indent=2)  # 文件里会写入 "resize": false


template_one = {
    "image_file_from_project_root": "",
    "image_file": "",
    "name": "con_percentage",
    "target_process_method": "",
    "icon_position_group": "center_bottom",
    "min_success_score": 0.7,
    "template_window_width": 1600,
    "template_window_height": 900,
    "template_window_target_x": 597,
    "template_window_target_y": 810,
    "template_width": 50,
    "template_height": 50,
    "resize": False,
    "template_x": 0,
    "template_y": 0,
    "load_image": False
  }
# with open('../src/assets/config/image_info/image_template_info.json', 'r', encoding='utf-8') as f:
#     template_info_list = json.load(f)
#
# for item in template_info_list:
#     if item["name"] in ["e_forte_not_ready","e_forte","mouse_forte","mouse_forte_not_ready"]:
#         item["load_image"] = True
#
# with open('../src/assets/config/image_info/image_template_info2.json', 'w', encoding='utf-8') as f:
#     json.dump(template_info_list, f, indent=2)  # 文件里会写入 "resize": false

# def icon_width_factor(image_origin_width, image_origin_height):
#     """
#     计算目标分辨率下图标宽度(使用deepseek得到不同分辨率下图标的宽度，用于后续不同分辨率之间比较比例数值）
#     """
#     ratio = image_origin_width / image_origin_height
#     if ratio >= 2.3:
#         # 带鱼屏 2560×1080	2.37 (21:9) 3440×1440	2.39 (21:9) 5120×1440	3.55 （32:9）
#         return image_origin_width / 32.2  # 最终技能图标宽度
#     else:
#         return image_origin_width / 24  # 最终技能图标宽度
# def cal_c(tar_window_w, tar_window_h, tem_window_w, tem_window_h, tem_target_x, tem_target_y,
#           template_position: IconPosition = IconPosition.CENTER_BOTTOM):
#     """
#     tar_window_w:目标图像宽度
#     tar_window_h:目标图像高度
#     tem_window_w:模板原始图像宽度
#     tem_window_h:模板原始图像高度
#     tem_target_x:模板原始图像目标坐标x
#     tem_target_y:模板原始图像目标坐标y
#     计算模板图像坐标在目标图像中的坐标
#     """
#     if tem_window_w == tar_window_w and tem_window_h == tar_window_h:
#         return tem_target_x, tem_target_y, 1
#     else:
#         tar_s_divided_tem_s_in = icon_width_factor(tar_window_w, tar_window_h) / icon_width_factor(tem_window_w,
#                                                                                                    tem_window_h)
#         if template_position == IconPosition.RIGHT_BOTTOM:
#             target_x = tar_window_w - (tem_window_w - tem_target_x) * tar_s_divided_tem_s_in
#             target_y = tar_window_h - (tem_window_h - tem_target_y) * tar_s_divided_tem_s_in
#             # return int(target_x), int(target_y), tar_s_divided_tem_s_in
#         elif template_position == IconPosition.CENTER_BOTTOM:
#             target_x = tar_window_w / 2 + (tem_target_x - tem_window_w / 2) * tar_s_divided_tem_s_in
#             target_y = tar_window_h / 2 + (tem_target_y - tem_window_h / 2) * tar_s_divided_tem_s_in
#             # return int(target_x), int(target_y), tar_s_divided_tem_s_in
#         elif template_position == IconPosition.RIGHT_TOP:
#             target_x = tar_window_w - (tem_window_w - tem_target_x) * tar_s_divided_tem_s_in
#             target_y = tem_target_y*tar_s_divided_tem_s_in
#         else:
#             raise Exception("cal_c not supported template_position: {}".format(template_position))
#         return int(target_x), int(target_y), tar_s_divided_tem_s_in
#
# # from src.utils.image_dealer import cal_c_new
# tem_window_w = 1600
# tem_window_h = 900
# tem_target_x = 1445
# tem_target_y = 396
# tar_w,tar_h = 1920,1440
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_TOP)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
#
# tar_w,tar_h = 1920,1080
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_TOP)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
#
# tar_w,tar_h = 1920,1200
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_TOP)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
#
#
# tar_w,tar_h = 2560,1440
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_TOP)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
#
# tar_w,tar_h = 3440,1440
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_TOP)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
#
# tar_w,tar_h = 1600,900
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_TOP)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
#
# print("next")
# tem_target_x = 1478
# tem_target_y = 771
# tar_w,tar_h = 1280,960
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_BOTTOM)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
# tar_w,tar_h = 1920,1440
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_BOTTOM)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
# tar_w,tar_h = 2560,1080
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_BOTTOM)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
# tar_w,tar_h = 3440,1440
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_BOTTOM)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)
# tar_w,tar_h = 1600,900
# tar_x, tar_y, tar_s_divided_tem_s = cal_c(tar_w,tar_h,tem_window_w,tem_window_h,tem_target_x,tem_target_y,IconPosition.RIGHT_BOTTOM)
# print("tar_w,tar_h ",tar_w,tar_h ,"result tar_x, tar_y,",tar_x, tar_y, tar_s_divided_tem_s)

# tar_x = tar_s_divided_tem_s*(1478-1600/2)+tar_w/2
# print("tar_x:", tar_x)

