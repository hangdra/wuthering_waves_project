from src.core.vision.window_capture import WindowCapture
import time

from src.core.vision.window_capture_fast import WindowCapture2
from src.core.vision.wgc import ZBLWindowGrabber
from src.utils.get_game_window_id import GetGameWindowId

# window_name = "鸣潮  "
window_name = None
game_window_instance = GetGameWindowId(window_name=window_name)

# 1. 创建捕获器（通过窗口标题）
time.perf_counter()
time_begin = time.perf_counter()
capturer = WindowCapture(game_window_instance)
time_capturer = time.perf_counter()
print(f"init window_capture cost time {time_capturer-time_begin:.4f}")
capturer2 = WindowCapture2(game_window_instance)
time_capturer2 = time.perf_counter()
print(f"init time_capturer2 cost time {time_capturer2-time_capturer:.4f}")
capturer3 = ZBLWindowGrabber(game_window_instance)
time_capturer3 = time.perf_counter()
print(f"init ZBLWindowGrabber cost time {time_capturer3-time_capturer2:.4f}")

# 2. 循环截取（例如每秒 10 次）
sleep_interval = 0.01
loop_count = 50

save_image_count_each = 2
save_image_dic = {}

#
# time_start = time.perf_counter()
# for i in range(loop_count):
#     img = capturer.capture_bitblt()  # 返回 PIL.Image
#     # 或 img_array = capturer.capture(as_array=True)  # 返回 numpy 数组'
#     # img.save(f"{output_dir}frame_{i:03d}.png")
#     time.sleep(sleep_interval)
#     if i <save_image_count_each:
#         save_image_dic["capture_bitblt_"+str(i)] = img
#
# time_end = time.perf_counter()
# time_cost = time_end - time_start - loop_count * sleep_interval
# avg_cost = time_cost / loop_count
# print(f"capture_bitblt cost_time {time_cost:.4f} 平均 {avg_cost:.4f}  1秒平均 {int(1/avg_cost)} 帧") #capture_bitblt cost_time 1.754  平均 0.003

#
#
# time_start = time.perf_counter()
# for i in range(loop_count):
#     img = capturer.capture_new()  # 返回 PIL.Image
#     # 或 img_array = capturer.capture(as_array=True)  # 返回 numpy 数组'
#     # img.save(f"{output_dir}frame_{i:03d}.png")
#     time.sleep(sleep_interval)
#     if i <save_image_count_each:
#         save_image_dic["capture_new_"+str(i)] = img
#
# time_end = time.perf_counter()
# time_cost = time_end - time_start - loop_count * sleep_interval
# avg_cost = time_cost / loop_count
# print("capture_new cost_time", str(time_cost)[:5]," 平均"," 平均", str(avg_cost)[:5]) #capture_new cost_time 8.335  平均  平均 0.016
#




time_start = time.perf_counter()
for i in range(loop_count):
    img = capturer.capture_fast_numpy()  # 返回 PIL.Image
    # 或 img_array = capturer.capture(as_array=True)  # 返回 numpy 数组'
    # img.save(f"{output_dir}frame_{i:03d}.png")
    time.sleep(sleep_interval)
    if i <save_image_count_each:
        save_image_dic["capture_fast_numpy"+str(i)] = img

time_end = time.perf_counter()
time_cost = time_end - time_start - loop_count * sleep_interval
avg_cost = time_cost / loop_count
print(f"capture_fast_numpy cost_time {time_cost:.4f} 平均 {avg_cost:.4f} 1秒平均 {int(1/avg_cost)} 帧") #capture_bitblt cost_time 1.754  平均 0.003
# 3. 释放资源（可选，析构时会自动释放）
capturer.close()


# 非常快 但需要前台
# time_start = time.perf_counter()
# for i in range(loop_count):
#     img = capturer2.capture()  # 返回 PIL.Image
#     # 或 img_array = capturer.capture(as_array=True)  # 返回 numpy 数组'
#     # img.save(f"{output_dir}frame_{i:03d}.png")
#     time.sleep(sleep_interval)
#     if i <save_image_count_each:
#         save_image_dic["capturer2 capture_bitblt"+str(i)] = img
#
# time_end = time.perf_counter()
# time_cost = time_end - time_start - loop_count * sleep_interval
# avg_cost = time_cost / loop_count
# print(f"capturer2 cost_time {time_cost:.4f} 平均 {avg_cost:.4f} 1秒平均 {int(1/avg_cost)} 帧") #capture_bitblt cost_time 1.754  平均 0.003
# capturer2.close()



time_start = time.perf_counter()
for i in range(loop_count):
    img = capturer3.get_frame()
    # 或 img_array = capturer.capture(as_array=True)  # 返回 numpy 数组'
    # img.save(f"{output_dir}frame_{i:03d}.png")
    time.sleep(sleep_interval)
    if i <save_image_count_each:
        save_image_dic["wgc"+str(i)] = img

time_end = time.perf_counter()
time_cost = time_end - time_start - loop_count * sleep_interval
avg_cost = time_cost / loop_count
print(f"wgc cost_time {time_cost:.4f} 平均 {avg_cost:.4f} 1秒平均 {int(1/avg_cost)} 帧") #capture_bitblt cost_time 1.754  平均 0.003
# 3. 释放资源（可选，析构时会自动释放）
capturer3.close()


import os
import cv2

def imwrite_chinese(path, img):
    """
    保存图像，支持中文路径
    :param path: 保存路径（可含中文）
    :param img: 图像数据 (numpy array)
    :return: True/False
    """
    try:
        # 1.提取目录并创建（如果不存在）
        dirname = os.path.dirname(path)
        if dirname:  # 如果路径包含目录部分
            os.makedirs(dirname, exist_ok=True)

        ext = os.path.splitext(path)[1]  # 获取扩展名
        if ext.lower() in ['.jpg', '.jpeg']:
            success, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 90])
        elif ext.lower() == '.png':
            success, encoded = cv2.imencode('.png', img)
        else:
            success, encoded = cv2.imencode(ext, img)
        if success:
            with open(path, 'wb') as f:
                f.write(encoded.tobytes())
            print(path, "写入成功")
            return True
        else:
            return False
    except Exception as e:
        print(f"保存失败: {e}")
        return False

from PIL import Image
output_dir = "tests/images/auto/"
for key in save_image_dic.keys():
    image = save_image_dic[key]
    if image is not None:
        if isinstance(image, Image.Image):
            image.save(f"{output_dir}frame_{key}.png")
        else:
            imwrite_chinese(f"{output_dir}frame_{key}.png",image)
    else:
        print(f"{key} image is None")