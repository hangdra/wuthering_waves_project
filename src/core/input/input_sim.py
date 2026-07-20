from enum import IntEnum
import win32con
import win32gui
import win32api
import time
from src.assets.config.config_keymap import vk_key_dict


# from src.utils.get_game_window_id import game_window_instance


class InputUtils:

    def __init__(self, game_window_instance):
        self.game_window_instance = game_window_instance
        self.hwnd_id = game_window_instance.hwnd_id

    def renew_hwnd_id(self):
        self.hwnd_id = self.game_window_instance.reget_hwnd_id()

    def try_activate(self):
        # pass
        # print("in activate")
        self.activate()

    def send_key(self, key, down_time=0.01):
        self.send_key_down(key)
        time.sleep(down_time)
        self.send_key_up(key)

    def send_key_down(self, key, activate=True):
        if activate:
            self.try_activate()
        vk_code = self.get_key_by_str(key)
        lparam = self.make_lparam(vk_code, is_up=False)
        self.post(win32con.WM_KEYDOWN, vk_code, lparam, )

    def send_key_up(self, key):
        # logger.debug(f'send_key_up {key}')
        vk_code = self.get_key_by_str(key)
        lparam = self.make_lparam(vk_code, is_up=True)
        self.post(win32con.WM_KEYUP, vk_code, lparam, )

    def make_lparam(self, vk_code, is_up=False):
        scan_code = win32api.MapVirtualKey(vk_code, 0)
        lparam = (scan_code << 16) | 1
        if is_up:
            lparam |= (1 << 30) | (1 << 31)
        return lparam

    def get_key_by_str(self, key):
        key = str(key)
        if key_code := vk_key_dict.get(key.upper()):
            vk_code = key_code
        else:
            vk_code = win32api.VkKeyScan(key)
        return vk_code

    def post(self, message, wParam=0, lParam=0):
        if self.hwnd_id is None:
            raise Exception("no  hwnd_id  error")
        try:
            win32gui.PostMessage(self.hwnd_id, message, wParam, lParam)
        except Exception as e:
            print(f'PostMessage error {self.hwnd_id}: {e}')

    def send(self, message, wParam=0, lParam=0):
        if self.hwnd_id is None:
            raise Exception("no hwnd_id error")
        try:
            # 临时替换为 SendMessage
            result = win32gui.SendMessage(self.hwnd_id, message, wParam, lParam)
            print(f"[DEBUG] SendMessage returned: {result}")
        except Exception as e:
            print(f'Message error {self.hwnd_id}: {e}')

    def activate(self):
        self.post(win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)

    def deactivate(self):
        self.post(win32con.WM_ACTIVATE, win32con.WA_INACTIVE, 0)

    # default_ = 0x90bfa
    def click(self, x=-1, y=-1, down_time=0.05, move_bool=True, key="left"):
        if move_bool:
            long_position = self.move(x, y)
            time.sleep(down_time)
            # print("move over", x, y, long_position)
        else:
            long_position = self.update_mouse_pos(x, y, activate=True)

        if key == "left":
            btn_down = win32con.WM_LBUTTONDOWN
            btn_mk = win32con.MK_LBUTTON
            btn_up = win32con.WM_LBUTTONUP
        elif key == "middle":
            btn_down = win32con.WM_MBUTTONDOWN
            btn_mk = win32con.MK_MBUTTON
            btn_up = win32con.WM_MBUTTONUP
        else:
            btn_down = win32con.WM_RBUTTONDOWN
            btn_mk = win32con.MK_RBUTTON
            btn_up = win32con.WM_RBUTTONUP
        self.post(btn_down, btn_mk, long_position)
        time.sleep(down_time)
        self.post(btn_up, 0, long_position)

    def move(self, x, y, down_btn=0):
        # long_pos = self.update_mouse_pos(x, y, True)
        # self.send(win32con.WM_MOUSEMOVE, down_btn, long_pos)
        abs_x, abs_y = win32gui.ClientToScreen(self.hwnd_id, (int(x), int(y)))
        print("_______cursor abs_x,abs_y", abs_x, abs_y)
        win32api.SetCursorPos((abs_x,abs_y))
        long_pos = self.update_mouse_pos(x, y, True)
        self.post(win32con.WM_MOUSEMOVE, down_btn, long_pos)
        return long_pos

    def update_mouse_pos(self, x, y, activate=True):
        self.try_activate()

        base_hwnd = self.hwnd_id

        if x == -1 or y == -1:
            x, y = (0, 0)
        else:
            pass
            # x, y = hwnd_window.get_top_window_cords(x, y)
            bg_mouse_pos = (x, y)

        try:
            abs_x, abs_y = win32gui.ClientToScreen(base_hwnd, (int(x), int(y)))

            target_hwnd = base_hwnd

            _dynamic_target_hwnd = target_hwnd

            local_x, local_y = win32gui.ScreenToClient(target_hwnd, (abs_x, abs_y))

            print("x,y", x, y, "abs_x,abs_y", abs_x, abs_y, "local_x,local_y", local_x, local_y)

            # logger.debug(
            #     f'hwnd_window hwnds ={hwnd_window.} top_hwnd={hwnd_window.top_hwnd}: {hwnd_descriptions}')
            # logger.debug(
            #     f'mouse_pos dynamically aimed at {target_hwnd} ({win32gui.GetClassName(target_hwnd)}): {local_x}, {local_y}')
            return win32api.MAKELONG(local_x, local_y)

        except Exception as e:
            print(f'update_mouse_pos conversion error targeting {base_hwnd}', e)
            return win32api.MAKELONG(int(x), int(y))

    def mouse_down(self, x=-1, y=-1, key="left"):
        long_position = self.update_mouse_pos(x, y)
        if key == "left":
            action = win32con.WM_LBUTTONDOWN
            btn = win32con.MK_LBUTTON
        elif key == "middle":
            action = win32con.WM_MBUTTONDOWN
            btn = win32con.MK_MBUTTON
        else:
            action = win32con.WM_RBUTTONDOWN
            btn = win32con.MK_RBUTTON
        self.post(action, btn, long_position)

    def mouse_up(self, x=-1, y=-1, key="left"):
        long_position = self.update_mouse_pos(x, y)
        if key == "left":
            action = win32con.WM_LBUTTONUP
        elif key == "middle":
            action = win32con.WM_MBUTTONUP
        else:
            action = win32con.WM_RBUTTONUP
        self.post(action, 0,
                  long_position)

# input_instance = InputUtils()
