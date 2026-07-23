# @Author  : liuha
# @Time    : 2026/7/16 16:06
# @File    : load_all_template.py

import os
import json

from src.utils.image_dealer import get_tar_s_divided_tem_s, resize_template_match_target, match_template_probability, \
    get_position_group, get_process_method, get_sub_tar_img, mask_img_by_color, compute_element_fill_ratio
from src.utils.read_write_image_from_filesys import imread_chinese, imwrite_chinese
from src.assets.config.config_others_all import *
from src.utils.tools import *
from typing import Callable, Optional
from typing import List, Dict, Any
import cv2

# from image_dealer import *
project_root = get_root_dir(__file__)


class LoadAllTemplate:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # print("init LoadAllTemplate Class")
        self.lazy_init = init_set["lazy_init"]

        self.template_all_list = []
        # self.template_info_list = []
        self.head_icon_info = []
        self.char_use_grey_image = True
        self.img_dic_by_path = {}
        self.img_dic_by_name = {}

        self.all_template_one_from_root = "src/assets/config/image_info/new_image_template_info.json"
        self.lock_enemy_matcher = None
        # self.all_template_info_file_from_root = "src/assets/config/image_info/image_template_info.json"
        # self.all_char_icon_config_file_from_root = "src/assets/config/image_info/all_char_head_icon_small2.json"
        if not hasattr(self, 'initialized'):
            # self.load_all_head_icon()
            # self.load_all_template_icon()

            # self.init_data_finish = self.init_data()
            self.x_variance_factor_default = 2
            self.y_variance_factor_default = 2
            if not self.lazy_init:
                self.load_all_template()

    def load_all_template(self):
        config_file_abs_path = os.path.join(project_root, self.all_template_one_from_root)
        with open(config_file_abs_path, 'r', encoding='utf-8') as f:
            # template_list: List[Dict[str, Any]] = json.load(f)  # ← 局部变量，类型明确
            self.template_all_list = json.load(f)
        for item in self.template_all_list:
            if "load_image" in item and not item["load_image"]:
                continue
            cv_read_color = cv2.IMREAD_COLOR
            if "force_grey" in item:
                use_grey = item["force_grey"]
                if use_grey:
                    cv_read_color = cv2.IMREAD_GRAYSCALE
            all_template_data = self.__load_img(item["image_file_from_project_root"], flag=cv_read_color)
            for sub_item in self.template_all_list:
                sub_item["template_img_data"] = all_template_data[
                    sub_item["template_y"]:sub_item["template_y"] + sub_item["template_height"],
                    sub_item["template_x"]:sub_item["template_x"] + sub_item["template_width"]]

    def __get_template_all(self)->List[Dict[str, Any]]:
        if self.template_all_list is None:
            self.load_all_template()
        if self.template_all_list is None:
            self.template_all_list = []
        return self.template_all_list

    def __load_img(self, path, flag=cv2.IMREAD_COLOR):
        if path not in self.img_dic_by_path:
            self.img_dic_by_path[path] = imread_chinese(path,
                                                        flag=flag)
        return self.img_dic_by_path[path]

    @stats_decorator
    def __load_img_by_name(self, name, img_info, is_tem_img=True):
        # todo  配合 template_list 加载文件 需要 category + template_list["name"] 作为新索引
        if name in self.img_dic_by_name:
            return self.img_dic_by_name[name]
        else:
            img_process_method: Optional[Callable] = None
            if is_tem_img:
                tar_win_hw, template_this_in = img_info
                if tar_win_hw[1] != template_this_in["template_window_width"] or tar_win_hw[0] != template_this_in[
                    "template_window_height"]:
                    tar_s_divided_tem_s = get_tar_s_divided_tem_s(tar_win_hw[1], tar_win_hw[0],
                                                                  template_this_in["template_window_width"],
                                                                  template_this_in["template_window_height"])
                    tem_img = resize_template_match_target(template_this_in["template_img_data"], tar_s_divided_tem_s)
                else:
                    tem_img = template_this_in["template_img_data"]
                if "template_process_method" in template_this_in and template_this_in[
                    "template_process_method"] is not None:
                    img_process_method = get_process_method(template_this_in["template_process_method"])
                    # result_img = img_process_method(tem_img)  # type: ignore
                result_img = tem_img
                this_r_name = "tem_" + name
            else:
                tar_img, tem_tar_xy, template_this_in, return_v = img_info
                tem_hw = [template_this_in["template_height"], template_this_in["template_width"]]
                tem_window_hw = (template_this_in["template_window_height"], template_this_in["template_window_width"])
                position_group = get_position_group(template_this_in["icon_position_group"])
                x_variance_factor_in = template_this_in[
                    "x_variance_factor"] if "x_variance_factor" in template_this_in else self.x_variance_factor_default
                y_variance_factor_in = template_this_in[
                    "y_variance_factor"] if "y_variance_factor" in template_this_in else self.y_variance_factor_default
                img_result = get_sub_tar_img(tar_img, tem_hw, tem_tar_xy, tem_window_hw,
                                             position_group, x_variance_factor_in, y_variance_factor_in)
                if "target_process_method" in template_this_in and template_this_in[
                    "target_process_method"] is not None:
                    img_process_method = get_process_method(template_this_in["target_process_method"])
                    # result_img = img_process_method(img_result)  #
                result_img = img_result
                this_r_name = "tar_" + name
                if return_v is not None and return_v != "":
                    this_r_name = this_r_name + "_" + return_v

            if "mask_color" in template_this_in and template_this_in["mask_color"] is not None:
                musk_color_this = mask_colors[template_this_in["mask_color"]]
                result_img = mask_img_by_color(result_img, musk_color_this)
            if callable(img_process_method):
                result_img = img_process_method(result_img)  # type: ignore
            self.img_dic_by_name[this_r_name] = result_img

            return self.img_dic_by_name[this_r_name]

    @stats_decorator
    def match_template_by_name_default(self, tar_img, template_name):
        template_this:Dict[str, Any] = next((tem for tem in self.__get_template_all() if tem["name"] == template_name),{})
        # print("template_this:", template_this)
        target_search_type = template_this["target_search_type"]
        # print("target_search_type:", target_search_type)
        tem_img = self.__load_img_by_name(template_name, [tar_img.shape[:2], template_this])
        if target_search_type == "multiple_match":
            # print("___________ in multiple_match")
            target_char_dic = {}
            tem_search_area_list = template_this["template_area_list"]
            target_search_return = template_this["target_search_return"]
            if tem_search_area_list is not None:
                for search_area in tem_search_area_list:
                    search_index = str(search_area[target_search_return])
                    tar_info = [tar_img, (search_area["x"], search_area["y"]), template_this, search_index]
                    tar_search_data = self.__load_img_by_name(template_name, tar_info, is_tem_img=False)
                    if "force_grey" in template_this:
                        force_grey: bool  = template_this.get("force_grey", False)
                    else:
                        force_grey = False
                    if "use_canny" in template_this:
                        use_canny: bool  = template_this.get("use_canny", False)
                    else:
                        use_canny = False
                    res = match_template_probability(tar_search_data, tem_img, force_grey=force_grey,
                                                     use_canny=use_canny)
                    candidates = {"name": template_this["name"], target_search_return: search_index,
                                  "confidence": res['score'],
                                  "scale": res['scale'], "top_left": res['top_left'],
                                  "bottom_right": res['bottom_right']}
                    # print(f"in multiple_match {target_search_return} : {search_index} ,candidates:{candidates}")
                    if candidates["confidence"] > template_this["min_success_score"]:
                        # if (search_index not in target_char_dic) or (
                        #         candidates["confidence"] > target_char_dic[search_index]["confidence"]):
                        target_char_dic[search_index] = candidates
                        # print("target_char_dic.len", len(target_char_dic))
            return target_char_dic
        else:
            # print("___________ in single_match")
            tar_info = [tar_img, (template_this["template_window_target_x"], template_this["template_window_target_y"]),
                        template_this, None]
            tar_search_data = self.__load_img_by_name(template_name, tar_info, is_tem_img=False)
            res = match_template_probability(tar_search_data, tem_img)
            candidates = {"name": template_this["name"], "confidence": res['score'],
                          "scale": res['scale'], "top_left": res['top_left'],
                          "bottom_right": res['bottom_right']}
            return {template_name: candidates}

    @stats_decorator
    def match_by_category_default(self, tar_img, category, return_mex_one=False, allow_muti_each_return=False):
        target_char_dic = None
        for tem in self.__get_template_all():
            if tem["category"] == category:
                name_this = tem["name"]
                res = self.match_template_by_name_default(tar_img, name_this)
                # print("________res",res)
                if target_char_dic is None:
                    target_char_dic = {}
                    if allow_muti_each_return:
                        for retun_val in res.keys():
                            # print("res", res,"retun_val",retun_val,"res[retun_val]",res[retun_val])
                            candidates = res[retun_val]
                            target_char_dic[retun_val] = [candidates]
                    else:
                        target_char_dic = res
                else:
                    for retun_val in res.keys():
                        candidates = res[retun_val]
                        if allow_muti_each_return:
                            if retun_val in target_char_dic:
                                target_char_dic[retun_val].append(candidates)
                            else:
                                target_char_dic[retun_val] = [candidates]
                        elif (retun_val not in target_char_dic) or (
                                candidates["confidence"] > target_char_dic[retun_val]["confidence"]):
                            target_char_dic[retun_val] = candidates
        # print("target_char_dic", target_char_dic)
        if return_mex_one and not allow_muti_each_return:
            max_confidence_item = None
            for index in target_char_dic.keys():
                item = target_char_dic[index]
                if max_confidence_item is None:
                    max_confidence_item = item
                else:
                    # print("item", item)
                    if item["confidence"] > max_confidence_item["confidence"]:
                        max_confidence_item = item
            return max_confidence_item
        return target_char_dic

    # def get_ult_percentage(self, tar_img, ele_type):
    #     template_name = "ult_percentage"
    #     template_this = next((tem for tem in self.__get_template_all() if tem["name"] == template_name), None)
    #     if template_this is None:
    #         raise Exception(f"template {template_name} not found")

    def get_enery_percentage(self, tar_img, template_name, ele_type):
        if template_name not in ["con_percentage","ult_percentage"]:
            raise Exception(f"template_name error unsupported template_name {template_name} for method[get_enery_percentage]")
        # template_name = "con_percentage"
        template_this = next((tem for tem in self.__get_template_all() if tem["name"] == template_name), None)
        if template_this is None:
            raise Exception(f"template {template_name} not found")

        tar_w_h, tar_w_w = tar_img.shape[:2]
        tem_w_h, tem_w_w = template_this["template_window_height"], template_this["template_window_width"]
        tem_h, tem_w = template_this["template_height"], template_this["template_width"]
        tar_s_divided_tem = get_tar_s_divided_tem_s(tar_w_w, tar_w_h, tem_w_w, tem_w_h)
        tar_info = [tar_img,
                    (template_this["template_window_target_x"], template_this["template_window_target_y"]),
                    template_this, None]
        tar_search_data = self.__load_img_by_name(template_name, tar_info, is_tem_img=False)
        ele_color = mask_colors[ele_type]
        if template_name == "con_percentage":
            start_angle = 0
        else:
            start_angle = 90
        percentage = compute_element_fill_ratio(tar_search_data, ele_color, start_angle=start_angle,
                                                outer_radius=round(tem_w * tar_s_divided_tem / 2),
                                                inner_radius=round(tem_w * tar_s_divided_tem / 2 * 0.8),
                                                visualize=False)
        return percentage


my_LoadAllTemplate_instance = LoadAllTemplate()
