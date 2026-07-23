import os

from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root

from src.utils.image_dealer import *
import json
import time
from src.utils.data_store import data_store

Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()

config_name_list = ["con_ult_percentage_no_template_img.json"]

tar_img_dir = "src/tests/images/auto/"
img_file_list = ['mc4_1600_900.png', 'mc3_1600_900.png', 'mc_lock_enemy_6_False.png', 'mc_lock_enemy_4_True.png',
                 'mc5_1600_900.png', 'mc1920_1200.png', 'mctest_1600_900.png', 'mc8_1600_900.png',
                 'mc电2_1600_900.png', 'mc3440_1440.png', 'mc光_1600_900.png', 'mc冰2_1600_900.png',
                 'mc9_1600_900.png', 'mc火_1600_900.png', 'mc1920_1200_rebecca_heavy.png', 'mc_技能cd1600_900.png',
                 'mc风_1600_900.png', 'mc1920_1440.png', 'mc电_1600_900.png', 'mc1920_1080.png', 'mc火2_1600_900.png',
                 'mc7_1600_900.png', 'mc暗_1600_900.png', 'mc_lock_enemy_5_False.png', 'mc6_1600_900.png',
                 'mc2560_1440.png', 'mc丽贝卡_霰弹_1600_900.png', 'mc丽贝卡_双枪_1600_900.png', 'mc1600_900_守岸人.png',
                 'mc冰_1600_900.png']

confing_dic = {}
for config_name in config_name_list:
    confing_dic[config_name] = {}
    with open(Root_dir / (Config_dir + config_name), 'r', encoding='utf-8') as f:
        template_info_list = json.load(f)

    from src.assets.config.config_others_all import *

    init_set["lazy_init"] = True
    init_set["img_show"] = True
    from src.utils.load_all_template import my_LoadAllTemplate_instance

    my_LoadAllTemplate_instance.all_template_one_from_root = (Config_dir + config_name)
    my_LoadAllTemplate_instance.load_all_template()

    time_s = time.perf_counter()
    counter = 0
    for img_file_path in img_file_list:
        confing_dic[config_name][img_file_path] = {}
        tar_img = imread_chinese(f"{tar_img_dir}{img_file_path}")
        # def get_enery_percentage(self, tar_img, template_name, ele_type):
        tem_name_list = ["con_percentage", "ult_percentage"]
        ele_type_list = ["spectro", "electric", "fire", "ice", "wind", "havoc"]
        for tem_name in tem_name_list:
            confing_dic[config_name][img_file_path][tem_name] = {}
            for ele_type in ele_type_list:
                counter += 1
                data_store.set_name(img_file_path+"  "+tem_name+"  "+ele_type)
                res = my_LoadAllTemplate_instance.get_enery_percentage(tar_img, tem_name, ele_type)
                confing_dic[config_name][img_file_path][tem_name][ele_type] = res

    time_e = time.perf_counter()
    avg_time = (time_e - time_s) / counter if counter > 0 else 0.0

    print(
        f"=================config_name '{config_name}' all match done {counter}/{counter} average time cost : {(time_e - time_s):.4f}, average time cost :{avg_time:.4f} ")
data_store.get_merged_img_and_show()

data_store.clear()
print("confing_dic",confing_dic)