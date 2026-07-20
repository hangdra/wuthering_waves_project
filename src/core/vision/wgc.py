# @Author  : liuha
# @Time    : 2026/7/15 14:23
# @File    : wgc.py
import numpy as np
import time
from zbl import Capture
from typing import Optional, Dict, Any
import win32gui
import win32con
# from src.utils.get_game_window_id import game_window_instance

class ZBLWindowGrabber:
    """
    高性能窗口/屏幕捕获器，自动适配 zbl 库参数名。
    """

    def __init__(
        self,game_window_instance=None):
        if game_window_instance is None:
            raise Exception("none game_window_instance")
        self.game_window_instance = game_window_instance
        window_name = self.game_window_instance.window_name
        hwnd = game_window_instance.hwnd_id
        if hwnd is None:
            raise ValueError("窗口句柄无效")
        self._hwnd = hwnd
        self._frame_counter = 0
        # 先设置标志位，避免 __del__ 访问不存在的属性
        self._is_open = False
        self._cap = None

        # 构造参数：根据 zbl 的实际签名决定使用哪个参数名
        # 此处我们尝试常见的几种写法
        kwargs: Dict[str, Any] = {}


        # if capture_cursor:
        #     kwargs['cursor_capture'] = True
        #
        # # 合并外部额外参数
        # kwargs.update(extra_kwargs)
        print("kwargs",kwargs)

        try:
            self._cap = Capture(window_name=window_name,**kwargs)
            # 手动进入上下文，初始化捕获会话
            self._cap.__enter__()
            self._is_open = True
        except Exception as e:
            # 如果初始化失败，确保 _cap 为 None，并重新抛出
            self._cap = None
            raise RuntimeError(f"初始化捕获器失败，请检查参数名是否正确。错误: {e}")

    def get_frame(self) -> np.ndarray:
        if not self._is_open or self._cap is None:
            raise RuntimeError("捕获器未正确初始化或已关闭。")
        if self._frame_counter % 100 == 0:
            self._frame_counter = 0
            if win32gui.IsIconic(self._hwnd):
                win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
                time.sleep(0.05)

        self._frame_counter += 1

        frame = self._cap.grab()
        if frame is None:
            raise RuntimeError("获取帧失败，可能窗口已关闭或尺寸为0。")
        return frame.copy()

    def close(self):
        if self._is_open and self._cap is not None:
            self._cap.__exit__(None, None, None)
            self._is_open = False
            self._cap = None

    def __del__(self):
        # 先判断属性是否存在
        if hasattr(self, '_is_open') and self._is_open:
            self.close()


# ---------- 使用示例 ----------
# if __name__ == "__main__":
#     time_begin = time.perf_counter()
#     grabber = ZBLWindowGrabber(window_name="鸣潮")
#     time_e = time.perf_counter()
#     print("init time cost: ", time_e - time_begin)
#     try:
#         frame = grabber.get_frame()
#         print(f"帧形状: {frame.shape}")
#     finally:
#         grabber.close()



