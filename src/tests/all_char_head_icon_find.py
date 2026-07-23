import os

from src.utils.read_write_image_from_filesys import imread_chinese
from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root

from src.utils.image_dealer import *
import json
import time

Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()

config_name_list = ["all_char_head_icon_small_15.json","all_char_head_icon_small_15_grey.json"]

file_list = ['mc_鉴心_白芷_秧秧_1600_900.png', 'mc_露西_丽贝卡_尤诺1600_900.png',
             'mc_夏空_奥古斯塔_卡提希娅_1600_900.png', 'mc_今汐_吟霖_卡卡罗_1600_900.png',
             'mc_釉瑚_丹瑾_炽霞_1600_900.png', 'mc_维里奈_安可_漂泊者_1600_900.png',
             'mc_长离_守岸人_相里要_1600_900.png', 'mc_桃祈_灯灯_秋水_1600_900.png', 'mc_莫特斐_鉴心_白芷_1600_900.png',
             'mc_卜灵_渊武_散华_1600_900.png']

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

    output_dir = "src/tests/images/auto/chars/"
    file_result = {}
    tar_sub_img = {}
    time_s = time.perf_counter()


    # file_list = ['mc_鉴心_白芷_秧秧_1600_900.png']

    # file_list = ["mc_lock_enemy_6_False.png"]
    counter = 0
    for filename in os.listdir(Root_dir / output_dir):
        # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
        if filename.startswith("mc"):
            if filename not in file_list:
                continue
                # pass
            # print("________filename", filename)
            counter = counter + 1
            file_result[filename] = {}
            tar_img = imread_chinese(f"{output_dir}{filename}")
            res = my_LoadAllTemplate_instance.match_by_category_default(tar_img, category_want,
                                                                        allow_muti_each_return=False)

            file_result[filename] = res
    confing_dig[config_name] = file_result

    time_e = time.perf_counter()
    avg_time = (time_e - time_s) / counter if counter > 0 else 0.0
    confidence_all = 0
    for filename_item in file_result.keys():
        item = file_result[filename_item]
        sk1 = "1"
        sk2 = "2"
        sk3 = "3"
        confidence_all += item[sk1]["confidence"]
        confidence_all += item[sk2]["confidence"]
        confidence_all += item[sk3]["confidence"]


    print(f"=================config_name '{config_name}' all match done {counter}/{counter} average confidence ****:{(confidence_all/(len(file_result)*3)):.4f}**** time cost : {(time_e - time_s):.4f}, average time cost :{avg_time:.4f} ")

stats = my_LoadAllTemplate_instance.load_img_by_name.get_stats()
print("统计结果: load_img_by_name", stats)

stats = my_LoadAllTemplate_instance.match_template_by_name_default.get_stats()
print("统计结果: match_template_by_name_default", stats)

stats = my_LoadAllTemplate_instance.match_by_category_default.get_stats()
print("统计结果: match_by_category_default", stats)

stats = match_template_probability.get_stats()
print("统计结果 match_template_probability:", stats)
print(confing_dig)
print("over")

compare_config = ["all_char_head_icon_small_15.json","all_char_head_icon_small_15_grey.json"]
for filename in file_list:
        for i in range(1,4,1):
            index = str(i)
            if confing_dig[compare_config[0]][filename][index]["name"]!=confing_dig[compare_config[1]][filename][index]["name"]:
                print(f'error confing_dig[{compare_config}[0]][{filename}][{index}][\"name\"] {confing_dig[compare_config[0]][filename][index]["name"]}'
                      f' 与 confing_dig[{compare_config}[1]][{filename}][{index}][\"name\"] {confing_dig[compare_config[1]][filename][index]["name"]} 不相等' )


#                  all_char_head_icon_small_15_grey.json 速度更快 快了 54%
# =================config_name 'all_char_head_icon_small_15.json' all match done 10/10 average confidence ****:0.9097**** time cost : 5.2813, average time cost :0.5281
# =================config_name 'all_char_head_icon_small_15_grey.json' all match done 10/10 average confidence ****:0.9098**** time cost : 2.3903, average time cost :0.2390
# 统计结果: load_img_by_name {'calls': 4160, 'total_time': '0.02109', 'avg_time': '0.00001', 'max': '0.00014', 'p99': '0.00002', 'p90': '0.00001', 'p1': '0.00000'}
# 统计结果: match_template_by_name_default {'calls': 1040, 'total_time': '6.94666', 'avg_time': '0.00668', 'max': '0.02243', 'p99': '0.01490', 'p90': '0.00953', 'p1': '0.00329'}
# 统计结果: match_by_category_default {'calls': 20, 'total_time': '6.94890', 'avg_time': '0.34744', 'max': '0.50879', 'p99': '0.50879', 'p90': '0.50385', 'p1': '0.18982'}
# 统计结果 match_template_probability: {'calls': 3120, 'total_time': '6.90897', 'avg_time': '0.00221', 'max': '0.01572', 'p99': '0.00484', 'p90': '0.00320', 'p1': '0.00103'}
# {'all_char_head_icon_small_15.json': {'mc_鉴心_白芷_秧秧_1600_900.png': {'3': {'name': '秧秧', 'index': '3', 'confidence': 0.9199204444885254, 'scale': 0.8666666666666667, 'top_left': (12, 10), 'bottom_right': (41, 39)}, '2': {'name': '白芷', 'index': '2', 'confidence': 0.7939725518226624, 'scale': 0.7666666666666666, 'top_left': (13, 14), 'bottom_right': (38, 40)}, '1': {'name': '鉴心', 'index': '1', 'confidence': 0.9494925737380981, 'scale': 0.8333333333333333, 'top_left': (15, 11), 'bottom_right': (42, 39)}}, 'mc_露西_丽贝卡_尤诺1600_900.png': {'3': {'name': '尤诺', 'index': '3', 'confidence': 0.9633436799049377, 'scale': 0.7666666666666666, 'top_left': (14, 17), 'bottom_right': (39, 43)}, '2': {'name': '丽贝卡', 'index': '2', 'confidence': 0.9146143794059753, 'scale': 0.7999999999999999, 'top_left': (17, 17), 'bottom_right': (43, 44)}, '1': {'name': '露西', 'index': '1', 'confidence': 0.88431715965271, 'scale': 0.7666666666666666, 'top_left': (14, 14), 'bottom_right': (39, 40)}}, 'mc_夏空_奥古斯塔_卡提希娅_1600_900.png': {'2': {'name': '奥古斯塔', 'index': '2', 'confidence': 0.9768945574760437, 'scale': 0.7999999999999999, 'top_left': (11, 15), 'bottom_right': (37, 42)}, '3': {'name': '卡提希娅', 'index': '3', 'confidence': 0.9114348292350769, 'scale': 0.7999999999999999, 'top_left': (13, 17), 'bottom_right': (39, 44)}, '1': {'name': '夏空', 'index': '1', 'confidence': 0.9551702737808228, 'scale': 0.7666666666666666, 'top_left': (13, 15), 'bottom_right': (38, 41)}}, 'mc_今汐_吟霖_卡卡罗_1600_900.png': {'1': {'name': '今汐', 'index': '1', 'confidence': 0.9336733222007751, 'scale': 0.7666666666666666, 'top_left': (11, 14), 'bottom_right': (36, 40)}, '2': {'name': '吟霖', 'index': '2', 'confidence': 0.9344677329063416, 'scale': 0.7666666666666666, 'top_left': (13, 16), 'bottom_right': (38, 42)}, '3': {'name': '卡卡罗', 'index': '3', 'confidence': 0.8337895274162292, 'scale': 0.7999999999999999, 'top_left': (11, 13), 'bottom_right': (37, 40)}}, 'mc_釉瑚_丹瑾_炽霞_1600_900.png': {'1': {'name': '釉瑚', 'index': '1', 'confidence': 0.9282557368278503, 'scale': 0.7999999999999999, 'top_left': (11, 15), 'bottom_right': (37, 42)}, '2': {'name': '丹瑾', 'index': '2', 'confidence': 0.9251604080200195, 'scale': 0.7666666666666666, 'top_left': (12, 13), 'bottom_right': (37, 39)}, '3': {'name': '炽霞', 'index': '3', 'confidence': 0.9141511917114258, 'scale': 0.8666666666666667, 'top_left': (11, 13), 'bottom_right': (40, 42)}}, 'mc_维里奈_安可_漂泊者_1600_900.png': {'3': {'name': '漂泊者', 'index': '3', 'confidence': 0.9609496593475342, 'scale': 0.9, 'top_left': (13, 11), 'bottom_right': (43, 42)}, '1': {'name': '维里奈', 'index': '1', 'confidence': 0.8975548148155212, 'scale': 0.8333333333333333, 'top_left': (9, 15), 'bottom_right': (36, 43)}, '2': {'name': '安可', 'index': '2', 'confidence': 0.7907349467277527, 'scale': 0.7999999999999999, 'top_left': (17, 20), 'bottom_right': (51, 58)}}, 'mc_长离_守岸人_相里要_1600_900.png': {'2': {'name': '守岸人', 'index': '2', 'confidence': 0.9737808108329773, 'scale': 0.7999999999999999, 'top_left': (12, 16), 'bottom_right': (38, 43)}, '3': {'name': '相里要', 'index': '3', 'confidence': 0.8834818601608276, 'scale': 0.8333333333333333, 'top_left': (10, 15), 'bottom_right': (37, 43)}, '1': {'name': '长离', 'index': '1', 'confidence': 0.9328799247741699, 'scale': 0.7333333333333333, 'top_left': (9, 15), 'bottom_right': (33, 40)}}, 'mc_桃祈_灯灯_秋水_1600_900.png': {'2': {'name': '灯灯', 'index': '2', 'confidence': 0.9276681542396545, 'scale': 0.8666666666666667, 'top_left': (10, 13), 'bottom_right': (39, 42)}, '1': {'name': '桃祈', 'index': '1', 'confidence': 0.9397082328796387, 'scale': 0.7999999999999999, 'top_left': (11, 11), 'bottom_right': (37, 38)}, '3': {'name': '秋水', 'index': '3', 'confidence': 0.8319777846336365, 'scale': 0.7333333333333333, 'top_left': (7, 13), 'bottom_right': (31, 38)}}, 'mc_莫特斐_鉴心_白芷_1600_900.png': {'1': {'name': '莫特斐', 'index': '1', 'confidence': 0.9506139755249023, 'scale': 0.7999999999999999, 'top_left': (11, 12), 'bottom_right': (37, 39)}, '3': {'name': '白芷', 'index': '3', 'confidence': 0.7939789891242981, 'scale': 0.7666666666666666, 'top_left': (13, 14), 'bottom_right': (38, 40)}, '2': {'name': '鉴心', 'index': '2', 'confidence': 0.9494838118553162, 'scale': 0.8333333333333333, 'top_left': (15, 11), 'bottom_right': (42, 39)}}, 'mc_卜灵_渊武_散华_1600_900.png': {'3': {'name': '散华', 'index': '3', 'confidence': 0.8688721060752869, 'scale': 0.7999999999999999, 'top_left': (10, 12), 'bottom_right': (36, 39)}, '2': {'name': '渊武', 'index': '2', 'confidence': 0.9337881803512573, 'scale': 0.7999999999999999, 'top_left': (8, 13), 'bottom_right': (34, 40)}, '1': {'name': '卜灵', 'index': '1', 'confidence': 0.9180179834365845, 'scale': 0.7999999999999999, 'top_left': (14, 17), 'bottom_right': (40, 44)}}}, 'all_char_head_icon_small_15_grey.json': {'mc_鉴心_白芷_秧秧_1600_900.png': {'2': {'name': '白芷', 'index': '2', 'confidence': 0.7935954332351685, 'scale': 0.7666666666666666, 'top_left': (13, 14), 'bottom_right': (38, 40)}, '3': {'name': '秧秧', 'index': '3', 'confidence': 0.9219275712966919, 'scale': 0.8666666666666667, 'top_left': (12, 10), 'bottom_right': (41, 39)}, '1': {'name': '鉴心', 'index': '1', 'confidence': 0.9495983719825745, 'scale': 0.8333333333333333, 'top_left': (15, 11), 'bottom_right': (42, 39)}}, 'mc_露西_丽贝卡_尤诺1600_900.png': {'3': {'name': '尤诺', 'index': '3', 'confidence': 0.9660238027572632, 'scale': 0.7666666666666666, 'top_left': (14, 17), 'bottom_right': (39, 43)}, '2': {'name': '丽贝卡', 'index': '2', 'confidence': 0.9151996970176697, 'scale': 0.7999999999999999, 'top_left': (17, 17), 'bottom_right': (43, 44)}, '1': {'name': '露西', 'index': '1', 'confidence': 0.8814417123794556, 'scale': 0.7666666666666666, 'top_left': (14, 14), 'bottom_right': (39, 40)}}, 'mc_夏空_奥古斯塔_卡提希娅_1600_900.png': {'2': {'name': '奥古斯塔', 'index': '2', 'confidence': 0.9747942686080933, 'scale': 0.7999999999999999, 'top_left': (11, 15), 'bottom_right': (37, 42)}, '3': {'name': '卡提希娅', 'index': '3', 'confidence': 0.9112836718559265, 'scale': 0.7999999999999999, 'top_left': (13, 17), 'bottom_right': (39, 44)}, '1': {'name': '夏空', 'index': '1', 'confidence': 0.9569781422615051, 'scale': 0.7666666666666666, 'top_left': (13, 15), 'bottom_right': (38, 41)}}, 'mc_今汐_吟霖_卡卡罗_1600_900.png': {'1': {'name': '今汐', 'index': '1', 'confidence': 0.9352349638938904, 'scale': 0.7666666666666666, 'top_left': (11, 14), 'bottom_right': (36, 40)}, '2': {'name': '吟霖', 'index': '2', 'confidence': 0.937881588935852, 'scale': 0.7666666666666666, 'top_left': (13, 16), 'bottom_right': (38, 42)}, '3': {'name': '卡卡罗', 'index': '3', 'confidence': 0.8328953385353088, 'scale': 0.7999999999999999, 'top_left': (11, 13), 'bottom_right': (37, 40)}}, 'mc_釉瑚_丹瑾_炽霞_1600_900.png': {'2': {'name': '丹瑾', 'index': '2', 'confidence': 0.9213102459907532, 'scale': 0.7666666666666666, 'top_left': (12, 13), 'bottom_right': (37, 39)}, '3': {'name': '炽霞', 'index': '3', 'confidence': 0.9148572087287903, 'scale': 0.8666666666666667, 'top_left': (11, 13), 'bottom_right': (40, 42)}, '1': {'name': '釉瑚', 'index': '1', 'confidence': 0.926716685295105, 'scale': 0.7999999999999999, 'top_left': (11, 15), 'bottom_right': (37, 42)}}, 'mc_维里奈_安可_漂泊者_1600_900.png': {'3': {'name': '漂泊者', 'index': '3', 'confidence': 0.9610570073127747, 'scale': 0.9, 'top_left': (13, 11), 'bottom_right': (43, 42)}, '1': {'name': '维里奈', 'index': '1', 'confidence': 0.8871070742607117, 'scale': 0.8333333333333333, 'top_left': (9, 15), 'bottom_right': (36, 43)}, '2': {'name': '安可', 'index': '2', 'confidence': 0.7889890074729919, 'scale': 0.7999999999999999, 'top_left': (17, 20), 'bottom_right': (51, 58)}}, 'mc_长离_守岸人_相里要_1600_900.png': {'3': {'name': '相里要', 'index': '3', 'confidence': 0.8831851482391357, 'scale': 0.8333333333333333, 'top_left': (10, 15), 'bottom_right': (37, 43)}, '2': {'name': '守岸人', 'index': '2', 'confidence': 0.9745519161224365, 'scale': 0.7999999999999999, 'top_left': (12, 16), 'bottom_right': (38, 43)}, '1': {'name': '长离', 'index': '1', 'confidence': 0.9314616918563843, 'scale': 0.7333333333333333, 'top_left': (9, 15), 'bottom_right': (33, 40)}}, 'mc_桃祈_灯灯_秋水_1600_900.png': {'3': {'name': '秋水', 'index': '3', 'confidence': 0.8310934901237488, 'scale': 0.7333333333333333, 'top_left': (7, 13), 'bottom_right': (31, 38)}, '2': {'name': '灯灯', 'index': '2', 'confidence': 0.9288347959518433, 'scale': 0.8666666666666667, 'top_left': (10, 13), 'bottom_right': (39, 42)}, '1': {'name': '桃祈', 'index': '1', 'confidence': 0.9412885308265686, 'scale': 0.7999999999999999, 'top_left': (11, 11), 'bottom_right': (37, 38)}}, 'mc_莫特斐_鉴心_白芷_1600_900.png': {'1': {'name': '莫特斐', 'index': '1', 'confidence': 0.9525874257087708, 'scale': 0.7999999999999999, 'top_left': (11, 12), 'bottom_right': (37, 39)}, '3': {'name': '白芷', 'index': '3', 'confidence': 0.7936047315597534, 'scale': 0.7666666666666666, 'top_left': (13, 14), 'bottom_right': (38, 40)}, '2': {'name': '鉴心', 'index': '2', 'confidence': 0.9495868682861328, 'scale': 0.8333333333333333, 'top_left': (15, 11), 'bottom_right': (42, 39)}}, 'mc_卜灵_渊武_散华_1600_900.png': {'2': {'name': '渊武', 'index': '2', 'confidence': 0.9427086710929871, 'scale': 0.7999999999999999, 'top_left': (8, 13), 'bottom_right': (34, 40)}, '3': {'name': '散华', 'index': '3', 'confidence': 0.8697596192359924, 'scale': 0.7999999999999999, 'top_left': (10, 12), 'bottom_right': (36, 39)}, '1': {'name': '卜灵', 'index': '1', 'confidence': 0.9169997572898865, 'scale': 0.7999999999999999, 'top_left': (14, 17), 'bottom_right': (40, 44)}}}}
# over