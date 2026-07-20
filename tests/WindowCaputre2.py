import win32api  # 需要额外导入
import win32con
import time
import dxcam
from PIL import Image
import win32gui
from src.utils.get_game_window_id import game_window_instance


class WindowCapture2:
    def __init__(self):
        self.game_window_instance = game_window_instance
        hwnd = game_window_instance.hwnd_id
        if hwnd is None:
            raise ValueError("窗口句柄无效")
        self._hwnd = hwnd
        self._update_rect()

        # 创建 dxcam 相机（不设置固定 region，由每次 grab 动态传入）
        self.camera = dxcam.create(output_idx=0, output_color="RGB")

    def _update_rect(self):
        left, top, right, bottom = win32gui.GetWindowRect(self._hwnd)
        self._left, self._top, self._right, self._bottom = left, top, right, bottom
        self._width = right - left
        self._height = bottom - top

    def _clip_to_screen(self, left, top, right, bottom):
        """将矩形裁剪到虚拟屏幕可见区域"""
        screen_left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        screen_top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        screen_right = screen_left + win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        screen_bottom = screen_top + win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)

        crop_left = max(left, screen_left)
        crop_top = max(top, screen_top)
        crop_right = min(right, screen_right)
        crop_bottom = min(bottom, screen_bottom)

        if crop_left >= crop_right or crop_top >= crop_bottom:
            return None  # 完全不可见
        return (crop_left, crop_top, crop_right, crop_bottom)

    def capture(self, as_array=False):
        """捕获窗口内容，返回 PIL Image 或 numpy 数组（RGB）"""
        # 若窗口最小化则还原
        if win32gui.IsIconic(self._hwnd):
            print("还原窗口")
            win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
            time.sleep(0.2)  # 等待窗口恢复

        # 获取当前窗口矩形
        left, top, right, bottom = win32gui.GetWindowRect(self._hwnd)
        region = self._clip_to_screen(left, top, right, bottom)

        if region is None:
            print(" regin is None")
            # 窗口完全不可见，尝试还原并重新获取
            win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
            time.sleep(0.3)
            left, top, right, bottom = win32gui.GetWindowRect(self._hwnd)
            region = self._clip_to_screen(left, top, right, bottom)
            if region is None:
                raise RuntimeError("窗口完全不在屏幕可见区域内，无法截图")

        # 使用裁剪后的区域抓取
        frame = self.camera.grab(region=region)

        if frame is None:
            print("屏幕没有变化")
            return None
            # 极少数情况仍失败，尝试用 PrintWindow 作为回退（可选）
            # 这里也可以选择重试一次
            time.sleep(0.05)
            frame = self.camera.grab(region=region)

        if as_array:
            return frame
        else:
            return Image.fromarray(frame, mode='RGB')

    def close(self):
        if hasattr(self, 'camera'):
            self.camera.stop()
            self.camera.release()
            del self.camera

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()




capturer_fast_need_window_active = WindowCapture2()