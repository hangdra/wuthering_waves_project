# @Author  : liuha
# @Time    : 2026/7/18 13:37
# @File    : test_cordinate_transform.py
from src.assets.config.config_others_all import con_colors_hsv
from src.utils.image_dealer import *

tar_window_w, tar_window_h = 3440, 1440
tem_window_w, tem_window_h = 1600, 900
tem_target_x, tem_target_y = 600, 813
tem_w = 45
tem_h = 45
# tar_s_divided_tem_s_in = get_tar_s_divided_tem_s(tar_window_w, tar_window_h, tem_window_w, tem_window_h)
template_position = IconPosition.CENTER_BOTTOM
res = calculate_target_template_xy(tar_window_w, tar_window_h, tem_window_w, tem_window_h,
                                   tem_target_x, tem_target_y,
                                   template_position)

white_color = {  # 用于检测UI元素可用状态的白色颜色范围。
    'r': (253, 255),  # Red range
    'g': (253, 255),  # Green range
    'b': (253, 255)  # Blue range
}

con_colors = {  # 不同角色属性的协奏值能量环的颜色范围列表。
    "spectro": {
        'r': (205, 235),
        'g': (190, 222),  # for yellow spectro
        'b': (90, 130)
    },
    "electric": {
        'r': (150, 190),  # Red range
        'g': (95, 140),  # Green range for purple electric
        'b': (210, 249)  # Blue range
    },
    "fire": {
        'r': (200, 230),  # Red range
        'g': (100, 130),  # Green range    for red fire
        'b': (75, 105)  # Blue range
    },
    "ice": {
        'r': (60, 95),  # Red range
        'g': (150, 180),  # Green range    for blue ice
        'b': (210, 245)  # Blue range
    },
    "wind": {
        'r': (70, 110),  # Red range
        'g': (215, 250),  # Green range    for green wind
        'b': (155, 190)  # Blue range
    },
    "havoc": {
        'r': (190, 220),  # Red range
        'g': (65, 105),  # Green range    for havoc
        'b': (145, 175)  # Blue range
    }
}


def calculate_color_percentage(image, color_ranges):
    print("color_ranges", color_ranges)
    mask = cv2.inRange(image, (color_ranges['b'][0], color_ranges['g'][0], color_ranges['r'][0]),
                       (color_ranges['b'][1], color_ranges['g'][1], color_ranges['r'][1]))
    target_pixels = cv2.countNonZero(mask)
    total_pixels = image.size / 3
    percentage = target_pixels / total_pixels
    return percentage


import cv2
import numpy as np
import cv2
import numpy as np

# def compute_element_fill_ratio(
#     img,
#     color_ranges,          # 例如: {'h': [130, 160], 's': [50, 255], 'v': [50, 255]}
#     thickness_ratio=0.15,       # 环宽 = 外半径 * thickness_ratio (当仅有一个圆时)
#     outer_radius=None,         # 手动指定外圆半径（若提供则跳过霍夫检测）
#     inner_radius=None,         # 手动指定内圆半径（优先级最高）
#     center=None,               # 手动指定圆心 (x, y)，若None则取图像中心
#     angle_step=0.5,        # 角度采样步长（度），越小越精确
#     visualize=False
# ):
#     """
#     计算圆环中紫色像素的比例（支持只检测到内圆的情况）。
#
#     参数：
#         img                 : 图像 (BGR格式)
#         color_ranges_bgr    : 字典，包含bgr三个通道的范围，例如 {'b':(130,160), 'g':(50,255), 'r':(50,255)}
#         thickness_ratio     : 当自动检测仅得到一个圆时，环宽度 = 外半径 * thickness_ratio
#         outer_radius        : 手动指定外圆半径（像素），若None则自动检测
#         inner_radius        : 手动指定内圆半径（若指定则忽略其他半径推算）
#         center              : 手动指定圆心 (x, y)，若不指定则自动取图像中心（用于手动指定半径时）
#         visualize           : 是否显示调试窗口
#     返回：
#         ratio (0~1)
#     """
#     if img is None:
#         raise ValueError("图片为空")
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     h, w = gray.shape
#
#     # ----- 1. 确定内外圆半径 -----
#     if outer_radius is None and inner_radius is None:
#         # 自动检测圆
#         edges = cv2.Canny(gray, 50, 150)
#         # cv2.imshow("edges", edges)
#         # cv2.waitKey(0)
#         # cv2.destroyAllWindows()
#         circles = cv2.HoughCircles(
#             edges, cv2.HOUGH_GRADIENT, dp=1, minDist=5,
#             param1=150, param2=40,
#             minRadius=int(min(h, w) * 0.05),   # 放宽最小半径，以防漏检小圆
#             maxRadius=int(min(h, w) * 0.95)
#         )
#         if circles is None:
#             raise RuntimeError("未检测到任何圆，请手动指定半径或调整霍夫参数")
#
#         circles = np.uint16(np.around(circles[0]))
#         circles = sorted(circles, key=lambda x: x[2], reverse=True)  # 按半径降序
#
#         # 如果只有一个圆，判断它是内圆还是外圆
#         if len(circles) == 1:
#             x, y, r = circles[0]
#             # 假设图像中心为圆心，半径小于图像最短边的一半则视为内圆
#             img_center = (w//2, h//2)
#             dist_center = np.hypot(x - img_center[0], y - img_center[1])
#             # 若检测到的圆偏小，且圆心接近图像中心，则视作内圆
#             if r < min(h, w) * 0.4 and dist_center < min(h, w) * 0.2:
#                 inner_r = r
#                 outer_r = int(inner_r / (1 - thickness_ratio))   # 根据厚度反推外半径
#                 print("仅检测到一个圆，将其作为内圆，并估算外圆")
#             else:
#                 outer_r = r
#                 inner_r = int(outer_r * (1 - thickness_ratio))
#                 print("仅检测到一个圆，将其作为外圆，并估算内圆")
#             center = (x, y)  # 使用检测到的圆心
#         else:
#             # 有多个圆，取最大作为外圆，第二大为内圆
#             outer_x, outer_y, outer_r = circles[0]
#             _, _, inner_r = circles[1]
#             center = (outer_x, outer_y)
#             print("检测到多个圆，取最大为外圆，次大为内圆")
#     else:
#         # 手动指定半径
#         if center is None:
#             center = (w//2, h//2)
#         if outer_radius is not None and inner_radius is None:
#             outer_r = outer_radius
#             inner_r = int(outer_r * (1 - thickness_ratio))
#         elif inner_radius is not None and outer_radius is None:
#             inner_r = inner_radius
#             outer_r = int(inner_r / (1 - thickness_ratio))
#         else:
#             outer_r = outer_radius
#             inner_r = inner_radius
#         # 若两者都指定，直接使用
#
#     # 安全保护：内外半径合法
#     if inner_r >= outer_r:
#         outer_r = inner_r + 4
#     print(f"外半径: {outer_r}, 内半径: {inner_r}, 圆心: {center}")
#
#     # ----- 2. 生成环状掩膜 -----
#     mask = np.zeros((h, w), dtype=np.uint8)
#     cv2.circle(mask, center, outer_r, 255, -1)
#     cv2.circle(mask, center, inner_r, 0, -1)
#
#     #满足范围条件的像素被置为 255（白色），不满足的置为 0（黑色）。
#     ele_mask = cv2.inRange(img, (color_ranges['b'][0], color_ranges['g'][0], color_ranges['r'][0]),
#                        (color_ranges['b'][1], color_ranges['g'][1], color_ranges['r'][1]))
#     # "electric": {
#     #     'h': (133, 151),  # Red range
#     #     's': (76, 255),  # Green range for purple electric
#     #     'v': (80, 255)  # Blue range
#     # }
#
#     # ----- 3. 角度扫描计算填充比例（新核心逻辑）-----
#     circle_deg = 360
#     num_steps = int(circle_deg / angle_step)
#     angles_deg = np.linspace(0.5, 360.5, num_steps, endpoint=False)  # 不包含360°
#     angles_rad = np.deg2rad(angles_deg)
#
#     # 预分配填充标记
#     filled = np.zeros(num_steps, dtype=bool)
#
#     # 采样半径步长（像素）
#     radius_step = 1.0  # 可调，兼顾精度与速度
#     # print("inner_r",inner_r,"outer_r",outer_r) #1600 900 inner_r 19 outer_r 22
#     for i, theta in enumerate(angles_rad):
#         cos_a = np.cos(theta)
#         sin_a = -np.sin(theta)  # 图像y轴向下，取负实现逆时针
#
#         # 沿射线从内到外扫描，发现紫色即标记该角度已填充
#         ray_has_ele_color = False
#         # 略微收缩内外边界，避免边缘噪声影响（可选）
#         for r in np.arange(inner_r + 0.5, outer_r - 0.5, radius_step):
#             px = int(center[0] + r * cos_a)
#             py = int(center[1] + r * sin_a)
#             if 0 <= px < w and 0 <= py < h and ele_mask[py, px] == 255:
#                 ray_has_ele_color = True
#                 break
#         filled[i] = ray_has_ele_color
#     print(filled[:10])
#     print("np.sum(filled)",np.sum(filled))
#
#     # 寻找第一个未填充的角度
#     first_empty = None
#     for i, val in enumerate(filled):
#         if not val:
#             first_empty = i
#             break
#     print("first_empty",first_empty)
#
#     if first_empty is None:
#         ratio = 1.0
#         max_angle = 360.0
#     else:
#         ratio = first_empty / num_steps
#         max_angle = angles_deg[first_empty]
#
#         # ----- 4. 可视化（增强显示角度终点）-----
#         if visualize:
#             vis = img.copy()
#             cv2.circle(vis, center, outer_r, (0, 255, 0), 1)
#             cv2.circle(vis, center, inner_r, (0, 0, 255), 1)
#
#             # 绘制起始方向（绿色箭头，3点钟方向）
#             start_x = int(center[0] + outer_r * 1.0)
#             start_y = int(center[1])
#             cv2.line(vis, center, (start_x, start_y), (0, 255, 0), 3)
#
#             # 绘制终止方向（红色箭头）
#             end_rad = np.deg2rad(max_angle)
#             end_x = int(center[0] + outer_r * np.cos(end_rad))
#             end_y = int(center[1] - outer_r * np.sin(end_rad))  # 注意取负
#             cv2.line(vis, center, (end_x, end_y), (0, 0, 255), 3)
#
#             # 叠加紫色半透明区域（方便视觉确认）
#             purple_overlay = np.zeros_like(vis)
#             purple_overlay[ele_mask > 0] = (255, 0, 255)
#             vis = cv2.addWeighted(vis, 0.6, purple_overlay, 0.4, 0)
#
#             cv2.imshow("Angle Scan Result", vis)
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()
#
#     return ratio


# # 使用示例
# if __name__ == "__main__":
#     ratio = get_purple_fill_ratio("circle_image.png")
#     print(f"紫色填充比例: {ratio:.3f}")

from pathlib import Path
import os
from src.utils.read_write_image_from_filesys import imwrite_chinese, imread_chinese
import math

project_root = Path(__file__).parent.parent.parent
output_dir = "src/tests/images/template/"
file_result = {}
tar_sub_img = {}
for filename in os.listdir(project_root / output_dir):
    # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
    if filename != "露西满E_4k.png":
        pass
        # continue
    file_result[filename] = {}
    find_char = []
    print(f"{output_dir}{filename}")
    tar_img = imread_chinese(f"{output_dir}{filename}")
    tar_window_h, tar_window_w = tar_img.shape[:2]
    tem_window_w, tem_window_h = 1600, 900
    tem_target_x, tem_target_y = 600, 813
    tem_w = 45
    tem_h = 45
    position_group = IconPosition.CENTER_BOTTOM
    print("tar_window_w:", tar_window_w, "tar_window_h:", tar_window_h, "tem_window_w:", tem_window_w, "tem_window_h:",
          tem_window_h, "tem_target_x:", tem_target_x, "tem_target_y:", tem_target_y, "tem_w:", tem_w, "tem_h:", tem_h)
    roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_are_by_default(tar_window_w, tar_window_h, tem_window_w,
                                                                           tem_window_h, tem_target_x, tem_target_y,
                                                                           tem_w, tem_h, position_group,
                                                                           w_variance=1.4,
                                                                           h_variance=1.4)
    target_img_sub = get_sub_image_from_image(tar_img, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)
    tar_s_divided_tem_s = get_tar_s_divided_tem_s(tar_window_w, tar_window_h,
                                                  tem_window_w, tem_window_h)
    print("tar_s_divided_tem_s", tar_s_divided_tem_s)

    print("target_img_sub.shape", target_img_sub.shape)
    for ele in con_colors.keys():
        print(ele)
        ele_color = con_colors_hsv[ele]
        percentage = compute_element_fill_ratio(target_img_sub, ele_color,
                                                outer_radius=round(tem_w * tar_s_divided_tem_s / 2),
                                                inner_radius=round(tem_w * tar_s_divided_tem_s / 2 * 0.8),
                                                visualize=False)
        # percentage = calculate_color_percentage(target_img_sub,ele_color)
        file_result[filename][ele] = percentage
        print(f"{output_dir}{filename}")
        print(f"{ele} :{percentage * 100:.4f}%")
        # exit()
        # cv2.imshow(ele+str(percentage), target_img_sub)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

print(file_result)
