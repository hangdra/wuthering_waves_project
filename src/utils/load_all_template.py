# @Author  : liuha
# @Time    : 2026/7/16 16:06
# @File    : load_all_template.py

import os
import json

from src.utils.image_dealer import get_rid_light_part_for_matching, \
    get_rid_dark_part_for_matching, get_grey_image, template_match_target, \
    IconPosition, get_tar_s_divided_tem_s, resize_template_match_target, calculate_target_template_xy, draw_lines, \
    get_sub_image_from_image, get_search_area, template_match_target_new, match_template_probability, \
    get_search_are_by_default, compute_element_fill_ratio,get_position_group,get_process_method
from src.utils.read_write_image_from_filesys import imread_chinese, imwrite_chinese
from src.assets.config.config_others_all import *
from src.utils.tools import *

import cv2
from pathlib import Path

# from image_dealer import *
project_root = get_root_dir(__file__)


#


def con_percentage(tar_img, char_element):
    """当前角色 协奏百分比 """
    position_group = get_position_group(con_info["position_group"])
    tar_window_h, tar_window_w = tar_img.shape[:2]
    tem_window_w, tem_window_h = con_info["tem_window_w"], con_info["tem_window_h"]
    tem_target_x, tem_target_y = con_info["tem_target_x"], con_info["tem_target_y"]
    tem_w = con_info["tem_w"]
    tem_h = con_info["tem_h"]
    roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_are_by_default(tar_window_w, tar_window_h, tem_window_w,
                                                                           tem_window_h, tem_target_x, tem_target_y,
                                                                           tem_w, tem_h, position_group,
                                                                           w_variance=1.2,
                                                                           h_variance=1.2)
    target_img_sub = get_sub_image_from_image(tar_img, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
    ele_color = con_colors[char_element]
    percentage = compute_element_fill_ratio(target_img_sub, ele_color, visualize=False)
    return percentage


class LoadAllTemplate:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # print("init LoadAllTemplate Class")
        self.template_all_list = None
        # self.template_info_list = []
        self.head_icon_info = []
        self.char_use_grey_image = True
        self.img_dic = {}
        self.all_template_one_from_root = "src/assets/config/image_info/new_image_template_info.json"
        # self.all_template_info_file_from_root = "src/assets/config/image_info/image_template_info.json"
        # self.all_char_icon_config_file_from_root = "src/assets/config/image_info/all_char_head_icon_small2.json"
        if not hasattr(self, 'initialized'):
            # self.load_all_head_icon()
            # self.load_all_template_icon()

            # self.init_data_finish = self.init_data()
            self.load_all_template()
            self.x_variance_factor_default = 2
            self.y_variance_factor_default = 2

    def load_all_template(self):
        config_file_abs_path = os.path.join(project_root, self.all_template_one_from_root)
        with open(config_file_abs_path, 'r', encoding='utf-8') as f:
            self.template_all_list = json.load(f)
        for item in self.template_all_list:
            all_template_data = self.load_img(item["image_file_from_project_root"],
                                              flag=cv2.IMREAD_GRAYSCALE)
            item["template_img_data"] = all_template_data[
                item["template_y"]:item["template_y"] + item["template_height"],
                item["template_x"]:item["template_x"] + item["template_width"]]
            if item["category"] == "all_char_head_icon":
                self.head_icon_info.append(item)


    # def load_all_template_icon(self):
    #     config_file_abs_path = os.path.join(project_root, self.all_template_info_file_from_root)
    #     with open(config_file_abs_path, 'r', encoding='utf-8') as f:
    #         self.template_info_list = json.load(f)
    #     for item in self.template_info_list:
    #         all_template_data = self.load_img(item["image_file_from_project_root"],
    #                                           flag=cv2.IMREAD_GRAYSCALE)
    #         item["template_img_data"] = all_template_data[
    #             item["template_y"]:item["template_y"] + item["template_height"],
    #             item["template_x"]:item["template_x"] + item["template_width"]]
    #
    # def load_all_head_icon(self):
    #     for item in self.template_all_list:
    #         if item["category"] == "all_char_head_icon"



    def load_img(self, path, flag=cv2.IMREAD_COLOR):
        if path not in self.img_dic:
            self.img_dic[path] = imread_chinese(path,
                                                flag=flag)
        return self.img_dic[path]

    def get_match_char_template_head_icon(self, target_img, find_and_return_once=False):
        tar_window_height, tar_window_width = target_img.shape[:2]
        target_char_dic = {}
        for i in range(len(self.head_icon_info)):
            item = self.head_icon_info[i]
            if find_and_return_once:
                if len(target_char_dic) == 3:
                    break
            tar_s_divided_tem_s = get_tar_s_divided_tem_s(tar_window_width, tar_window_height,
                                                          item["template_window_width"], item["template_window_height"])
            resize_template_img = resize_template_match_target(item["template_img_data"], tar_s_divided_tem_s)

            position_group = get_position_group(item["icon_position_group"])

            target_process_method_in = None
            if "target_process_method" in item and item["target_process_method"] is not None:
                target_process_method_in = get_process_method(item["target_process_method"])
            # todo 模板图片直接灰度处理 不要进入程序再处理 done _grey.png

            template_process_method = None
            if "template_process_method" in item and item["template_process_method"] is not None:
                template_process_method = get_process_method(item["template_process_method"])

                # else:
                #     raise ValueError("Unknown process_method", item["template_process_method"])
            tem_search_area_list = item["template_area_list"]
            if tem_search_area_list is not None:
                for search_area in tem_search_area_list:
                    search_index = str(search_area["index"])
                    if find_and_return_once:
                        if search_index in target_char_dic:
                            continue
                    tem_x, tem_y = search_area["x"], search_area["y"]
                    target_x, target_y, tar_s_divided_tem_s = calculate_target_template_xy(tar_window_width,
                                                                                           tar_window_height,
                                                                                           item[
                                                                                               "template_window_width"],
                                                                                           item[
                                                                                               "template_window_height"],
                                                                                           tem_x, tem_y, position_group,
                                                                                           tar_s_divided_tem_s_in=tar_s_divided_tem_s)
                    x_variance_factor = item[
                        "x_variance_factor"] if "x_variance_factor" in item else self.x_variance_factor_default
                    y_variance_factor = item[
                        "y_variance_factor"] if "y_variance_factor" in item else self.y_variance_factor_default
                    roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_area(target_x, target_y,
                                                                                 tar_window_width,
                                                                                 tar_window_height,
                                                                                 item["template_width"],
                                                                                 item["template_height"],
                                                                                 tar_s_divided_tem_s,
                                                                                 x_variance_factor, y_variance_factor)
                    target_img_sub = get_sub_image_from_image(target_img, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
                    if template_process_method is not None:
                        resize_template_img = template_process_method(resize_template_img)
                    if target_process_method_in is not None:
                        target_img_sub = target_process_method_in(target_img_sub)
                    # print(item["name"],search_index,"resize_template_img.shape",resize_template_img.shape,"target_img_sub.shape",target_img_sub.shape)
                    res = match_template_probability(resize_template_img, target_img_sub, use_color=False)

                    candidates = {"name": item["name"], "index": search_index, "confidence": res['score'],
                                  "scale": res['scale'], "top_left": res['top_left'],
                                  "bottom_right": res['bottom_right']}
                    if candidates["confidence"] > item["min_success_score"]:
                        if (search_index not in target_char_dic) or (
                                candidates["confidence"] > target_char_dic[search_index]["confidence"]):
                            target_char_dic[search_index] = candidates

                    # max_val = res["score"]
                    # # max_val,search_local_x, search_local_y = template_match_target_new(target_img_sub,resize_template_img,target_process_method=target_process_method_in,
                    # #     template_process_method=template_process_method)
                    # # print(item["name"]," index",search_index,"confidence",max_val)
                    # if max_val > item["min_success_score"]:
                    #     candidates = {"name": item["name"], "confidence": max_val}
                    #     if str(search_index) not in target_char_dic:
                    #         target_char_dic[str(search_index)] = candidates
                    #     else:
                    #         old_confidence = target_char_dic[str(search_index)]["confidence"]
                    #         if old_confidence < max_val:
                    #             target_char_dic[str(search_index)] = candidates
                    # max_val = candidates["confidence"]
                    # if max_val >  item["min_success_score"]:
                    #     # print(item)
                    #     search_local_x, search_local_y = res["top_left"][0],res["top_left"][1]
                    #
                    #     # print("tar_window_height, tar_window_width", tar_window_height, tar_window_width )
                    #     # print("target_x, target_y", target_x, target_y)
                    #     base_name = "match_[" + item["name_pinyin"] + "]"
                    #
                    #     output_file_name = base_name + "_grey"
                    #     save_image = False
                    #     show_image = False
                    #     template_height_a, template_width_a = resize_template_img.shape[:2]
                    #     print("resize_template_img.shape", resize_template_img.shape,"target_img_sub.shape", target_img_sub.shape)
                    #     image_with_draw = draw_lines(target_img_sub.copy(), (search_local_x, search_local_y), max_val,
                    #                                  template_width_a,
                    #                                  template_height_a, search_area_xywh=[0, 0, 0, 0],
                    #                                  name=output_file_name, min_score=item["min_success_score"],
                    #                                  save_image=save_image,
                    #                                  output_dir="", show_image=show_image,template_image = resize_template_img)
                    #
                    #     output_file_name = base_name + "_origin"
                    #     save_image = False
                    #     show_image = True
                    #     image_with_draw = draw_lines(target_img.copy(), (roi_x_fix + search_local_x,roi_y_fix + search_local_y), max_val, template_width_a,
                    #                                  template_height_a, search_area_xywh=(roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix),
                    #                                  name=output_file_name, min_score=item["min_success_score"],
                    #                                  save_image=save_image,
                    #                                  output_dir="", show_image=show_image)
        return target_char_dic

    def match_template_by_name_new(self, target_img, template_name):
        tar_window_height, tar_window_width = target_img.shape[:2]
        found_template = False
        template_info = None
        for item in self.template_all_list:
            if item["name"] == template_name:
                found_template = True
                template_info = item
                break

        if not found_template:
            raise Exception("template not found", template_name)
        else:
            position_group = get_position_group(template_info["icon_position_group"])
            # 先让模板缩放与目标图像的搜寻目标大小匹配
            tar_s_divided_tem_s = get_tar_s_divided_tem_s(tar_window_width, tar_window_height,
                                                          template_info["template_window_width"],
                                                          template_info["template_window_height"])
            resize_template_img = resize_template_match_target(template_info["template_img_data"], tar_s_divided_tem_s)
            target_x, target_y, tar_s_divided_tem_s_in = calculate_target_template_xy(tar_window_width,
                                                                                      tar_window_height,
                                                                                      template_info[
                                                                                          "template_window_width"],
                                                                                      template_info[
                                                                                          "template_window_height"],
                                                                                      template_info[
                                                                                          "template_window_target_x"],
                                                                                      template_info[
                                                                                          "template_window_target_y"],
                                                                                      position_group,
                                                                                      tar_s_divided_tem_s)

            target_process_method_in = None
            if "target_process_method" in template_info and template_info["target_process_method"] is not None:
                target_process_method_in = get_process_method(template_info["target_process_method"])
            # todo 模板图片直接灰度处理 不要进入程序再处理 done _grey.png

            template_process_method = None
            if "template_process_method" in template_info and template_info["template_process_method"] is not None:
                template_process_method = get_process_method(template_info["template_process_method"])

            x_variance_factor = template_info[
                "x_variance_factor"] if "x_variance_factor" in template_info else self.x_variance_factor_default
            y_variance_factor = template_info[
                "y_variance_factor"] if "y_variance_factor" in template_info else self.y_variance_factor_default
            roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_area(target_x, target_y,
                                                                         tar_window_width,
                                                                         tar_window_height,
                                                                         template_info["template_width"],
                                                                         template_info["template_height"],
                                                                         tar_s_divided_tem_s,
                                                                         x_variance_factor, y_variance_factor)
            # print("_______________roi_x_fix: ", roi_x_fix, "roi_y_fix: ", roi_y_fix, "roi_w_fix: ", roi_w_fix, "roi_h_fix: ", roi_h_fix)
            target_img_sub = get_sub_image_from_image(target_img, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
            if template_process_method is not None:
                resize_template_img = template_process_method(resize_template_img)
            if target_process_method_in is not None:
                target_img_sub = target_process_method_in(target_img_sub)

            res = template_match_target(target_img_sub,resize_template_img)
            max_val = res[0]

            if max_val > 0.5:
                search_local_x, search_local_y = res[1]
                # print(item)
                # search_local_x, search_local_y = res["top_left"][0],res["top_left"][1]

                # print("tar_window_height, tar_window_width", tar_window_height, tar_window_width )
                # print("target_x, target_y", target_x, target_y)
                base_name = "match_[" + template_info["name"] + "]"

                output_file_name = base_name + "_grey"
                save_image = False
                show_image = True
                template_height_a, template_width_a = resize_template_img.shape[:2]
                print("resize_template_img.shape", resize_template_img.shape, "target_img_sub.shape",
                      target_img_sub.shape)
                image_with_draw = draw_lines(target_img_sub.copy(), (search_local_x, search_local_y), max_val,
                                             template_width_a,
                                             template_height_a, search_area_xywh=[0, 0, 0, 0],
                                             name=output_file_name, min_score=template_info["min_success_score"],
                                             save_image=save_image,
                                             output_dir="", show_image=show_image, template_image=resize_template_img)

                output_file_name = base_name + "_origin"
                save_image = False
                show_image = False
                image_with_draw = draw_lines(target_img.copy(),
                                             (roi_x_fix + search_local_x, roi_y_fix + search_local_y), max_val,
                                             template_width_a,
                                             template_height_a,
                                             search_area_xywh=(roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix),
                                             name=output_file_name, min_score=template_info["min_success_score"],
                                             save_image=save_image,
                                             output_dir="", show_image=show_image)

            return max_val > template_info["min_success_score"], max_val

    def has_template_by_name(self, tar_img, template_name):
        has_template, max_val = self.match_template_by_name_new(tar_img, template_name)
        return has_template, max_val


my_LoadAllTemplate_instance = LoadAllTemplate()
