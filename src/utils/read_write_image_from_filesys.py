# @Author  : liuha
# @Time    : 2026/7/16 16:15
# @File    : read_write_image_from_filesys.py
import time
import os
import cv2
import numpy as np
from pathlib import Path
from src.utils.tools import timer

project_root = Path(__file__).parent.parent.parent



# @timer
def imread_chinese(image_path, flag=cv2.IMREAD_COLOR):
    """
    读取可能包含中文路径的图片
    :param image_path: 图片路径
    :param flag: 读取方式，同 cv2.imread 的 flags
    :return: OpenCV 图像 (numpy array)，失败返回 None
    """
    image_abs_path = os.path.join(project_root, image_path)
    try:
        if not os.path.exists(image_abs_path):
            print("文件不存在")
            return None
        else:
            # 1. 以二进制模式读取文件内容到内存
            with open(image_abs_path, 'rb') as f:
                image_data = f.read()
            # 2. 将字节数据转为numpy数组，再用imdecode解码为图像
            # 使用 np.frombuffer 将字节流转换为 numpy 数组[reference:10]
            image = cv2.imdecode(np.frombuffer(image_data, np.uint8), flag)
            return image
    except Exception as e:
        print(f"读取图片失败: {e}")
        return None


@timer
def imwrite_chinese(path, img):
    """
    保存图像，支持中文路径
    :param path: 保存路径（可含中文）
    :param img: 图像数据 (numpy array)
    :return: True/False
    """
    try:
        image_abs_path = os.path.join(project_root, path)

        # 1.提取目录并创建（如果不存在）
        dirname = os.path.dirname(image_abs_path)
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
            with open(image_abs_path, 'wb') as f:
                f.write(encoded.tobytes())
            print(image_abs_path, "写入成功")
            return True
        else:
            return False
    except Exception as e:
        print(f"保存失败: {e}")
        return False