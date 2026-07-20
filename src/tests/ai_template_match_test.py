# @Author  : liuha
# @Time    : 2026/7/18 00:35
# @File    : ai_template_match_test.py
import cv2
import numpy as np
from typing import Optional, Union, List
from src.utils.image_dealer import match_template_probability, concat_images_with_padding_new, template_match_target, \
    pad_image, resize_template_match_target

# def match_template_probability(
#         template: Union[str, np.ndarray],
#         target: Union[str, np.ndarray],
#         scales: Optional[List[float]] = None,
#         method=cv2.TM_CCOEFF_NORMED,
#         use_color: bool = False,
#         output_img: bool = False,
#         visualize_path: Optional[str] = None,
#         scale_min: float = 0.75,
#         scale_max: float = 1.0,
#         scale_step: int = 5,
#         min_score_thresh: float = 0.7,
#         name: str = ""
# ) -> dict:
#     """
#     Returns dict:
#       { 'score': float (0..1),
#         'scale': float,
#         'top_left': (x,y),
#         'bottom_right': (x,y),
#         'resized_template_shape': (h,w) }
#     """
#
#     # load images if paths given
#     def _load(img):
#         if isinstance(img, str):
#             im = cv2.imread(img, cv2.IMREAD_COLOR)
#             if im is None:
#                 raise FileNotFoundError(f"Can't read image: {img}")
#             return im
#         return img.copy()
#
#     tpl = _load(template)
#     tgt = _load(target)
#
#     # use grayscale by default (more robust for anime head shapes); allow color if requested
#     if use_color:
#         tpl_proc = tpl
#         tgt_proc = tgt
#     else:
#         tpl_proc = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
#         tgt_proc = cv2.cvtColor(tgt, cv2.COLOR_BGR2GRAY)
#
#     th, tw = tpl_proc.shape[:2]
#     H, W = tgt_proc.shape[:2]
#
#     if scales is None:
#         scales = list(np.linspace(scale_min, scale_max, scale_step))  # covers smaller->larger scales; includes ~2.0
#         # scales = [1]
#
#     best_score = -1.0
#     best_scale = None
#     best_loc = None
#     best_size = None
#
#     for s in scales:
#         # resize template
#         new_w = int(round(tw * s))
#         new_h = int(round(th * s))
#         if new_w < 3 or new_h < 3:
#             continue
#         if new_w > W or new_h > H:
#             continue
#         interp = cv2.INTER_LINEAR if s >= 1.0 else cv2.INTER_AREA
#         tpl_resized = cv2.resize(tpl_proc, (new_w, new_h), interpolation=interp)
#
#         # match
#         res = cv2.matchTemplate(tgt_proc, tpl_resized, method)
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#
#         if method in (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED):
#             score = 1.0 - min_val  # lower is better -> convert
#         else:
#             score = max_val  # higher is better
#
#         # clamp to [0,1]
#         score = float(np.clip(score, 0.0, 1.0))
#
#         if score > best_score:
#             best_score = score
#             best_scale = s
#             best_loc = max_loc if method not in (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED) else min_loc
#             best_size = (new_w, new_h)
#
#     if best_loc is None:
#         return {'score': 0.0, 'scale': None, 'top_left': None, 'bottom_right': None, 'resized_template_shape': None}
#
#     x, y = best_loc
#     w, h = best_size
#     top_left = (x, y)
#     bottom_right = (x + w, y + h)
#
#     # optional visualization
#     if output_img:
#         if visualize_path is not None:
#             if best_score > min_score_thresh:
#                 vis = tgt.copy()
#                 cv2.putText(vis, str(f"{best_score:0.4f} {name}"), (0, 15),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#                 cv2.rectangle(vis, top_left, bottom_right, (0, 255, 0), 2)
#                 imwrite_chinese(visualize_path + f"{best_score:0.4f}.png", vis)
#
#     return {
#         'score': float(best_score),
#         'scale': float(best_scale),
#         'top_left': top_left,
#         'bottom_right': bottom_right,
#         'resized_template_shape': (h, w)
#     }


from pathlib import Path
import os
import json
import time
import matplotlib.pyplot as plt
from src.utils.image_dealer import get_search_area, get_sub_image_from_image, template_match_target_new, \
    calculate_target_template_xy, IconPosition
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese

# 使用示例
if __name__ == "__main__":


    use_color_img = False
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
            if use_color_img:
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
                        res = match_template_probability(resized, target_img_sub, use_color=use_color_img,use_canny=use_canny_in,
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
    print(f"all match done {counter}/{counter} time cost : {(time_e - time_s):.4f}")
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
