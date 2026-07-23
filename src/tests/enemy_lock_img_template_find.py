import os

from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root

from src.utils.image_dealer import *
import json
import time




Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()

config_name = "enemy_lock.json"
with open(Root_dir/(Config_dir+config_name), 'r', encoding='utf-8') as f:
    template_info_list = json.load(f)

from src.assets.config.config_others_all import *
init_set["lazy_init"]=True
init_set["img_show"]=False
from src.utils.load_all_template import my_LoadAllTemplate_instance
my_LoadAllTemplate_instance.all_template_one_from_root = "src/assets/config/image_info/"+config_name
my_LoadAllTemplate_instance.load_all_template()

print("len(my_LoadAllTemplate_instance.template_all_list)",len(my_LoadAllTemplate_instance.template_all_list))
category_want = template_info_list[0]["category"]






output_dir = "src/tests/images/auto/"
file_result = {}
tar_sub_img = {}
time_s = time.perf_counter()
file_list = ["mc_lock_enemy_4_True.png","mc_lock_enemy_5_False.png","mc_lock_enemy_6_False.png"]
# file_list = ["mc_lock_enemy_6_False.png"]

counter = 0
for filename in os.listdir(Root_dir / output_dir):
    # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
    if filename.startswith("mc"):
        if filename not in file_list:
            continue
            # pass
        print("________filename",filename)
        counter = counter + 1
        file_result[filename] = {}
        tar_img = imread_chinese(f"{output_dir}{filename}")
        res = my_LoadAllTemplate_instance.match_by_category_default(tar_img,category_want,allow_muti_each_return=False)

        file_result[filename] = res
time_e = time.perf_counter()
avg_time = (time_e - time_s) / counter if counter > 0 else 0.0
print(f"all match done {counter}/{counter} time cost : {(time_e - time_s):.4f}, average time cost :{avg_time:.4f} ")

print(file_result)