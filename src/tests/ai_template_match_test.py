# @Author  : liuha
# @Time    : 2026/7/18 00:35
# @File    : ai_template_match_test.py
import cv2
import numpy as np
from typing import Optional, Union, List
from src.utils.image_dealer import match_template_probability, concat_images_with_padding_new, \
    pad_image, resize_template_match_target



from pathlib import Path
import os
import json
import time
import matplotlib.pyplot as plt
from src.utils.image_dealer import get_search_area, get_sub_image_from_image, \
    calculate_target_template_xy, IconPosition
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese

# 使用示例
if __name__ == "__main__":


    force_grey = False
    project_root = Path(__file__).parent.parent.parent
    all_template_info_file_name = "src/assets/config/image_info/all_char_head_icon_small3.json"
    image_abs_path = os.path.join(project_root, all_template_info_file_name)
    with open(image_abs_path, 'r', encoding='utf-8') as f:
        head_icon_info = json.load(f)

    output_dir = "src/tests/images/auto/chars/"
    file_result = {}
    tar_sub_img = {}
    time_s = time.perf_counter()
    counter = 0

    for filename in os.listdir(project_root / output_dir):
        # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
        if filename.startswith("mc"):
            if filename!="mc1920_1080.png":
                # continue
                pass
            counter = counter + 1
            file_result[filename] = {}
            find_char = []
            print(f"{output_dir}{filename}")
            tar_img = imread_chinese(f"{output_dir}{filename}")
            find_count = 0
            print(tar_img.shape)
            tar_window_height, tar_window_width = tar_img.shape[:2]
            # tar_s_divided_tem_s = 1
            if not force_grey:
                print(head_icon_info[0]["image_file_from_project_root"])
                all_head_icon_data = imread_chinese(head_icon_info[0]["image_file_from_project_root"])
            else:
                print(head_icon_info[0]["image_grey_file_from_project_root"])
                all_head_icon_data = imread_chinese(head_icon_info[0]["image_grey_file_from_project_root"])
            position_group = IconPosition.RIGHT_TOP
            old_method_dic = {}
            for i in range(len(head_icon_info)):
                item = head_icon_info[i]
                item["template_img_data"] = all_head_icon_data[
                    item["template_y"]:item["template_y"] + item["template_height"],
                    item["template_x"]:item["template_x"] + item["template_width"]]
                tem_search_area_list = item["template_area_list"]
                if tem_search_area_list is not None:
                    for search_area in tem_search_area_list:
                        search_index = search_area["index"]
                        tem_tar_x, tem_tar_y = search_area["x"], search_area["y"]
                        target_x, target_y, tar_s_divided_tem_s = calculate_target_template_xy(tar_window_width,
                                                                                               tar_window_height,
                                                                                               item["template_window_width"],
                                                                                               item["template_window_height"],
                                                                                               tem_tar_x, tem_tar_y,
                                                                                               position_group)
                        #
                        # target_x, target_y = calculate_target_template_xy(tar_s_divided_tem_s, tar_window_width,
                        #                                                   tar_window_height,
                        #                                                   item["template_window_width"],
                        #                                                   item["template_window_height"],
                        #                                                   tem_x, tem_y, position_group)
                        #
                        roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_area(target_x, target_y,
                                                                                     tar_window_width,
                                                                                     tar_window_height,
                                                                                     item["template_width"],
                                                                                     item["template_height"],
                                                                                     tar_s_divided_tem_s, 1.5,1.5)
                        target_img_sub = get_sub_image_from_image(tar_img, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
                        tar_sub_img[filename + str(search_index)] = target_img_sub
                        scales = [1.0]
                        # if item["template_img_data"].shape[1] == 0:
                        #     del item["template_img_data"]
                        #     print("all_head_icon_data.shape",all_head_icon_data.shape)
                        #     print(item)
                        #     exit()
                        print('item["template_img_data"].shape',item["template_img_data"].shape, 'target_img_sub.shape',target_img_sub.shape)
                        # exit()
                        if tar_s_divided_tem_s != 1.0:
                            resized = cv2.resize(item["template_img_data"], None, fx=tar_s_divided_tem_s, fy=tar_s_divided_tem_s)
                        else:
                            resized = item["template_img_data"]


                        template = resized
                        print(filename, item["name"])
                        print("index", search_index,"resized.shape", resized.shape,"target_img_sub.shape", target_img_sub.shape)
                        use_canny_in = True
                        res = match_template_probability(target_img_sub,resized, force_grey=force_grey,use_canny=use_canny_in,
                                                         visualize_path="src/tests/images/auto/matches/" +
                                                                        filename.split("_")[0] + "_" + str(
                                                             search_index) + "_" + item["name"],method=cv2.TM_CCOEFF_NORMED )
                        cv_method = "TM_CCOEFF_NORMED"+str(use_canny_in)
                        # res2 = template_match_target(target_img_sub,resized)
                        # print("____________________________________________res2", res2[0])
                        print("匹配分数:", res['score'])
                        print("缩放比例:", res['scale'])
                        print("位置:", res['top_left'], res['bottom_right'])
                        candidates = {"name": item["name"], "index": str(search_index), "confidence": res['score'],#"confidence2": res2[0],
                                      "scale": res['scale'], "top_left": res['top_left'],
                                      "bottom_right": res['bottom_right']}
                        if (str(search_index) not in file_result[filename]) or (
                                candidates["confidence"] > file_result[filename][str(search_index)]["confidence"]):
                            file_result[filename][str(search_index)] = candidates

                        # 测试匹配效果
                        # if filename == "mc风_1600_900.png" and (
                        #         item["name"] == "安可" ):
                        #     # 绘制匹配结果
                        #     img_out = concat_images_with_padding_new(target_img_sub, resized).copy()
                        #     top_left, bottom_right = res['top_left'], res['bottom_right']
                        #     cv2.rectangle(img_out, top_left, bottom_right, (0, 255, 0), 2)
                        #     cv2.putText(img_out, str(f"{candidates["confidence"]:0.4f} {candidates["name"]}"),
                        #                 (0, 15),
                        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        #     cv2.imshow(item["name_pinyin"], img_out)
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
        "src/tests/images/auto/matches/all_matches"+cv_method+".png", padding_image)
