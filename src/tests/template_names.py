# @Author  : liuha
# @Time    : 2026/7/17 01:20
# @File    : check_template_data.py

from src.utils.load_all_template import my_LoadAllTemplate_instance
import cv2

head_icon_info = my_LoadAllTemplate_instance.head_icon_info

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
                'shouanren', 'xiangliyao', 'zhezhi', 'zhangli', 'jinxi', 'yinlin', 'jiyan', 'kakaluo', 'lingyang',
                'jianxin', 'weilinai', 'anke', 'piaobozhe', 'buling', 'dengdeng', 'youhu', 'yuanwu', 'danjin', 'sanhua',
                'motefei', 'taoqi', 'qiushui', 'baizhi', 'yangyang', 'chixia']



# for item in head_icon_info:
#     if item["name"]=="炽霞":
#         cv2.imshow(item["name_pinyin"], item["template_img_data"])
#         cv2.imshow(item["name"], item["template_img_data"])
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()


