import os

from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root

from src.utils.image_dealer import *
import json
import time

Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()

config_name = "char_123_active.json"
# with open(Root_dir / (Config_dir + config_name), 'r', encoding='utf-8') as f:
#     template_info_list = json.load(f)
#
# from src.assets.config.config_others_all import *
#
# init_set["lazy_init"] = True
# init_set["img_show"] = False
# from src.utils.load_all_template import my_LoadAllTemplate_instance
#
# my_LoadAllTemplate_instance.all_template_one_from_root = "src/assets/config/image_info/" + config_name
# my_LoadAllTemplate_instance.load_all_template()
#
# print("len(my_LoadAllTemplate_instance.template_all_list)", len(my_LoadAllTemplate_instance.template_all_list))
# category_want = template_info_list[0]["category"]
#
# output_dir = "src/tests/images/auto/"
# file_result = {}
# tar_sub_img = {}
# time_s = time.perf_counter()

config_name_list = ["char_123_active.json","char_123_active_grey.json"]

file_list = ['mc4_1600_900.png', 'mc3_1600_900.png', 'mc_lock_enemy_6_False.png', 'mc_lock_enemy_4_True.png',
             'mc5_1600_900.png', 'mc1920_1200.png', 'mctest_1600_900.png', 'mc8_1600_900.png',
             'mc电2_1600_900.png', 'mc3440_1440.png', 'mc光_1600_900.png', 'mc冰2_1600_900.png',
             'mc9_1600_900.png', 'mc火_1600_900.png', 'mc1920_1200_rebecca_heavy.png', 'mc_技能cd1600_900.png',
             'mc风_1600_900.png', 'mc1920_1440.png', 'mc电_1600_900.png', 'mc1920_1080.png', 'mc火2_1600_900.png',
             'mc7_1600_900.png', 'mc暗_1600_900.png', 'mc_lock_enemy_5_False.png', 'mc6_1600_900.png',
             'mc2560_1440.png', 'mc丽贝卡_霰弹_1600_900.png', 'mc丽贝卡_双枪_1600_900.png', 'mc1600_900_守岸人.png',
             'mc冰_1600_900.png']

file_list = file_list[:3]


confing_dig = {}
for config_name in config_name_list:
    with open(Root_dir / (Config_dir + config_name), 'r', encoding='utf-8') as f:
        template_info_list = json.load(f)

    from src.assets.config.config_others_all import *

    init_set["lazy_init"] = True
    init_set["img_show"] = False
    from src.utils.load_all_template import my_LoadAllTemplate_instance

    my_LoadAllTemplate_instance.all_template_one_from_root = "src/assets/config/image_info/" + config_name
    my_LoadAllTemplate_instance.load_all_template()

    # print("len(my_LoadAllTemplate_instance.template_all_list)", len(my_LoadAllTemplate_instance.template_all_list))
    category_want = template_info_list[0]["category"]

    tar_img_dir = "src/tests/images/auto/"
    file_result = {}
    time_s = time.perf_counter()

    counter = 0
    result_key_count = 0
    for filename in os.listdir(Root_dir / tar_img_dir):
        # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
        if filename.startswith("mc"):
            if filename not in file_list:
                continue
                # pass
            # print("________filename", filename)
            counter = counter + 1
            file_result[filename] = {}
            tar_img = imread_chinese(f"{tar_img_dir}{filename}")
            res = my_LoadAllTemplate_instance.match_by_category_default(tar_img, category_want,return_mex_one=False,
                                                                        allow_muti_each_return=False)

            file_result[filename] = res
    confing_dig[config_name] = file_result

    time_e = time.perf_counter()
    avg_time = (time_e - time_s) / counter if counter > 0 else 0.0
    confidence_all = 0
    for filename_item in file_result.keys():
        item = file_result[filename_item]
        sk1 = "char_1"
        sk2 = "char_2"
        sk3 = "char_3"
        if sk1 in item:
            result_key_count +=1
            confidence_all += item[sk1]["confidence"]
        if sk2 in item:
            result_key_count += 1
            confidence_all += item[sk2]["confidence"]
        if sk3 in item:
            result_key_count += 1
            confidence_all += item[sk3]["confidence"]
    print(
        f"=================config_name '{config_name}' all match done {counter}/{counter} average confidence ****:{((confidence_all / result_key_count) if result_key_count!=0 else None):.4f}**** time cost : {(time_e - time_s):.4f}, average time cost :{avg_time:.4f} ")


stats = my_LoadAllTemplate_instance.load_img_by_name.get_stats()
print("统计结果: load_img_by_name", stats)

stats = match_template_probability.get_stats()
print("统计结果 match_template_probability:", stats)

stats = my_LoadAllTemplate_instance.match_template_by_name_default.get_stats()
print("统计结果: match_template_by_name_default", stats)

stats = my_LoadAllTemplate_instance.match_by_category_default.get_stats()
print("统计结果: match_by_category_default", stats)

print(confing_dig)
print("over")

 #. 差不多 'char_123_active.json' 'char_123_active_grey.json'
# =================config_name 'char_123_active.json' all match done 3/3 average confidence ****:0.7079**** time cost : 0.1398, average time cost :0.0466
# =================config_name 'char_123_active_grey.json' all match done 3/3 average confidence ****:0.7845**** time cost : 0.1194, average time cost :0.0398
# 统计结果: load_img_by_name {'calls': 36, 'total_time': '0.00477', 'avg_time': '0.00013', 'max': '0.00314', 'p99': '0.00314', 'p90': '0.00008', 'p1': '0.00000'}
# 统计结果 match_template_probability: {'calls': 18, 'total_time': '0.01927', 'avg_time': '0.00107', 'max': '0.00958', 'p99': '0.00958', 'p90': '0.00123', 'p1': '0.00035'}
# 统计结果: match_template_by_name_default {'calls': 18, 'total_time': '0.02427', 'avg_time': '0.00135', 'max': '0.01281', 'p99': '0.01281', 'p90': '0.00131', 'p1': '0.00039'}
# 统计结果: match_by_category_default {'calls': 6, 'total_time': '0.02434', 'avg_time': '0.00406', 'max': '0.01473', 'p99': '0.01473', 'p90': '0.01473', 'p1': '0.00151'}
# #

