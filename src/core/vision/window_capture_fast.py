# @Author  : liuha
# @Time    : 2026/7/13 04:53
# @File    : window_capture_fast.py


import win32api  # 需要额外导入
import win32con
import time
import dxcam
from PIL import Image
import win32gui


class WindowCapture2:
    def __init__(self,game_window_instance = None):
        if game_window_instance is None:
            raise Exception("none game_window_instance")
        self.game_window_instance = game_window_instance
        hwnd = game_window_instance.hwnd_id
        if hwnd is None:
            raise ValueError("窗口句柄无效")
        self._hwnd = hwnd
        self._update_rect()
        self.last_frame = None

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

    def is_window_topmost(self):
        """检查窗口是否具有 WS_EX_TOPMOST 扩展样式"""
        ex_style = win32gui.GetWindowLong(self._hwnd, win32con.GWL_EXSTYLE)
        return (ex_style & win32con.WS_EX_TOPMOST) != 0

    def set_window_topmost(self, topmost=True):
        """
        设置窗口是否置顶
        topmost=True  -> 置顶
        topmost=False -> 取消置顶
        """
        flags = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
        if topmost:
            win32gui.SetWindowPos(self._hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, flags)
        else:
            win32gui.SetWindowPos(self._hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, flags)

    def ensure_window_topmost(self):
        """如果窗口未置顶，则置顶；若已置顶则不做操作"""
        if not self.is_window_topmost():
            self.set_window_topmost(True)
            print("窗口已置顶")
        else:
            print("窗口已经是置顶状态")

    def is_window_active(self):
        """检查窗口是否为当前活动窗口（即用户正在操作的窗口）"""
        return win32gui.GetForegroundWindow() == self._hwnd
    def activate_window(self):
        """
        激活目标窗口，使其成为活动窗口（置于最前），但不设置为始终置顶（Topmost）
        处理最小化状态，并兼容 Windows 对 SetForegroundWindow 的限制
        """
        if not win32gui.IsWindow(self._hwnd):
            return False

        # 1. 如果窗口最小化，先还原
        if win32gui.IsIconic(self._hwnd):
            win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
            time.sleep(0.1)  # 等待还原动画完成

        # 2. 如果已经是活动窗口，无需操作
        if win32gui.GetForegroundWindow() == self._hwnd:
            return True

        # 3. 尝试设置为前景窗口（最直接的方式）
        win32gui.SetForegroundWindow(self._hwnd)
        time.sleep(0.05)

        # 4. 若失败（后台进程调用 SetForegroundWindow 可能被系统限制），使用备用方案
        if win32gui.GetForegroundWindow() != self._hwnd:
            # BringWindowToTop 会将窗口带到 Z 序顶部，但不会抢夺键盘焦点（比 SetForegroundWindow 更温和）
            win32gui.BringWindowToTop(self._hwnd)
            # 或者使用 SetWindowPos 移到顶部（注意 HWND_TOP 不带 TOPMOST 属性）
            # win32gui.SetWindowPos(self._hwnd, win32con.HWND_TOP, 0, 0, 0, 0,
            #                       win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

        # 5. 最终检查
        return win32gui.GetForegroundWindow() == self._hwnd
    def capture(self, as_array=False):
        """捕获窗口内容，返回 PIL Image 或 numpy 数组（RGB）"""
        # 若窗口最小化则还原
        if win32gui.IsIconic(self._hwnd):
            print("还原窗口")
            win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
            time.sleep(0.1)  # 等待窗口恢复

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

        #置顶
        # self.ensure_window_topmost()
        #激活窗口
        self.activate_window()
        # 使用裁剪后的区域抓取
        frame = self.camera.grab(region=region)

        if frame is None:
            # print("屏幕没有变化")
            return self.last_frame
            # 极少数情况仍失败，尝试用 PrintWindow 作为回退（可选）
            # 这里也可以选择重试一次
            time.sleep(0.05)
            frame = self.camera.grab(region=region)
        else:
            self.last_frame = frame

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