# @Author  : liuha
# @Time    : 2026/7/13 01:27
# @File    : get_game_window_id.py
import win32gui

class GetGameWindowId:

    def __init__(self,window_name = None):
        self.window_name = None
        self.hwnd_id = None
        self.window_name = window_name
        if self.window_name is None:
            self.window_name = "鸣潮  "
        self.reget_hwnd_id()

    def reget_hwnd_id(self):
        # window_name = "(48) Kisuumi - Twitch - Google Chrome"
        self.hwnd_id = win32gui.FindWindow(None, self.window_name)
        print("______________self.hwnd_id ",self.hwnd_id)
        if self.hwnd_id == 0:
            self.window_name = self.window_name.rstrip()
            self.hwnd_id = win32gui.FindWindow(None, self.window_name.rstrip())
            if self.hwnd_id == 0:
                raise Exception("GetGameWindowId no hwnd_id error")


# game_window_instance = GetGameWindowId()
