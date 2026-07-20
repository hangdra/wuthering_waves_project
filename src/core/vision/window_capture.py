import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image
import numpy as np
import time


class WindowCapture:
    """
    后台窗口截图类（基于 PrintWindow API）
    复用 DC 和位图对象，适合高频调用
    """

    def __init__(self,game_window_instance=None):
        """
        初始化窗口捕获器
        """
        if game_window_instance is None:
            raise Exception("none game_window_instance")
        self.game_window_instance = game_window_instance
        hwnd = game_window_instance.hwnd_id
        print(f"WindowCapture hwnd: {hwnd}")

        if hwnd is None:
            raise ValueError("必须提供 window_title 或 hwnd")

        self._hwnd = hwnd

        # 获取初始窗口尺寸
        self._left, self._top, self._right, self._bottom = win32gui.GetWindowRect(hwnd)
        self._width = self._right - self._left
        self._height = self._bottom - self._top

        # 创建 DC 和位图（将在 _create_resources 中完成）
        self._hwnd_dc = None
        self._mfc_dc = None
        self._save_dc = None
        self._save_bitmap = None
        self._create_resources()


    def _create_resources(self):
        """（重新）创建所有 GDI 资源"""
        # 释放旧资源（如果有）
        self._release_resources()

        # 获取窗口 DC
        self._hwnd_dc = win32gui.GetWindowDC(self._hwnd)
        self._mfc_dc = win32ui.CreateDCFromHandle(self._hwnd_dc)
        self._save_dc = self._mfc_dc.CreateCompatibleDC()

        # 创建兼容位图
        self._save_bitmap = win32ui.CreateBitmap()
        self._save_bitmap.CreateCompatibleBitmap(self._mfc_dc, self._width, self._height)
        self._save_dc.SelectObject(self._save_bitmap)

    def _release_resources(self):
        """释放所有 GDI 资源"""
        if self._save_bitmap:
            win32gui.DeleteObject(self._save_bitmap.GetHandle())
            self._save_bitmap = None
        if self._save_dc:
            self._save_dc.DeleteDC()
            self._save_dc = None
        if self._mfc_dc:
            self._mfc_dc.DeleteDC()
            self._mfc_dc = None
        if self._hwnd_dc:
            win32gui.ReleaseDC(self._hwnd, self._hwnd_dc)
            self._hwnd_dc = None

    def _ensure_window_valid(self):
        """检查窗口是否仍然有效，若无效则抛出异常"""
        if not win32gui.IsWindow(self._hwnd):
            raise Exception(f"窗口句柄 {self._hwnd} 已失效")

    def _update_size_if_changed(self):
        """检测窗口尺寸是否变化，若变化则重建资源"""
        left, top, right, bottom = win32gui.GetWindowRect(self._hwnd)
        new_width = right - left
        new_height = bottom - top
        if new_width != self._width or new_height != self._height:
            self._left, self._top, self._right, self._bottom = left, top, right, bottom
            self._width, self._height = new_width, new_height
            self._create_resources()  # 重建位图以匹配新尺寸

    def capture_bitblt(self, as_array=False):
        # 确保窗口不是最小化（BitBlt 需要屏幕上有内容）
        if win32gui.IsIconic(self._hwnd):
            win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
            time.sleep(0.05)

        # 直接从屏幕 DC 复制到内存 DC（比 PrintWindow 快）
        self._save_dc.BitBlt((0, 0), (self._width, self._height),
                             self._mfc_dc, (0, 0), win32con.SRCCOPY)

        # 获取像素数据（与之前相同）
        bmpinfo = self._save_bitmap.GetInfo()
        bmpstr = self._save_bitmap.GetBitmapBits(True)
        if as_array:
            return np.frombuffer(bmpstr, dtype=np.uint8).reshape(
                (self._height, self._width, 4))[:, :, :3]
        else:
            return Image.frombuffer('RGB', (self._width, self._height),
                                    bmpstr, 'raw', 'BGRX', 0, 1)

    def capture_fast_numpy(self):
        # 1. 如果窗口最小化，先还原
        if win32gui.IsIconic(self._hwnd):
            win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
            self._update_size_if_changed()
            time.sleep(0.05)  # 等待还原动画完成

        # 调用 PrintWindow
        result = windll.user32.PrintWindow(self._hwnd, self._save_dc.GetSafeHdc(), 2)
        if result == 0:
            print("警告: PrintWindow 调用失败，截图可能不完整")

        # 获取位图信息
        bmpinfo = self._save_bitmap.GetInfo()
        width, height = bmpinfo['bmWidth'], bmpinfo['bmHeight']

        # 获取原始像素字节 (BGRX 格式，每个像素 4 字节)
        bmpstr = self._save_bitmap.GetBitmapBits(True)

        # 直接构造 NumPy 数组，形状 (height, width, 4)，数据类型 uint8
        img_bgra = np.frombuffer(bmpstr, dtype=np.uint8).reshape((height, width, 4))

        # 若需要 RGB（实际是 BGR），提取前三个通道（注意：是视图，不复制）
        # 如果需要 BGR（OpenCV 风格），可以直接返回 img_bgra[:, :, :3]
        return img_bgra[:, :, :3]  # 返回 (H, W, 3)，顺序为 BGR（Windows 原生）

    def capture_fast(self, as_array=False):
        """
        快速截图，跳过有效性/尺寸/最小化检查（请确保外部保证窗口有效且尺寸不变）
        """
        # 直接调用 PrintWindow
        result = windll.user32.PrintWindow(self._hwnd, self._save_dc.GetSafeHdc(), 2)
        if result == 0:
            # 可选降级：使用 BitBlt（但会丢失后台能力）
            pass

        # 获取位图数据（与之前相同）
        bmpinfo = self._save_bitmap.GetInfo()
        bmpstr = self._save_bitmap.GetBitmapBits(True)
        img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                               bmpstr, 'raw', 'BGRX', 0, 1)
        if as_array:
            return np.array(img)
        return img

    def capture_new(self, as_array=True):
        """
        截取当前窗口内容（支持后台/被遮挡）
        返回 numpy.ndarray，格式为 BGR (H, W, 3)，适合 OpenCV 直接使用
        """
        self._ensure_window_valid()
        self._update_size_if_changed()

        # 如果窗口最小化，尝试还原（根据需要可注释）
        if win32gui.IsIconic(self._hwnd):
            win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
            time.sleep(0.05)

        # 使用 PrintWindow 将窗口内容绘制到 save_dc
        result = windll.user32.PrintWindow(self._hwnd, self._save_dc.GetSafeHdc(), 2)
        if result == 0:
            print("警告: PrintWindow 调用失败，截图可能不完整")

        # 获取位图信息
        bmpinfo = self._save_bitmap.GetInfo()
        width, height = bmpinfo['bmWidth'], bmpinfo['bmHeight']

        # 获取原始像素字节（格式为 BGRX，每个像素 4 字节）
        bmpstr = self._save_bitmap.GetBitmapBits(True)

        # 直接构造 numpy 数组，形状 (height, width, 4)，dtype=uint8
        img_bgra = np.frombuffer(bmpstr, dtype=np.uint8).reshape((height, width, 4))

        # 移除 Alpha 通道，只保留前三个通道（BGR），返回 (H, W, 3)
        # 注意：这是原数组的视图，不复制内存，非常高效
        img_bgr = img_bgra[:, :, :3]

        # 如果调用者需要 PIL.Image（兼容旧代码），可在此转换，但既然你用 cv2，直接返回数组
        # 若仍想保留 as_array 参数，可以这样：
        # if not as_array:
        #     from PIL import Image
        #     return Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
        # 但推荐统一返回数组，不再依赖 PIL
        return img_bgr

    def capture(self, as_array=False):
        """
        截取当前窗口内容（支持后台/被遮挡）
        :param as_array: 若为 True 返回 numpy.ndarray (H, W, 3)，否则返回 PIL.Image
        :return: PIL.Image 或 numpy.ndarray
        """
        self._ensure_window_valid()
        self._update_size_if_changed()

        # 如果窗口最小化，尝试还原（可选，根据需求可注释）
        if win32gui.IsIconic(self._hwnd):
            win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
            time.sleep(0.1)  # 等待窗口还原（可根据情况调整）

        # 使用 PrintWindow 将窗口内容绘制到 save_dc
        # 参数 2 = PW_RENDERFULLCONTENT，包含非客户区（标题栏等）
        result = windll.user32.PrintWindow(self._hwnd, self._save_dc.GetSafeHdc(), 2)
        if result == 0:
            # PrintWindow 失败时，可尝试仅客户区（参数 0）或 BitBlt 降级
            # 这里仅打印警告，但可能得到黑屏
            print("警告: PrintWindow 调用失败，截图可能不完整")

        # 从位图获取像素数据
        bmpinfo = self._save_bitmap.GetInfo()
        bmpstr = self._save_bitmap.GetBitmapBits(True)
        img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                               bmpstr, 'raw', 'BGRX', 0, 1)

        if as_array:
            return np.array(img)
        return img

    def close(self):
        """主动释放资源（调用后对象不能再使用）"""
        self._release_resources()
        self._hwnd = None

    def __del__(self):
        """析构时释放资源（防御性）"""
        self.close()

    # 可选：上下文管理器支持
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


