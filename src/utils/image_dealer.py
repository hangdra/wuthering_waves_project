# @Author  : liuha
# @Time    : 2026/7/16 17:05
# @File    : image_dealer.py

import cv2
import numpy as np
from src.utils.read_write_image_from_filesys import imwrite_chinese
from src.utils.tools import timer
from enum import Enum


class IconPosition(Enum):
    RIGHT_BOTTOM = "right_bottom"
    CENTER_BOTTOM = "center_bottom"
    RIGHT_TOP = "right_top"

class TemplateType(Enum):
    SINGLE_TARGET = "single_target"
    MULTIPLE_TARGET = "multiple_targets"

def get_position_group(group_name):
    if group_name == "center_bottom":
        position_group = IconPosition.CENTER_BOTTOM
    elif group_name == "right_bottom":
        position_group = IconPosition.RIGHT_BOTTOM
    elif group_name == "right_top":
        position_group = IconPosition.RIGHT_TOP
    else:
        raise Exception("Unknown position group", group_name)
    return position_group


def get_process_method(method_name):
    target_process_method_in = None
    if method_name is not None and method_name != "":
        if method_name == "get_rid_light_part_for_matching":
            target_process_method_in = get_rid_light_part_for_matching
        elif method_name == "get_rid_dark_part_for_matching":
            target_process_method_in = get_rid_dark_part_for_matching
        elif method_name == "get_grey_image":
            target_process_method_in = get_grey_image
    return target_process_method_in

def remove_part_of_img(img, remove_left_percentage=0.0, remove_bottom_percentage=0.0, remove_top_percentage=0.0,
                       remove_right_percentage=0.0):
    h, w = img.shape[:2]
    remove_left_percentage = max(0.0, min(1.0, remove_left_percentage))
    remove_bottom_percentage = max(0.0, min(1.0, remove_bottom_percentage))
    remove_top_percentage = max(0.0, min(1.0, remove_top_percentage))
    remove_right_percentage = max(0.0, min(1.0, remove_right_percentage))
    start_x = int(w * remove_left_percentage)
    end_x = int(w * (1 - remove_right_percentage))
    start_y = int(h * remove_top_percentage)
    end_y = int(h * (1 - remove_bottom_percentage))
    return img[start_y:end_y, start_x:end_x]


def pad_image(img, top, bottom, left, right, fill_color=(255, 255, 255, 0)):
    padded = cv2.copyMakeBorder(
        img,
        top, bottom,
        left, right,
        cv2.BORDER_CONSTANT,
        value=fill_color
    )
    return padded


def concat_images_with_padding_new(img1, img2, align='top', fill_color=(0, 0, 0, 255)):
    """
    水平拼接两张图像，若高度不同则按指定对齐方式上下补边（填充颜色）。
    自动统一通道数：取两者中最大的通道数，将低通道图像转换为对应格式。
    支持灰度(1通道)、BGR(3通道)、BGRA(4通道)。

    参数：
        img1, img2: 输入图像 (numpy array)
        align: 'top' / 'bottom' / 'center'，短图补齐时的对齐方式
        fill_color: 填充颜色，根据最终通道数决定长度：
                    - 1通道: 标量 (如 0 或 255)
                    - 3通道: (B,G,R) 或 (B,G,R)
                    - 4通道: (B,G,R,A)
                    若传入长度不匹配，会自动适配。
    返回：
        水平拼接后的图像
    """
    # ========== 1. 输入标准化 ==========
    # 确保是 uint8
    if img1.dtype != np.uint8:
        img1 = img1.astype(np.uint8)
    if img2.dtype != np.uint8:
        img2 = img2.astype(np.uint8)

    # 获取各图像的维度信息
    def get_dims(img):
        if len(img.shape) == 2:
            return img.shape[0], img.shape[1], 1  # 灰度
        else:
            return img.shape[0], img.shape[1], img.shape[2]

    h1, w1, c1 = get_dims(img1)
    h2, w2, c2 = get_dims(img2)

    # ========== 2. 确定目标通道数 ==========
    target_c = max(c1, c2)  # 取较大通道数

    # ========== 3. 将图像统一到 target_c 通道 ==========
    def convert_to_channels(img, target_c):
        h, w, c = get_dims(img)
        if c == target_c:
            return img
        if target_c == 1:
            # 目标为灰度：彩色转灰度
            if c == 3:
                return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            elif c == 4:
                # BGRA 转灰度：先转 BGR 再转灰度
                return cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGRA2BGR), cv2.COLOR_BGR2GRAY)
            else:
                return img  # 不可能
        elif target_c == 3:
            # 目标为 BGR
            if c == 1:
                return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif c == 4:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                return img
        elif target_c == 4:
            # 目标为 BGRA
            if c == 1:
                bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                return cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
            elif c == 3:
                return cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            else:
                return img
        else:
            raise ValueError(f"Unsupported channel count: {target_c}")

    img1 = convert_to_channels(img1, target_c)
    img2 = convert_to_channels(img2, target_c)

    # ========== 4. 适配 fill_color ==========
    # 将 fill_color 调整为 target_c 长度的元组
    if isinstance(fill_color, (int, float)):
        fill_color = (fill_color,) * target_c
    else:
        fill_color = tuple(fill_color)
        if len(fill_color) < target_c:
            # 若长度不足，则补充最后一个值（或默认255）
            fill_color = fill_color + (fill_color[-1],) * (target_c - len(fill_color))
        elif len(fill_color) > target_c:
            fill_color = fill_color[:target_c]
    fill_color = tuple(int(c) for c in fill_color)  # 保证整数

    # ========== 5. 补齐高度 ==========
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    target_h = max(h1, h2)

    def pad_to_height(img, target_h, align, color):
        h, w = img.shape[:2]
        if h >= target_h:
            return img
        if align == 'top':
            top, bottom = 0, target_h - h
        elif align == 'bottom':
            top, bottom = target_h - h, 0
        else:  # center
            top = (target_h - h) // 2
            bottom = target_h - h - top
        top, bottom = max(0, int(top)), max(0, int(bottom))
        return cv2.copyMakeBorder(img, top, bottom, 0, 0,
                                  cv2.BORDER_CONSTANT, value=color)

    padded1 = pad_to_height(img1, target_h, align, fill_color)
    padded2 = pad_to_height(img2, target_h, align, fill_color)

    # ========== 6. 水平拼接 ==========
    result = np.hstack([padded1, padded2])
    return np.ascontiguousarray(result)


def hconcat_pad(img1, img2, pad_color=0):
    """
    水平拼接两张图，高度不同时用 pad_color 填充对齐
    pad_color: 0 为黑边，255 为白边，(0,0,255) 为红边
    """
    # if img1.shape != 2 and img1.shape[-1] != 1:
    #     color_deep = img1.shape[-1]
    #     if color_deep == 3:
    #         pad_color = (0, 0, 0)
    #     else:
    #         pad_color = (255, 0, 0, 255)
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    target_h = max(h1, h2)

    # 为 img1 补上/下边
    delta_h1 = target_h - h1
    if delta_h1 > 0:
        img1 = cv2.copyMakeBorder(img1, 0, delta_h1, 0, 0, cv2.BORDER_CONSTANT, value=pad_color)
    # 为 img2 补上/下边
    delta_h2 = target_h - h2
    if delta_h2 > 0:
        img2 = cv2.copyMakeBorder(img2, 0, delta_h2, 0, 0, cv2.BORDER_CONSTANT, value=pad_color)

    print("here near return")
    return np.hstack((img1, img2))


def icon_width_factor(image_origin_width, image_origin_height):
    """
    计算目标分辨率下图标宽度(使用deepseek得到不同分辨率下图标的宽度，用于后续不同分辨率之间比较比例数值）
    """
    ratio = image_origin_width / image_origin_height
    if ratio >= 2.3:
        # 带鱼屏 2560×1080	2.37 (21:9) 3440×1440	2.39 (21:9) 5120×1440	3.55 （32:9）
        return image_origin_width / 32.2  # 32.2  # 最终技能图标宽度
    else:
        return image_origin_width / 24  # 最终技能图标宽度


def get_tar_s_divided_tem_s(tar_window_w, tar_window_h, tem_window_w, tem_window_h):
    """
    获取不同分辨率下图标比例
    :param tar_window_w: 目标图像宽度
    :param tar_window_h: 目标图像高度
    :param tem_window_w: 模板原始图像宽度
    :param tem_window_h: 模板原始图像高度
    :return:
    """
    if tem_window_w == tar_window_w and tem_window_h == tar_window_h:
        return 1
    else:
        tar_s_divided_tem_s_in = icon_width_factor(tar_window_w, tar_window_h) / icon_width_factor(tem_window_w,
                                                                                                   tem_window_h)
        return tar_s_divided_tem_s_in


def calculate_target_template_xy(tar_window_w, tar_window_h, tem_window_w, tem_window_h,
                                 tem_target_x, tem_target_y,
                                 template_position: IconPosition = IconPosition.CENTER_BOTTOM,
                                 tar_s_divided_tem_s_in=None):
    """
    tar_window_w:目标图像宽度
    tar_window_h:目标图像高度
    tem_window_w:模板原始图像宽度
    tem_window_h:模板原始图像高度
    tem_target_x:模板原始图像目标坐标x
    tem_target_y:模板原始图像目标坐标y
    计算模板图像坐标在目标图像中的坐标
    """
    if tar_s_divided_tem_s_in is None:
        tar_s_divided_tem_s_in = get_tar_s_divided_tem_s(tar_window_w, tar_window_h, tem_window_w, tem_window_h)
    if tar_s_divided_tem_s_in == 1:
        return tem_target_x, tem_target_y, tar_s_divided_tem_s_in
    else:
        if template_position == IconPosition.RIGHT_BOTTOM:
            target_x = tar_window_w - (tem_window_w - tem_target_x) * tar_s_divided_tem_s_in
            target_y = tar_window_h - (tem_window_h - tem_target_y) * tar_s_divided_tem_s_in
            # return int(target_x), int(target_y), tar_s_divided_tem_s_in
        elif template_position == IconPosition.CENTER_BOTTOM:
            target_x = tar_window_w / 2 + (tem_target_x - tem_window_w / 2) * tar_s_divided_tem_s_in
            target_y = tar_window_h / 2 + (tem_target_y - tem_window_h / 2) * tar_s_divided_tem_s_in
            # return int(target_x), int(target_y), tar_s_divided_tem_s_in
        elif template_position == IconPosition.RIGHT_TOP:
            target_x = tar_window_w - (tem_window_w - tem_target_x) * tar_s_divided_tem_s_in
            target_y = tem_target_y * tar_s_divided_tem_s_in
        else:
            raise Exception("cal_c not supported template_position: {}".format(template_position))
        return int(target_x), int(target_y), tar_s_divided_tem_s_in


def resize_template_match_target(template_image, tar_s_divided_tem_s):
    if tar_s_divided_tem_s != 1:
        resized_template_image = cv2.resize(template_image, None, fx=tar_s_divided_tem_s, fy=tar_s_divided_tem_s)
        return resized_template_image
    else:
        return template_image


#
# def calculate_target_x_y(tar_window_w, tar_window_h, template_image, tem_window_w, tem_window_h, tem_target_x, tem_target_y,
#                          position_group: IconPosition = IconPosition.CENTER_BOTTOM):
#     target_x, target_y, tar_s_divided_tem_s = cal_c(tar_window_w, tar_window_h, tem_window_w,
#                                                     tem_window_h,
#                                                     tem_target_x,
#                                                     tem_target_y, position_group)
#
#
#     return target_x, target_y


def get_rid_light_part_for_matching(image, threshold=210):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    # 创建一个与原始图像大小相同的纯色图像(亮部要替换成的颜色)
    color_img = np.full_like(gray_image, 0, dtype=np.uint8)
    result_pic = np.where(mask == 255, color_img, gray_image)
    return result_pic


def get_rid_dark_part_for_matching(image, threshold=120):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    # 创建一个与原始图像大小相同的纯色图像(亮部要替换成的颜色)
    color_img = np.full_like(gray_image, 0, dtype=np.uint8)
    result_pic = np.where(mask != 255, color_img, gray_image)
    # cv2.imshow("", result_pic)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return result_pic


def get_grey_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def get_search_area(tar_x, tar_y, tar_w_w, tar_w_h, tem_w, tem_h, tar_s_divided_tem_s_in=1, w_variance=3, h_variance=2):
    print(f"tar_x : {tar_x} , tar_y : {tar_y}, tar_w_w : {tar_w_w}, tar_w_h : {tar_w_h}, tem_w : {tem_w}, tem_h : {tem_h}")
    tem_w_in_tar = tem_w * tar_s_divided_tem_s_in
    tem_h_in_tar = tem_h * tar_s_divided_tem_s_in

    center_tar_x = tar_x + tem_w_in_tar / 2
    center_tar_y = tar_y + tem_h_in_tar / 2

    roi_x_fix = int(center_tar_x - w_variance / 2 * tem_w_in_tar)
    roi_y_fix = int(center_tar_y - h_variance / 2 * tem_h_in_tar)
    roi_w_fix = int(w_variance * tem_w_in_tar)
    roi_h_fix = int(h_variance * tem_h_in_tar)
    # roi_x_fix = int(x - (w_variance / 2 - 0.5) * tem_w * tar_s_divided_tem_s_in)
    # roi_y_fix = int(y - (h_variance / 2 - 0.5) * tem_h * tar_s_divided_tem_s_in)
    # roi_w_fix = int(w_variance * tem_w * tar_s_divided_tem_s_in)
    # roi_h_fix = int(h_variance * tem_h * tar_s_divided_tem_s_in)
    # # print(" step1 roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix ", roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
    # 确保不越界

    roi_x_fix = max(0, min(roi_x_fix, tar_w_w - 1))
    roi_y_fix = max(0, min(roi_y_fix, tar_w_h - 1))
    roi_w_fix = min(roi_w_fix, tar_w_w - roi_x_fix)
    roi_h_fix = min(roi_h_fix, tar_w_h - roi_y_fix)
    return roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix


def get_search_are_by_default(tar_w_w, tar_w_h, tem_w_w, tem_w_h, tem_x, tem_y, tem_w, tem_h, position_group,
                              w_variance=3,
                              h_variance=2, tar_s_divided_tem_s=None):
    target_x, target_y, tar_s_divided_tem_s = calculate_target_template_xy(tar_w_w,
                                                                           tar_w_h,
                                                                           tem_w_w,
                                                                           tem_w_h,
                                                                           tem_x, tem_y, position_group,
                                                                           tar_s_divided_tem_s_in=tar_s_divided_tem_s)
    return get_search_area(target_x, target_y, tar_w_w, tar_w_h, tem_w, tem_h, tar_s_divided_tem_s, w_variance,
                           h_variance)


def get_sub_image_from_image(image, x, y, w, h):
    sub_image = image[y:y + h, x:x + w]
    return sub_image


from typing import Optional, Union, List


@timer
def match_template_probability(
        template: Union[str, np.ndarray],
        target: Union[str, np.ndarray],
        scales: Optional[List[float]] = None,
        method=cv2.TM_CCOEFF_NORMED,
        use_color: bool = False,
        use_canny: bool = False,          # 新增
        canny_thresh1: int = 30,          # 新增，Canny低阈值
        canny_thresh2: int = 90,         # 新增，Canny高阈值
        output_img: bool = False,
        visualize_path: Optional[str] = None,
        scale_min: float = 0.7,
        scale_max: float = 1.0,
        scale_step: int = 10,
        min_score_thresh: float = 0.7,
        name: str = ""
) -> dict:
    """
    Returns dict:
      { 'score': float (0..1),
        'scale': float,
        'top_left': (x,y),
        'bottom_right': (x,y),
        'resized_template_shape': (h,w) }
    """

    # load images if paths given

    def _load(img):
        if isinstance(img, str):
            im = cv2.imread(img, cv2.IMREAD_COLOR)
            if im is None:
                raise FileNotFoundError(f"Can't read image: {img}")
            return im
        return img.copy()

    tpl = _load(template)
    tgt = _load(target)

    # use grayscale by default (more robust for anime head shapes); allow color if requested
    if use_color:
        tpl_proc = tpl
        tgt_proc = tgt
    else:
        # 转为灰度
        tpl_proc = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY) if len(tpl.shape) == 3 else tpl
        tgt_proc = cv2.cvtColor(tgt, cv2.COLOR_BGR2GRAY) if len(tgt.shape) == 3 else tgt


    # --- 新增 Canny 边缘提取 ---
    if use_canny:
        # 对灰度图提取边缘（边缘图仍然是单通道 uint8，边缘为255，其余为0）
        tpl_proc = cv2.Canny(tpl_proc, canny_thresh1, canny_thresh2)
        tgt_proc = cv2.Canny(tgt_proc, canny_thresh1, canny_thresh2)
        # 可选：对边缘图做轻微膨胀，使边缘变粗，增加匹配稳定性（视情况决定）
        # kernel = np.ones((2,2), np.uint8)
        # tpl_proc = cv2.dilate(tpl_proc, kernel, iterations=1)
        # tgt_proc = cv2.dilate(tgt_proc, kernel, iterations=1)

    th, tw = tpl_proc.shape[:2]
    H, W = tgt_proc.shape[:2]
    if scales is None:
        scales = list(np.linspace(scale_min, scale_max, scale_step))  # covers smaller->larger scales; includes ~2.0
        # scales = [1]

    best_score = -1.0
    best_scale = None
    best_loc = None
    best_size = None

    for s in scales:
        # resize template
        new_w = int(round(tw * s))
        new_h = int(round(th * s))
        if new_w < 3 or new_h < 3:
            continue
        if new_w > W or new_h > H:
            continue
        interp = cv2.INTER_LINEAR if s >= 1.0 else cv2.INTER_AREA
        tpl_resized = cv2.resize(tpl_proc, (new_w, new_h), interpolation=interp)

        # match
        res = cv2.matchTemplate(tgt_proc, tpl_resized, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method == cv2.TM_SQDIFF_NORMED:
            score = 1.0 - min_val  # 归一化平方差，直接转换
            loc = min_loc
        elif method == cv2.TM_SQDIFF:
            # 未归一化平方差：值越小越好，映射到 (0,1] 且越大越好
            print("_______________________TM_SQDIFF__min_val",min_val)
            score = 1.0 / (1.0 + min_val)
            loc = min_loc
        else:
            # TM_CCOEFF_NORMED, TM_CCORR_NORMED 等
            score = max_val
            loc = max_loc

        # clamp to [0,1]
        score = float(np.clip(score, 0.0, 1.0))

        if score > best_score:
            best_score = score
            best_scale = s
            best_loc = loc
            best_size = (new_w, new_h)

    if best_loc is None:
        return {'score': 0.0, 'scale': None, 'top_left': None, 'bottom_right': None, 'resized_template_shape': None}

    x, y = best_loc
    w, h = best_size
    top_left = (x, y)
    bottom_right = (x + w, y + h)

    # optional visualization
    if output_img:
        if visualize_path is not None:
            if best_score > min_score_thresh:
                vis = tgt.copy()
                cv2.putText(vis, str(f"{best_score:0.4f} {name}"), (0, 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.rectangle(vis, top_left, bottom_right, (0, 255, 0), 2)
                imwrite_chinese(visualize_path + f"{best_score:0.4f}.png", vis)

    return {
        'score': float(best_score),
        'scale': float(best_scale),
        'top_left': top_left,
        'bottom_right': bottom_right,
        'resized_template_shape': (h, w)
    }


def template_match_target_new(tar_img, tem_img, target_process_method=None, template_process_method=None):
    if target_process_method is not None:
        tar_img = target_process_method(tar_img)

    if template_process_method is not None:
        tem_image = template_process_method(tem_img)

    result = cv2.matchTemplate(tar_img, tem_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    search_local_x, search_local_y = max_loc
    # target_match_x = roi_x_fix + search_local_x
    # target_match_y = roi_y_fix + search_local_y

    return max_val, search_local_x, search_local_y

def template_match_target(tar_img, tem_img, target_process_method=None, template_process_method=None):
    if target_process_method is not None:
        tar_img = target_process_method(tar_img)

    if template_process_method is not None:
        tem_img = template_process_method(tem_img)

    print("tar_img.shape", tar_img.shape)
    print("tem_img.shape", tem_img.shape)
    result = cv2.matchTemplate(tar_img, tem_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    search_local_x, search_local_y = max_loc
    return max_val,(search_local_x, search_local_y)



def compute_element_fill_ratio(
        img,
        color_ranges,  # 例如: {'h': [130, 160], 's': [50, 255], 'v': [50, 255]}
        start_angle=0, #
        thickness_ratio=0.2,  # 环宽 = 外半径 * thickness_ratio (当仅有一个圆时)
        outer_radius=None,  # 手动指定外圆半径（若提供则跳过霍夫检测）
        inner_radius=None,  # 手动指定内圆半径（优先级最高）
        center=None,  # 手动指定圆心 (x, y)，若None则取图像中心
        angle_step=3.6,  # 角度采样步长（度），越小越精确
        visualize=False
):
    """
    计算圆环中元素颜色像素的比例（支持只检测到内圆的情况）。

    参数：
        img                 : 图像 (BGR格式)
        color_ranges        : 字典，包含hsv三个通道的范围，例如 {'h':(130,160), 's':(50,255), 'v':(50,255)}
        start_angle         : 初始查询角度水平为0度 查协奏，如果是大招 从90度开始
        thickness_ratio     : 当自动检测仅得到一个圆时，环宽度 = 外半径 * thickness_ratio
        outer_radius        : 手动指定外圆半径（像素），若None则自动检测
        inner_radius        : 手动指定内圆半径（若指定则忽略其他半径推算）
        center              : 手动指定圆心 (x, y)，若不指定则自动取图像中心（用于手动指定半径时）
        visualize           : 是否显示调试窗口
    返回：
        ratio (0~1)
    """
    if img is None:
        raise ValueError("图片为空")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # 满足范围条件的像素被置为 255（白色），不满足的置为 0（黑色）。
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ele_mask = cv2.inRange(img_hsv, (color_ranges['h'][0], color_ranges['s'][0], color_ranges['v'][0]),
                           (color_ranges['h'][1], color_ranges['s'][1], color_ranges['v'][1]))


    # ----- 1. 确定内外圆半径 -----
    if outer_radius is None and inner_radius is None:
        # 自动检测圆
        # edges = cv2.Canny(gray, 50, 150)

        circles = cv2.HoughCircles(
            ele_mask, cv2.HOUGH_GRADIENT, dp=1, minDist=2,
            param1=150, param2=45,
            minRadius=int(min(h, w) * 0.05),  # 放宽最小半径，以防漏检小圆
            maxRadius=int(min(h, w) * 0.95)
        )

        if circles is None:
            raise RuntimeError("未检测到任何圆，请手动指定半径或调整霍夫参数")

        circles = np.uint16(np.around(circles[0]))
        circles = sorted(circles, key=lambda x: x[2], reverse=True)  # 按半径降序

        # 如果只有一个圆，判断它是内圆还是外圆
        if len(circles) == 1:
            x, y, r = circles[0]
            # 假设图像中心为圆心，半径小于图像最短边的一半则视为内圆
            img_center = (w // 2, h // 2)
            # dist_center = np.hypot(x - img_center[0], y - img_center[1])
            # 若检测到的圆偏小，且圆心接近图像中心，则视作内圆
            # if r < min(h, w) * 0.4 and dist_center < min(h, w) * 0.2:
            print("img_center",img_center,"inner_r",r)
            if r < min(h, w) * 0.4 :
                inner_r = r
                outer_r = int(inner_r / (1 - thickness_ratio))  # 根据厚度反推外半径
                print("仅检测到一个圆，将其作为内圆，并估算外圆")
            else:
                outer_r = r
                inner_r = int(outer_r * (1 - thickness_ratio))
                print("仅检测到一个圆，将其作为外圆，并估算内圆")
            center = (x, y)  # 使用检测到的圆心
        else:
            # 有多个圆，取最大作为外圆，第二大为内圆
            outer_x, outer_y, outer_r = circles[0]
            _, _, inner_r = circles[1]
            center = (outer_x, outer_y)
            print("检测到多个圆，取最大为外圆，次大为内圆")
    else:
        # 手动指定半径
        if center is None:
            center = (w // 2, h // 2)
        if outer_radius is not None and inner_radius is None:
            outer_r = outer_radius
            inner_r = int(outer_r * (1 - thickness_ratio))
        elif inner_radius is not None and outer_radius is None:
            inner_r = inner_radius
            outer_r = int(inner_r / (1 - thickness_ratio))
        else:
            outer_r = outer_radius
            inner_r = inner_radius
        # 若两者都指定，直接使用

    # 安全保护：内外半径合法
    if inner_r >= outer_r:
        outer_r = inner_r + 4
    print(f"外半径: {outer_r}, 内半径: {inner_r}, 圆心: {center}")

    # ----- 2. 生成环状掩膜 -----
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, outer_r, 255, -1)
    cv2.circle(mask, center, inner_r, 0, -1)


    # if circles is not None and len(circles) > 0:




    ele_mask_after = cv2.bitwise_and(ele_mask, mask)  # 更简洁，避免np.where
    # cv2.imshow("ele_mask", ele_mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # ----- 3. 角度扫描计算填充比例（新核心逻辑）-----
    circle_deg = 360
    num_steps = int(circle_deg / angle_step)
    angles_deg = np.linspace(start_angle + 0.1, start_angle + circle_deg, num_steps, endpoint=True)  # 不包含360°
    angles_rad = np.deg2rad(angles_deg)

    # 预分配填充标记
    filled = np.zeros(num_steps, dtype=bool)

    # 采样半径步长（像素）
    radius_step = 0.8  # 可调，兼顾精度与速度
    # print("inner_r",inner_r,"outer_r",outer_r) #1600 900 inner_r 19 outer_r 22
    for i, theta in enumerate(angles_rad):
        cos_a = np.cos(theta)
        sin_a = -np.sin(theta)  # 图像y轴向下，取负实现逆时针

        # 沿射线从内到外扫描，发现紫色即标记该角度已填充
        ray_has_ele_color = False
        # 略微收缩内外边界，避免边缘噪声影响（可选）
        for r in np.arange(inner_r + 0.1, outer_r - 0.1, radius_step):
            px = int(center[0] + r * cos_a)
            py = int(center[1] + r * sin_a)
            if 0 <= px < w and 0 <= py < h and ele_mask_after[py, px] == 255:
                ray_has_ele_color = True
                break
        filled[i] = ray_has_ele_color
    print(filled[:10])
    print("np.sum(filled)", np.sum(filled))

    # 寻找第一个未填充的角度
    first_empty = None
    for i, val in enumerate(filled):
        if not val:
            first_empty = i
            break
    print("first_empty", first_empty)

    if first_empty is None:
        ratio = 1.0
        max_angle = 360.0
    else:
        ratio = first_empty / num_steps
        max_angle = angles_deg[first_empty]

    print("ratio",ratio)
    # ----- 4. 可视化（增强显示角度终点）-----
    if visualize:
        vis = img.copy()
        cv2.circle(vis, center, outer_r, (0, 255, 0), 1)
        cv2.circle(vis, center, inner_r, (0, 0, 255), 1)

        print(f"{center}___________{start_angle}___________x+{outer_r*np.cos(start_angle)},y-{outer_r * np.sin(start_angle)}")
        # 绘制起始方向（绿色箭头，3点钟方向）
        start_rad = np.deg2rad(start_angle)
        start_x = int(center[0] + outer_r * np.cos(start_rad))
        start_y = int(center[1] - outer_r * np.sin(start_rad))
        cv2.line(vis, center, (start_x, start_y), (0, 255, 0), 3)

        # 绘制终止方向（红色箭头）
        end_rad = np.deg2rad(max_angle)
        end_x = int(center[0] + outer_r * np.cos(end_rad))
        end_y = int(center[1] - outer_r * np.sin(end_rad))  # 注意取负
        cv2.line(vis, center, (end_x, end_y), (0, 0, 255), 3)

        # 叠加半透明区域（方便视觉确认）
        purple_overlay = np.zeros_like(vis)
        purple_overlay[ele_mask_after > 0] = (0, 0, 255)
        vis = cv2.addWeighted(vis, 0.6, purple_overlay, 0.4, 0)

        fi1 = ele_mask#concat_images_with_padding_new(edges,mask)
        fi2 = concat_images_with_padding_new(fi1, mask)
        fi3 = concat_images_with_padding_new(fi2, ele_mask_after)
        result = cv2.bitwise_and(img, img, mask=ele_mask_after)
        fi4 = concat_images_with_padding_new(fi3, result)
        fi5 = concat_images_with_padding_new(fi4, vis)

        cv2.imshow("Angle Scan Result", fi5)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return ratio



def draw_lines(image, global_xy, max_val, template_width_a, template_height_a, name, min_score=0.65,
               search_area_xywh=None,
               search_area_color=(255, 90, 50), find_color=(0, 0, 255), text_color=(0, 255, 0),
               grey_img_text_color=(0, 0, 0), save_image=False,
               output_dir=None, show_image=False, template_image=None):
    template_name = name.split("[")[1].split("]")[0]
    valid = max_val > min_score
    if "origin" in name:
        # 画出searcharea 并标注项目
        cv2.rectangle(image, (search_area_xywh[0], search_area_xywh[1]),
                      (search_area_xywh[0] + search_area_xywh[2], search_area_xywh[1] + search_area_xywh[3]),
                      search_area_color, 2)
        cv2.putText(image, f"{template_name} ", (search_area_xywh[0], search_area_xywh[1] + search_area_xywh[3] + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
    if "origin" in name:
        # 画出匹配信心
        cv2.putText(image, f"{max_val:.2f} {valid}", (search_area_xywh[0], search_area_xywh[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, find_color, 2, cv2.LINE_AA)
    else:
        if template_image is not None:
            if image.shape == 2:
                image = hconcat_pad(image, template_image)
            else:
                image = concat_images_with_padding_new(image, template_image)
        cv2.putText(image, f"{max_val:.2f} {valid}", (search_area_xywh[0], search_area_xywh[1] + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, grey_img_text_color, 1, cv2.LINE_AA)
    if max_val >= min_score:
        cv2.rectangle(image, (global_xy[0], global_xy[1]),
                      (global_xy[0] + template_width_a, global_xy[1] + template_height_a),
                      find_color, 2)
    if save_image:
        imwrite_chinese(
            output_dir + name + "_confidence_" + str(
                max_val)[:4] + "_" + str(valid) + ".png", image)
    if show_image:
        cv2.imshow(name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return image
