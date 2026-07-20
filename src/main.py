# import win32con
# import win32gui
# import win32api
# import time
# from src.characters.subs.Lucy import Lucy
#
# # from src.core.input.input_sim import InputUtils, ActionType
# #
# # vk_key_dict = {
# #     'F1': win32con.VK_F1,
# #     'F2': win32con.VK_F2,
# #     'F3': win32con.VK_F3,
# #     'F4': win32con.VK_F4,
# #     'F5': win32con.VK_F5,
# #     'F6': win32con.VK_F6,
# #     'F7': win32con.VK_F7,
# #     'F8': win32con.VK_F8,
# #     'F9': win32con.VK_F9,
# #     'F10': win32con.VK_F10,
# #     'F11': win32con.VK_F11,
# #     'F12': win32con.VK_F12,
# #     'ESC': win32con.VK_ESCAPE,
# #     'CTRL': win32con.VK_CONTROL,
# #     'CONTROL': win32con.VK_CONTROL,
# #     'LCTRL': win32con.VK_LCONTROL,
# #     'RCTRL': win32con.VK_RCONTROL,
# #     'CTRL_L': win32con.VK_LCONTROL,
# #     'CTRL_R': win32con.VK_RCONTROL,
# #     'LCONTROL': win32con.VK_LCONTROL,
# #     'RCONTROL': win32con.VK_RCONTROL,
# #     'ALT': win32con.VK_MENU,
# #     'LALT': win32con.VK_LMENU,
# #     'RALT': win32con.VK_RMENU,
# #     'ALT_L': win32con.VK_LMENU,
# #     'ALT_R': win32con.VK_RMENU,
# #     'SHIFT': win32con.VK_SHIFT,
# #     'LSHIFT': win32con.VK_LSHIFT,
# #     'RSHIFT': win32con.VK_RSHIFT,
# #     'SHIFT_L': win32con.VK_LSHIFT,
# #     'SHIFT_R': win32con.VK_RSHIFT,
# #     'TAB': win32con.VK_TAB,
# #     'ENTER': win32con.VK_RETURN,
# #     'RETURN': win32con.VK_RETURN,
# #     'SPACE': win32con.VK_SPACE,
# #     'LEFT': win32con.VK_LEFT,
# #     'UP': win32con.VK_UP,
# #     'RIGHT': win32con.VK_RIGHT,
# #     'DOWN': win32con.VK_DOWN,
# #     'BACKSPACE': win32con.VK_BACK,
# #     'PAGEUP': win32con.VK_PRIOR,
# #     'PAGE_UP': win32con.VK_PRIOR,
# #     'PAGEDOWN': win32con.VK_NEXT,
# #     'PAGE_DOWN': win32con.VK_NEXT,
# #     'HOME': win32con.VK_HOME,
# #     'END': win32con.VK_END,
# #     'INSERT': win32con.VK_INSERT,
# #     'DELETE': win32con.VK_DELETE,
# #     'CAPSLOCK': win32con.VK_CAPITAL,
# #     'CAPS_LOCK': win32con.VK_CAPITAL,
# #     'NUMLOCK': win32con.VK_NUMLOCK,
# #     'NUM_LOCK': win32con.VK_NUMLOCK,
# #     'SCROLLLOCK': win32con.VK_SCROLL,
# #     'SCROLL_LOCK': win32con.VK_SCROLL,
# #     'PRINTSCREEN': win32con.VK_SNAPSHOT,
# #     'PRINT_SCREEN': win32con.VK_SNAPSHOT,
# #     'WIN': win32con.VK_LWIN,
# #     'WINDOWS': win32con.VK_LWIN,
# #     'COMMAND': win32con.VK_LWIN,
# #     'CMD': win32con.VK_LWIN,
# #     'CMD_L': win32con.VK_LWIN,
# #     'CMD_R': win32con.VK_RWIN,
# #     'META': win32con.VK_LWIN,
# #     # Add more keys as needed
# # }
# #
# #
# def list_window_names():
#     def winEnumHandler(hwnd_id, ctx):
#         if win32gui.IsWindowVisible(hwnd_id):
#             print(hex(hwnd_id), '"' + win32gui.GetWindowText(hwnd_id) + '"')
#             list_inner_windows(hwnd_id)
#
#     win32gui.EnumWindows(winEnumHandler, None)
#     print("------------over------------------")
#
#
# def list_inner_windows(whndl):
#     def callback(hwnd_id, hwnds):
#         if win32gui.IsWindowVisible(hwnd_id) and win32gui.IsWindowEnabled(hwnd_id):
#             hwnds[win32gui.GetClassName(hwnd_id)] = hwnd_id
#             return True
#
#     hwnds = {}
#     win32gui.EnumChildWindows(whndl, callback, hwnds)
#     if hwnds:
#         print(str(whndl), "child", hwnds)
#
#     print("------------over------------------")
#     return hwnds
# #
# #
# # def try_activate(hwnd_id):
# #     # pass
# #     # print("in activate")
# #     activate(hwnd_id)
# #
# #
# # def send_key(key, down_time=0.01, hwnd_id=None):
# #     send_key_down(key, hwnd_id=hwnd_id)
# #     time.sleep(down_time)
# #     send_key_up(key, hwnd_id=hwnd_id)
# #
# #
# # def send_key_down(key, activate=True, hwnd_id=None):
# #     if activate:
# #         try_activate(hwnd_id)
# #     vk_code = get_key_by_str(key)
# #     lparam = make_lparam(vk_code, is_up=False)
# #     post(win32con.WM_KEYDOWN, vk_code, lparam, hwnd_id)
# #
# #
# # def send_key_up(key, hwnd_id=None):
# #     # logger.debug(f'send_key_up {key}')
# #     vk_code = get_key_by_str(key)
# #     lparam = make_lparam(vk_code, is_up=True)
# #     post(win32con.WM_KEYUP, vk_code, lparam, hwnd_id)
# #
# #
# # def make_lparam(vk_code, is_up=False):
# #     scan_code = win32api.MapVirtualKey(vk_code, 0)
# #     lparam = (scan_code << 16) | 1
# #     if is_up:
# #         lparam |= (1 << 30) | (1 << 31)
# #     return lparam
# #
# #
# # def get_key_by_str(key):
# #     key = str(key)
# #     if key_code := vk_key_dict.get(key.upper()):
# #         vk_code = key_code
# #     else:
# #         vk_code = win32api.VkKeyScan(key)
# #     return vk_code
# #
# #
# # def post(message, wParam=0, lParam=0, hwnd_id=None):
# #     if hwnd_id is None:
# #         raise Exception("no hwnd_id error")
# #     try:
# #         win32gui.PostMessage(hwnd_id, message, wParam, lParam)
# #     except Exception as e:
# #         print(f'PostMessage error {hwnd_id}: {e}')
# #
# #
# # def activate(hwnd_id):
# #     post(win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0, hwnd_id=hwnd_id)
# #
# #
# # def deactivate(hwnd_id):
# #     post(win32con.WM_ACTIVATE, win32con.WA_INACTIVE, 0, hwnd_id=hwnd_id)
# #
# #
# # # default_hwnd_id = 0x90bfa
# # def click(x=-1, y=-1, down_time=0.01, move_bool=True, key="left", hwnd_id=None):
# #     if move_bool:
# #         long_position = move(x, y, hwnd_id=hwnd_id)
# #         time.sleep(down_time)
# #     else:
# #         long_position = update_mouse_pos(x, y, activate=True, hwnd_id=hwnd_id)
# #
# #     if key == "left":
# #         btn_down = win32con.WM_LBUTTONDOWN
# #         btn_mk = win32con.MK_LBUTTON
# #         btn_up = win32con.WM_LBUTTONUP
# #     elif key == "middle":
# #         btn_down = win32con.WM_MBUTTONDOWN
# #         btn_mk = win32con.MK_MBUTTON
# #         btn_up = win32con.WM_MBUTTONUP
# #     else:
# #         btn_down = win32con.WM_RBUTTONDOWN
# #         btn_mk = win32con.MK_RBUTTON
# #         btn_up = win32con.WM_RBUTTONUP
# #
# #     post(btn_down, btn_mk, long_position
# #          , hwnd_id)
# #     time.sleep(down_time)
# #     post(btn_up, 0, long_position
# #          , hwnd_id)
# #
# #
# # def move(x, y, down_btn=0, hwnd_id=None):
# #     long_pos = update_mouse_pos(x, y, True, hwnd_id=hwnd_id)
# #     post(win32con.WM_MOUSEMOVE, down_btn, long_pos, hwnd_id=hwnd_id)
# #     return long_pos
# #
# #
# # def update_mouse_pos(x, y, activate=True, hwnd_id=None):
# #     try_activate(hwnd_id)
# #
# #     base_hwnd = hwnd_id
# #
# #     if x == -1 or y == -1:
# #         x, y = (0, 0)
# #     else:
# #         pass
# #         # x, y = hwnd_window.get_top_window_cords(x, y)
# #         bg_mouse_pos = (x, y)
# #
# #     try:
# #         abs_x, abs_y = win32gui.ClientToScreen(base_hwnd, (int(x), int(y)))
# #
# #         target_hwnd = base_hwnd
# #
# #         _dynamic_target_hwnd = target_hwnd
# #
# #         local_x, local_y = win32gui.ScreenToClient(target_hwnd, (abs_x, abs_y))
# #
# #         # logger.debug(
# #         #     f'hwnd_window hwnds hwnd_id={hwnd_window.hwnd_id} top_hwnd={hwnd_window.top_hwnd}: {hwnd_descriptions}')
# #         # logger.debug(
# #         #     f'mouse_pos dynamically aimed at {target_hwnd} ({win32gui.GetClassName(target_hwnd)}): {local_x}, {local_y}')
# #         return win32api.MAKELONG(local_x, local_y)
# #
# #     except Exception as e:
# #         print(f'update_mouse_pos conversion error targeting {base_hwnd}', e)
# #         return win32api.MAKELONG(int(x), int(y))
# #
# #
# # def mouse_down(x=-1, y=-1, key="left", hwnd_id=None):
# #     long_position = update_mouse_pos(x, y, hwnd_id=hwnd_id)
# #     if key == "left":
# #         action = win32con.WM_LBUTTONDOWN
# #         btn = win32con.MK_LBUTTON
# #     elif key == "middle":
# #         action = win32con.WM_MBUTTONDOWN
# #         btn = win32con.MK_MBUTTON
# #     else:
# #         action = win32con.WM_RBUTTONDOWN
# #         btn = win32con.MK_RBUTTON
# #     post(action, btn, long_position, hwnd_id=hwnd_id)
# #
# #
# # def mouse_up(x=-1, y=-1, key="left", hwnd_id=None):
# #     long_position = update_mouse_pos(x, y, hwnd_id=hwnd_id)
# #     if key == "left":
# #         action = win32con.WM_LBUTTONUP
# #     elif key == "middle":
# #         action = win32con.WM_MBUTTONUP
# #     else:
# #         action = win32con.WM_RBUTTONUP
# #     post(action, 0,
# #          long_position, hwnd_id=hwnd_id)
# #
# #
# # def heavy_att(duration, hwnd_id=None):
# #     mouse_down(hwnd_id=hwnd_id)
# #     time.sleep(duration)
# #     mouse_up(hwnd_id=hwnd_id)
# #
# #
# # def continuous_att(duration, hwnd_id=None, interval=0.03):
# #     click_time = int(duration / interval)
# #     for i in range(click_time):
# #         click(hwnd_id=hwnd_id)
# #         time.sleep(interval)
# #     time.sleep(duration - click_time * interval)
# #
# #
# # def continuous_press_some_key(key, duration, hwnd_id=None, interval=0.03):
# #     press_time = int(duration / interval)
# #     for i in range(press_time):
# #         send_key(key, hwnd_id=hwnd_id)
# #         time.sleep(interval)
# #     time.sleep(duration - press_time * interval)
# #
# #
# # def lucy_light_att_with_heavy(hwnd_id):
# #     click(hwnd_id=hwnd_id)
# #     time.sleep(0.19)
# #     click(hwnd_id=hwnd_id)
# #     time.sleep(0.53)
# #     click(hwnd_id=hwnd_id)
# #     heavy_att(1.0, hwnd_id=hwnd_id)
# #
# #
# # def lucy_light_att(hwnd_id, start_index=0):
# #     # finished
# #
# #     time_gate = [0.15, 0.33, 0.57]
# #     for i in range(start_index, len(time_gate)):
# #         continuous_att(time_gate[i], hwnd_id=hwnd_id)
# #     return 0.5
# #
# #
# # def lucy_light_att_p2(hwnd_id, start_index=0):
# #     # finished
# #
# #     time_gate = [0.12, 0.48, 0.61]
# #     for i in range(start_index, len(time_gate)):
# #         continuous_att(time_gate[i], hwnd_id=hwnd_id)
# #     return 0.98
# #     time.sleep(0.9)
# #
# #
# # def lucy_light_att_p2_with_heavy(hwnd_id):
# #     # 不推荐 二段重击会浮空 没有共鸣重击要打下落攻击
# #     click(hwnd_id=hwnd_id)
# #     time.sleep(0.12)
# #     click(hwnd_id=hwnd_id)
# #     time.sleep(0.8)
# #     click(hwnd_id=hwnd_id)
# #     heavy_att(1.15, hwnd_id=hwnd_id)
# #
# #
# # def lucy_double_e(hwnd_id):
# #     # finished
# #     time_gate = [0.9]
# #     continuous_press_some_key("e", time_gate[0], hwnd_id)
# #     time.sleep(1.5)
# #     # continuous_att(0.1,hwnd_id)
# #     lucy_light_att(hwnd_id, start_index=1)
# #     return 0
# #
# #
# # def lucy_e_att_p2(hwnd_id):
# #     # finished
# #     continuous_press_some_key("e", 0.1, hwnd_id)
# #     time.sleep(2.5)
# #     # 额外时间
# #     continuous_att(0.05, hwnd_id)
# #     lucy_light_att_p2(hwnd_id=hwnd_id, start_index=1)
# #     return 14
# #
# #
# # def lucy_ult(hwnd_id):
# #     continuous_press_some_key("r", 0.1, hwnd_id)
# #     # time fixed
# #     time.sleep(3.4)
# #     print("here_______")
# #     heavy_att(1.1, hwnd_id=hwnd_id)
# #     time.sleep(1.5)
# #     continuous_att(0.1, hwnd_id)
# #     return 0
# #
# #
# # def lucy_double_heavy_p2(hwnd_id):
# #     # finished
# #     heavy_att(1.6, hwnd_id=hwnd_id)
# #     # time.sleep(1.4)
# #     # 额外时间s
# #     return 1.4, 0.85
# #
# #
# # def shore_keeper_e(hwnd_id, auto_att=False):
# #     continuous_press_some_key("e", 0.1, hwnd_id)
# #     w1 = 0.52
# #     if auto_att:
# #         time.sleep(w1)
# #         continuous_att(0.6, hwnd_id=hwnd_id)
# #     return w1, 0, 0
# #
# #
# # def shore_keeper_normal_att_5(hwnd_id):
# #     # over
# #     continuous_att(0.95, hwnd_id=hwnd_id)
# #     time_sleep = 0.8
# #     time.sleep(time_sleep)
# #     # print("sleep_time",time_sleep )
# #     return 0.8, 0, 0
# #
# #
# # def shore_keeper_normal_att_after_e(hwnd_id, test_index):
# #     # over
# #     duration_time = 1.3
# #     print("duration_time", duration_time)
# #     continuous_att(duration_time, hwnd_id=hwnd_id)
# #     # print("sleep_time",time_sleep )
# #     return 0.8, 0, 0
# #
# #
# # def build_shore_keeper_forte(hwnd_id):
# #     heavy_att(5, hwnd_id=hwnd_id)
# #     click(hwnd_id=hwnd_id)
# #     print("build over2_______________________")
# #     time.sleep(1.5)
# #
# #
# # def shore_keeper_heavy_att(hwnd_id):
# #     # over
# #     duration_time = 0.29
# #     heavy_att(duration_time, hwnd_id=hwnd_id)
# #     return 1.4, 0, 0
# #
# #
# # def shore_keeper_in_auto_att(hwnd_id, test_index):
# #     duration_time = 1.1 - test_index * 0.05
# #     duration_time = 0.85
# #
# #     # print("shore_keeper_in_auto_att duration_time",duration_time)
# #     continuous_att(duration_time, hwnd_id=hwnd_id)
# #
# #
# # def build_up_ult(hwnd_id):
# #     print("build up_____________________________ start")
# #
# #     for i in range(13):
# #         shore_keeper_normal_att_5(hwnd_id)
# #         time.sleep(0.05)
# #         w1, w2, w3 = shore_keeper_heavy_att(hwnd_id)
# #         time.sleep(w1)
# #         print("loop build_up_ult", i)
# #         if i % 2 == 0:
# #             w_key_time = 1.5
# #             continuous_press_some_key("w", w_key_time, hwnd_id)
# #     print("build up_____________________________ over")
# #
# #
# # def shore_keep_use_ult(hwnd_id):
# #     continuous_press_some_key("r", 0.1, hwnd_id)
# #     return 2.6, 2.6, 0
# #
# #
# # class Lucy(InputUtils):
# #
# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #
# #         self.e_phase = 0
# #         self.last_p1_e1_cast_time = -1
# #         self.last_p1_e2_cast_time = -1
# #         self.last_enter_p2_time = -1
# #         self.last_forte_e_cast_time = -1
# #         self.last_p1_heavy2_cast_time = -1  # 最后一次阶段一 2段重击释放时间
# #         self.last_p2_forte_heavy2_cast_time = -1  # 最后一次阶段2 露西强化2段重击释放时间
# #
# #         self.phase2_after_heavy2_no_action_back_to_phase1_time = 8 + 1  # 防止延迟出伤 多1秒
# #         self.light_att_animation_p1 = [0.18, 0.59, 0.97, 1.38]
# #         self.light_att_animation_p2 = [0.17, 0.82, 1.06, 1.03]
# #         self.last_light_att_index_p1 = -1  # 最后执行普攻段数 p1
# #         self.last_light_att_index_p2 = -1  # 最后执行普攻段数 p2
# #
# #         # self.next_light_att_index_p1 = -1 #下一次普攻的段数 p1
# #         # self.next_light_att_index_p2 = -1 #下一次普攻的段数 p2
# #         # self.next_heavy_att_index_p1 = -1
# #         # self.next_heavy_att_index_p2 = -1
# #         # todo 切人情况需要测试
# #         self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed = 2.6  # 露西E2后能等待最多多久重击开始蓄力还能接上重击（必须在场）
# #         self.max_wait_time_p1_light = 2.6
# #         # todo 切露西进来 自动普攻2段后接普通时间，接重击时间
# #         self.ground_switch_in_wait_time_to_normal_att = 0.4
# #         self.ground_switch_in_wait_time_to_heavy_att = 0.4
# #         # todo 地面切露西进场 等待的最长可接重击1，2的时间
# #         self.ground_switch_in_max_wait_time_to_lance_heavy_att = 3.5
# #
# #     def lucy_heavy2_after_light3(self, index=0, learning_rate=0.0):
# #         # fixed 10/10
# #         duration_time = 1.15  # +index*learning_rate
# #         # if learning_rate>0.0:
# #         #     print("lucy_heavy2_after_light3  duration_time", duration_time)
# #         print(self.w_light)
# #         self.try_sleep_before_action(ActionType.HEAVY_ATT)
# #         self.heavy_att(duration_time)
# #         # fixed 18/20
# #         w_light = 2.0  # +index*learning_rate
# #         self.update_wait_time(w_light=w_light)
# #         # if learning_rate>0.0:
# #         #     print("w_light", w_light)
# #         # print("w_light=", w_light)
# #
# #     def lucy_p1_light_att(self, start_index=0, end_index=-1, test_index=0, test_learning_rate=0.0):
# #         # 10/10 index 0
# #         # 10/10 index 1
# #         # 10/10 index 2
# #         # 10/10 index 3   lucy.test_light_all(end=5,index=i,test_learning_rate=-0.00)
# #         animation_duration = self.light_att_animation_p1
# #         # change_index = end_index - 2 if (end_index - 2) < len(animation_duration) else len(animation_duration)
# #         # animation_duration[change_index] = animation_duration[change_index] + test_index * test_learning_rate
# #         if test_learning_rate != 0.0:
# #             print("end_index -1 duration", animation_duration[end_index - 2])
# #         if end_index == -1 or end_index > len(animation_duration):
# #             end_index = len(animation_duration)
# #         if start_index > len(animation_duration):
# #             start_index = len(animation_duration)
# #         if end_index < start_index:
# #             end_index = start_index
# #         if start_index > end_index:
# #             start_index = end_index
# #         print("light att start_index", start_index, "end_index", end_index)
# #         for i in range(start_index, end_index):
# #             # print("____________i",i)
# #             self.try_light_att(w_light=animation_duration[i])
# #             self.last_light_att_index_p1 = i
# #
# #     def check_combo_time_valid(self):
# #         return time.time() - self.last_action_time < self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed
# #
# #     def lucy_light_default(self, end_index=-1, must_combo=False):
# #         """
# #         :param end_index:
# #         :param must_combo:  True 只执行初始 普攻计数不为-1的行为，False 所有行为都支持 并且普攻
# #         :return:
# #         """
# #         if self.e_phase in [0, 1, 2]:
# #             phase = 1
# #             light_att_animation = self.light_att_animation_p1
# #         else:
# #             phase = 2
# #             light_att_animation = self.light_att_animation_p2
# #         if end_index == -1 or end_index > len(light_att_animation):
# #             end_index = len(light_att_animation)
# #
# #         if must_combo:
# #             if phase == 1:
# #                 if self.next_light_step_p1 in [0,4]:
# #                     return False
# #
# #         start_index = 0
# #         if self.last_action_type in [ActionType.LIGHT_ATT, ActionType.E_ATT,
# #                                      ActionType.SWITCH] and self.check_combo_time_valid():
# #             if phase == 1:
# #                 start_index = self.last_light_att_index_p1 + 1
# #             else:
# #                 start_index = self.last_light_att_index_p2 + 1
# #             if start_index >= len(light_att_animation):
# #                 start_index = 0
# #
# #         for i in range(start_index, end_index):
# #             self.try_light_att(w_light=light_att_animation[i])
# #             if phase == 1:
# #                 self.last_light_att_index_p1 = i
# #             else:
# #                 self.last_light_att_index_p2 = i
# #
# #         return True
# #
# #     def test_random_light_att(self, index=0):
# #         # fixed 10/10
# #         # le1 = index
# #         # print("test_random_light_att", le1)
# #         # self.lucy_normal_att(end_index=le1)
# #         # self.lucy_normal_att(start_index=le1)
# #         # self.lucy_normal_att()
# #         le1 = index
# #         print("test_random_light_att", le1)
# #         self.lucy_p1_light_att(end_index=le1)
# #         self.lucy_p1_light_att(start_index=le1)
# #         self.lucy_p1_light_att()
# #
# #     # def get_animation_duration_list(self,duration_list):
# #
# #     def test_light_all(self, end=-1, index=0, test_learning_rate=0.0):
# #         # self.lucy_p1_light_att(end_index=end, test_index=index,test_learning_rate=test_learning_rate)
# #         self.lucy_p1_light_att(end_index=4)
# #         self.lucy_p1_light_att(end_index=4)
# #
# #     def lucy_heavy12_for_switch_in_or_light2(self, index=0, learning_rate=0.0):
# #         # fixed 10/10 lucy.test_light2_and_heavy(index=i,test_learning_rate=0)
# #         duration_time = 1.45 + index * learning_rate
# #         if learning_rate > 0.0:
# #             print("lucy_heavy2_att_just_after_light3  duration_time", duration_time)
# #         if not self.last_action_type == ActionType.LIGHT_ATT:
# #             print("last action type", self.last_action_type)
# #         self.try_sleep_before_action(ActionType.HEAVY_ATT)
# #         self.heavy_att(duration_time)
# #         w_light = 2.0  # +index*learning_rate
# #         self.update_wait_time(w_light=w_light)
# #
# #     def test_light2_and_heavy(self, index=0, test_learning_rate=0.0):
# #         self.lucy_p1_light_att(end_index=1)
# #         self.lucy_p1_light_att(start_index=1, end_index=2)
# #         # checked duration_time and w_light
# #         self.lucy_heavy_default(duration_time=1.5, w_light=2.0)
# #
# #     def test_heavy2_for_switch_in(self, index=0, test_learning_rate=0.0):
# #         # 丽贝卡变奏入场
# #         self.lucy_p1_light_att(end_index=1)
# #
# #         # real happend
# #         self.lucy_p1_light_att(start_index=1, end_index=2)
# #
# #     # def lucy_heavy_p1_default(self,duration_time,wait_time = 0.0):
# #     #     self.try_sleep_before_action(ActionType.HEAVY_ATT)
# #     #     self.heavy_att(duration_time)
# #     #     # w_light = 2.0  # +index*learning_rate
# #     #     self.update_wait_time(w_light=wait_time)
# #
# #     def reset_data(self):
# #         # 退出压缩算法状态
# #         if self.e_phase == 3:
# #             self.e_phase = 0
# #         # 一定要设置为None 要么 第二次进入压缩哦阶段， 任何攻击都会触发 此函数
# #         self.try_sleep_call_back_after_sleep_function = None
# #
# #     def check_data_before_each_action_sleep(self):
# #         # print("in here function[check_data_before_each_action_sleep]")
# #         if self.e_phase != 3:
# #             # 大招改变状态
# #             self.reset_data()
# #             return
# #         # 如果阶段2 打出强化重击后8s内没有攻击动作，则退回阶段一
# #         if self.last_action_time - self.last_p2_forte_heavy2_cast_time > self.phase2_after_heavy2_no_action_back_to_phase1_time:
# #             print(" self.e_phase", self.e_phase, "reset to 0")
# #             self.reset_data()
# #         else:
# #             # 如果8s 内有动作，更新阶段2重击最后动作时间
# #             self.last_p2_forte_heavy2_cast_time = self.last_action_time
# #
# #     def lucy_heavy_default(self, duration_time, w_light=0.0, w_heavy=0.0, w_e=0.0, w_r=0.0, w_switch=0.0):
# #         self.try_sleep_before_action(ActionType.HEAVY_ATT)
# #         self.heavy_att(duration_time)
# #         if self.e_phase == 3:
# #             self.try_sleep_call_back_after_sleep_function = self.check_data_before_each_action_sleep
# #             self.last_p2_forte_heavy2_cast_time = time.time()
# #         if self.e_phase in [0, 1, 2]:
# #             self.last_p1_heavy2_cast_time = time.time()
# #         # w_light = 2.0  # +index*learning_rate
# #         self.update_wait_time(w_light=w_light, w_heavy=w_heavy, w_e=w_e, w_r=w_r, w_switch=w_switch)
# #
# #     def lucy_ult(self):
# #         self.try_sleep_before_action(ActionType.R_ATT)
# #         self.continuous_press_some_key("r", 0.1)
# #         # 释放共鸣解放 重置死锁cd
# #         self.last_forte_e_cast_time = -1
# #         # todo 再次判定 大招是否释放成功再睡觉
# #         # todo 若大招放成功 变灰
# #         self.reset_data()
# #         time.sleep(3.4)
# #         self.heavy_att(1.1)
# #         # todo 确认等待时间 也可以先放着 （反正预输入重击）
# #         self.update_wait_time()
# #
# #     def lucy_cast_e_p2(self):
# #         # done
# #         self.try_sleep_before_action(ActionType.E_ATT)
# #         self.continuous_press_some_key("e", 0.1)
# #         self.last_forte_e_cast_time = time.time()
# #         # todo self.last_enter_p2_time 有啥用？
# #         if self.e_phase == 2:
# #             self.last_enter_p2_time = self.last_forte_e_cast_time
# #         self.e_phase = 3
# #         # 阶段2 e技能 时停且不可切人
# #         time.sleep(2.5)
# #         self.update_wait_time(next_light_step_p2=2)
# #
# #     def lucy_cast_e_p1(self, wait_time=0.0):
# #         # print("_________________________lucy_cast_e_p1 self.e_phase", self.e_phase)
# #         # todo 检查e是否可以释放 是否阶段1
# #         self.try_sleep_before_action(ActionType.E_ATT)
# #         self.continuous_press_some_key("e", 0.1)
# #         if self.e_phase == 0:
# #             w_light = 0.7
# #             w_heavy = 0.0
# #             w_e = 0.6  # check
# #             w_r = 0.6
# #             next_light_p1 = 2
# #             next_heavy_p1 = 2
# #             self.e_phase = 1
# #             self.last_p1_e1_cast_time = time.time()
# #         elif self.e_phase == 1:
# #             w_light = 0.0
# #             w_heavy = 0.0
# #             w_e = 0.0
# #             w_r = 0.0
# #             next_light_p1 = 2
# #             next_heavy_p1 = 0
# #             self.e_phase = 2
# #             self.last_p1_e2_cast_time = time.time()
# #         else:
# #             raise Exception("不支持的 self.e_phase" + str(self.e_phase))
# #         # todo  e_phase == 1
# #         self.update_wait_time(w_light=w_light, w_heavy=w_heavy, w_e=w_e, w_r=w_r, next_light_step_p1=next_light_p1,
# #                               next_heavy_step_p1=next_heavy_p1)
# #
# #     def lucy_p2_light_att(self, start_index=0, end_index=-1, test_index=0, test_learning_rate=0.0):
# #         # 10/10 index 0 lucy.lucy_p2_light_att(end_index=2,test_index=i,test_learning_rate=0.01)
# #         # 10/10 index 1  lucy.lucy_p2_light_att(end_index=3,test_index=i,test_learning_rate=0.01)
# #         # 10/10 index 2 lucy.lucy_p2_light_att(end_index=4,test_index=i,test_learning_rate=0.01)
# #         # 10/10 index 3  lucy.lucy_p2_light_att(end_index=5,test_index=i,test_learning_rate=0)
# #         #               lucy.lucy_p2_light_att(end_index=4)
# #         animation_duration = [0.17, 0.82, 1.06, 1.03]
# #         change_index = end_index - 2 if (end_index - 2) < len(animation_duration) else len(animation_duration)
# #         animation_duration[change_index] = animation_duration[change_index] + test_index * test_learning_rate
# #         if test_learning_rate != 0.0:
# #             print("end_index -1 duration", animation_duration[end_index - 2])
# #         if end_index == -1 or end_index > len(animation_duration):
# #             end_index = len(animation_duration)
# #         if start_index > len(animation_duration):
# #             start_index = len(animation_duration)
# #         if end_index < start_index:
# #             end_index = start_index
# #         if start_index > end_index:
# #             start_index = end_index
# #         # print("start_index", start_index, "end_index", end_index)
# #         for i in range(start_index, end_index):
# #             # print("____________i", i)
# #             self.try_light_att(w_light=animation_duration[i])
# #
# #     def test_ult_and_heavy2(self, pre_input_heavy2_duration_time=1.4):
# #         # 测试露西大招重击
# #         self.lucy_ult()
# #         self.heavy_att(pre_input_heavy2_duration_time)
# #
# #     # def test_lucy_p1_e1_ult_not_ready_rotation(self,duration_time):
# #     #     self.lucy_cast_e_p1()
# #     #     self.lucy_heavy2_only(duration_time=duration_time)
# #
# #     # def lucy_p2_heavy12(self,test_wait_time=0.0):
# #     #     #done
# #     #     self.try_sleep_before_action(ActionType.HEAVY_ATT)
# #     #     self.heavy_att(2)
# #     #     #等待2段重击出伤后可以使用e或者r
# #     #     #done w_light
# #     #     # self.update_wait_time(w_light=0.5,w_e=0.68,w_r=0.68)
# #     #     self.update_wait_time(w_light=0.71, w_e=0.71, w_r=0.71)
# #
# #     def test_lucy_p2_light4_and_heavy2_and_e_and_light4(self, wait_time=0.0):
# #         """
# #         压缩阶段普攻1-4 接重击1，2 接普攻1-4
# #         :param wait_time:
# #         :return:
# #         """
# #         # done test code
# #         # time_d = 0.68#+0.05*i
# #         # lucy.test_lucy_p2_light4_and_heavy2_and_e_and_light4(time_d) #2.2ok
# #         # print("露西进入阶段2 普攻后重击 等待重击出伤 后马上大招 等待时间",time_d)
# #         # time_here = time.time()
# #         # while time.time() -time_here <10:
# #         #     lucy.lucy_p2_light_att(end_index=4)
# #         self.lucy_p2_light4_and_heavy2()
# #         # self.lucy_p2_light_att(end_index=4)
# #         # self.lucy_heavy_default(duration_time=2,w_light=0.71, w_e=0.71, w_r=0.71)
# #         # self.lucy_p2_heavy12(wait_time)
# #         self.continuous_press_some_key("e", 0.1)
# #         self.lucy_p2_light_att(end_index=4)
# #
# #     # def lucy_heavy_after_ult(self,wait_time=0.0):
# #     #     self.try_sleep_before_action(ActionType.HEAVY_ATT)
# #     #     self.heavy_att(1.4)
# #     #     self.update_wait_time(w_light=2.0, w_e=wait_time, w_r=0.0)
# #     def lucy_p2_light4_and_heavy2(self):
# #         # 露西压缩 阶段普攻4下然后重击
# #         self.lucy_p2_light_att(end_index=4)
# #         print(" lucy_p2_light4_and_heavy2 普攻4下结束")
# #         # w_light=0.71, w_e=0.71, w_r=0.71 checked
# #         self.lucy_heavy_default(duration_time=2, w_light=0.71, w_e=0.71, w_r=0.71)
# #
# #     def lucy_ult_and_pre_heavy2(self):
# #         # todo  前置确认，大招就绪？
# #         self.lucy_ult()
# #         self.lucy_heavy_default(duration_time=1.4, w_light=2.0, w_e=1.6)
# #
# #     def lucy_quick_p2_and_ult(self, wait_time=2.0):
# #         # todo 确认是否e_forte_ready
# #         self.lucy_cast_e_p2()
# #         # todo  前置确认，大招就绪？
# #         self.lucy_p2_light4_and_heavy2()
# #         # todo  如果重击没满 或者 大招没满，一直普攻
# #         self.lucy_ult_and_pre_heavy2()
# #         # self.lucy_p2_light_att(end_index=4)
# #         # self.lucy_p2_heavy12()
# #         # self.lucy_heavy_after_ult(wait_time)
# #
# #     def build_ult(self):
# #         # self.lucy_cast_e_p2()
# #         # self.lucy_cast_e_p1()
# #         if self.e_phase == 0:
# #             self.lucy_cast_e_p1()
# #             self.lucy_cast_e_p1()
# #         elif self.e_phase == 1:
# #             self.lucy_cast_e_p1()
# #         for i in range(13):
# #             self.lucy_p1_light3_heavy2()
# #             # self.lucy_p1_light_att()
# #
# #     def back_to_p1_e0(self):
# #         if self.e_phase in [1, 2]:
# #             print("in here ", self.e_phase)
# #             for i in range(7 - self.e_phase * 3):
# #                 self.lucy_p1_light3_heavy2()
# #             self.lucy_cast_e_p2()
# #             print(" e p2 casted~~~~~~~~~~~~~~~~~~~~~~~~~~")
# #             self.lucy_p2_light4_and_heavy2()
# #             time.sleep(self.phase2_after_heavy2_no_action_back_to_phase1_time)
# #         elif self.e_phase == 3:
# #             print("in here ", self.e_phase)
# #             self.lucy_p2_light4_and_heavy2()
# #             time.sleep(self.phase2_after_heavy2_no_action_back_to_phase1_time)
# #         print("back to p1 over ~~~")
# #
# #     def lucy_e1_light2_4(self, light_end_index=4):
# #         """ 露西放e1 并且衔接普攻2-4"""
# #         if self.e_phase == 0:
# #             self.lucy_cast_e_p1()
# #             self.lucy_p1_light_att(start_index=1, end_index=light_end_index)
# #
# #     def lucy_e1_e2(self):
# #         if self.e_phase == 0:
# #             self.lucy_cast_e_p1()
# #             self.lucy_cast_e_p1()
# #
# #     def lucy_e1_heavy2(self, wait_time=0.0):
# #         """
# #         露西 E1 接重2
# #         :param wait_time:
# #         :return:
# #         """
# #         self.lucy_cast_e_p1()
# #         # done 测定各个攻击行为等待时间
# #         # w_light = 1.8 done
# #         # w_e = 1.2 done 出伤之后立马接2段e
# #         self.try_heavy2()
# #         # self.lucy_heavy_default(duration_time=0.76, w_light=1.8, w_e=1.2, w_r=1.2)
# #
# #     def lucy_e2_heavy2(self, time_in=0.0):
# #         """
# #         露西 E2 接重击12
# #         不推荐使用 露西E2后应该直接切人
# #         :param time_in:
# #         :return:
# #         """
# #         self.lucy_cast_e_p1()
# #         # 测试E2 后多久能接上重击的时间 求最大
# #         # todo 测定各个攻击行为等待时间
# #         self.try_heavy2(time_in=time_in)
# #
# #     def lucy_p1_light3_heavy2(self, time_in=0.0):
# #         # todo 循环有问题 单独循环没问题 接E1 或者 E2都不太行
# #         self.lucy_p1_light_att(end_index=3)
# #         self.lucy_heavy_default(duration_time=1.15, w_light=2.0, w_e=time_in, w_r=time_in)
# #
# #     def try_heavy2(self, time_in=0.0):
# #         # todo
# #         if self.last_action_type == ActionType.E_ATT:
# #             if self.e_phase == 2:
# #                 if time.time() < self.last_p1_e2_cast_time + self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed:
# #                     # duration_time=2.5 done 2.4 is ok too
# #                     self.lucy_heavy_default(duration_time=2.5, w_light=1.9, w_e=time_in, w_r=time_in)
# #             elif self.e_phase == 1:
# #                 if time.time() < self.last_p1_e1_cast_time + self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed:
# #                     self.lucy_heavy_default(duration_time=0.76, w_light=1.8, w_e=1.2, w_r=1.2)
# #
# #         if self.last_action_type == ActionType.LIGHT_ATT:
# #             if self.last_action_time + self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed > time.time():
# #                 if self.e_phase in [0, 1, 2]:
# #                     # todo 如果有rebecca buff 从普攻1，2，开始长按重击 不要普攻3
# #                     if self.prevent_switch_dead_time > time.time():
# #                         if self.last_light_att_index_p1 == 0:
# #                             self.lucy_light_default(end_index=3)
# #                     else:
# #                         # 阶段1普攻3+重击
# #                         self.lucy_light_default(end_index=3)
# #                         self.lucy_heavy_default(duration_time=1.15, w_light=2.0)
# #                 else:
# #                     # 阶段2普攻4+重击
# #                     self.lucy_light_default(end_index=4)
# #                     self.lucy_heavy_default(duration_time=2, w_light=0.71, w_e=0.71, w_r=0.71)
#
#     # def lucy_p2_light4_and_heavy2(self):
#     #     # 露西压缩 阶段普攻4下然后重击
#     #     self.lucy_p2_light_att(end_index=4)
#     #     print(" lucy_p2_light4_and_heavy2 普攻4下结束")
#     #     # w_light=0.71, w_e=0.71, w_r=0.71 checked
#     #     self.lucy_heavy_default(duration_time=2, w_light=0.71, w_e=0.71, w_r=0.71)
#
#
# def main():
#     print('auto_action scaffold: run perception -> planner -> executor')
#     list_window_names()
#     window_name = "鸣潮  "
#     hwnd_id = win32gui.FindWindow(None, window_name)
#     print(window_name, hwnd_id)
#
#     lucy = Lucy(hwnd_id)
#     # #冷启动
#     # lucy.send_key("SHIFT")
#     time.sleep(0.5)
#     loop_time = 10
#     loop_sleep = 3
#     first_time_in = True
#
#     # todo 重击之后 接e3
#     for i in range(3, 4):
#         print(i)
#     try:
#         for i in range(loop_time):
#             # if first_time_in:
#             #     first_time_in = False
#             #     lucy.e_phase = 0
#             # lucy.back_to_p1_e0()
#
#
#             # 测试p1普攻间隔
#             target_step = 4
#             # self.light_att_animation_p1 = [0.18, 0.59, 0.97, 1.38]
#             # self.light_att_animation_p2 = [0.17, 0.82, 1.06, 1.03]
#             lucy.lucy_p2_light_att(end_index=target_step-1)
#             # l1-l2 1.8 l2-l3 1.3
#             time_sleep = 3.1#-i*0.1
#             print("_____________________time_sleep", time_sleep)
#             time.sleep(time_sleep)
#             lucy.lucy_p2_light_att(start_index=target_step-1, end_index=target_step)
#
#
#             # lucy.lucy_p1_light3_heavy2()
#             # lucy.lucy_e1_heavy2()
#
#             # 测试露西e1 重击 e2重击 出伤之后 e3  需要等待时间
#             # lucy.lucy_p1_light3_heavy2()
#             # lucy.lucy_e1_heavy2()
#             # duration = 1.3 + 0.2 * i  # 1.0 失败 1.9 ok
#             # print("__________________________duration", duration)
#             # lucy.lucy_e2_heavy2(time_in=duration)
#             # print("e2 should be cast now")
#             # lucy.lucy_cast_e_p2()
#             # print(" done test+++++++++++++++++++++++++++++++++++++++++++++++++")
#             # break
#
#             # lucy.build_ult()
#             #
#             # # 测试露西进入二阶段并直接进入大招流程并且大招后预输入重击
#             # # todo 预输入重击后，测试 普攻合e 技能可以释放时机。
#             # wait_time = 1.6
#             # print("----------------------------------wait_time", wait_time)
#             # lucy.lucy_quick_p2_and_ult(wait_time = wait_time)
#             # lucy.lucy_cast_e_p1()
#             # # lucy.lucy_p2_light_att(end_index=4)
#             # # lucy.test_ult_and_heavy2(pre_input_heavy2_duration_time=1.4)#成功次数1
#             # # break
#             # #测试露西 p1 or p2 大招 预输入重击 #todo
#
#             # # # 测试露西 阶段1 e1 接重2 #todo
#             #
#             # lucy.lucy_e2_heavy2() # 2.4 不够   2.6多了
#             # break
#             # 测试露西 阶段1 e2 接重2 #todo
#
#             # 测试露西e1 重击 e2重击 之后普攻需要等待时间 done
#             # duration = 1.9 + 0.2 * i  # 1.0 失败 1.9 ok
#             # lucy.lucy_e1_heavy2()
#             # print("__________________________duration", duration)
#             # lucy.lucy_e2_heavy2(time_in=duration)
#             # lucy.lucy_p1_light_att()
#             # print(" done test+++++++++++++++++++++++++++++++++++++++++++++++++")
#
#             # 测试露西e1 重击 e2重击 e2后最大等待时间能接上 重击 done
#             # time_wait = 2.6  # 2ok 3失败 2.5 ok 2.8 失败
#             # lucy.lucy_e1_heavy2()
#             # print("__________________________time_wait", time_wait)
#             # lucy.lucy_e2_heavy2(wait_time=time_wait)
#             # print(" done test")
#
#             # done 测试露西e1 普攻
#             # time_wait = 0.7  # + 0.05*i #0.6不行 0.7ok
#             # print("__________________________time_wait", time_wait)
#             # lucy.lucy_cast_e_p1(wait_time=time_wait)
#             # lucy.lucy_p1_light_att(start_index=1, end_index=4)
#             # print(" done test")
#
#             # done 测试露西e1 e2连放时间 done
#             # time_wait = 0.6  # + 0.2*i #0.3 no 0.6ok
#             # print("time_wait", time_wait)
#             # lucy.lucy_cast_e_p1(wait_time=time_wait)
#             # lucy.lucy_cast_e_p1()
#
#             # 露西e1 重击 之后等待时间普攻 done
#             # wait_light = 1.2  # done
#             # print("____________________wait_light", wait_light)
#             # lucy.lucy_e1_heavy2(wait_light)
#             # lucy.lucy_cast_e_p1()  # done
#
#             # time_d = 0.68#+0.05*i
#             # lucy.test_lucy_p2_light4_and_heavy2_and_e_and_light4(time_d) #2.2ok
#             # print("露西进入阶段2 普攻后重击 等待重击出伤 后马上大招 等待时间",time_d)
#             # time_here = time.time()
#             # while time.time() -time_here <10:
#             #     lucy.lucy_p2_light_att(end_index=4)
#             # break
#             # 露西进入阶段2 普攻后重击 之后普攻需要等待时间 #done
#
#             # lucy.lucy_cast_e_p2(0.0)#ok 0.0可以4段普攻
#             # lucy.lucy_p2_light_att(end_index=4)
#             # break
#             # 露西进入阶段2 测试进入后普攻 间隔 #done
#
#             # lucy.lucy_p2_light_att(end_index=5,test_index=i,test_learning_rate=0)
#             # lucy.lucy_p2_light_att(end_index=4)
#             # 测试露西阶段2 普攻  #done
#
#             # lucy.test_light2_and_heavy(index=i,test_learning_rate=0)
#             # lucy.test_light_all(end=5,index=i,test_learning_rate=-0.00)
#             # lucy.lucy_p1_light3_heavy2(index=i,test_learning_rate=0.00)
#             # lucy.test_light1_3_heavy2_light1_4(index=i)
#             # lucy.test_light1_4_and_light1_4_wait_time(index=0)
#             # lucy.test_random_light_att(index=i)
#             # #测试地面切换守岸人后普攻直到攒满重击能量
#             # send_key("3", hwnd_id=hwnd_id)
#             # time.sleep(1.1)
#             # send_key("1", hwnd_id=hwnd_id)
#             #
#             # time_sleep_after_switch_in = 0.4-0.05*i
#             # if time_sleep_after_switch_in <= 0:
#             #     time_sleep_after_switch_in = 0
#             # time.sleep(time_sleep_after_switch_in)
#             # print("time_sleep_after_switch_in",time_sleep_after_switch_in)
#             # shore_keeper_in_auto_att(hwnd_id,i)
#             # time.sleep(0.05)
#             # w1, w2, w3 = shore_keeper_heavy_att(hwnd_id)
#             # time.sleep(0.5)
#             # send_key("SHIFT", hwnd_id=hwnd_id)
#             # continuous_press_some_key("w", 1, hwnd_id)
#             #
#             # # 测试空中切换守岸人后普攻直到攒满重击能量
#             # send_key("3", hwnd_id=hwnd_id)
#             # time.sleep(1.1)
#             # send_key("SPACE", hwnd_id=hwnd_id)
#             # time.sleep(0.23)
#             # send_key("1", hwnd_id=hwnd_id)
#             #
#             # time_sleep_after_switch_in = 0.85
#             # if time_sleep_after_switch_in <= 0:
#             #     time_sleep_after_switch_in = 0
#             # time.sleep(time_sleep_after_switch_in)
#             # print("time_sleep_after_switch_in", time_sleep_after_switch_in)
#             # shore_keeper_in_auto_att(hwnd_id, i)
#             # time.sleep(0.05)
#             # w1, w2, w3 = shore_keeper_heavy_att(hwnd_id)
#             # time.sleep(0.5)
#             # send_key("SHIFT", hwnd_id=hwnd_id)
#             # continuous_press_some_key("w", 1, hwnd_id)
#
#             # continuous_att(0.9, hwnd_id)
#             # heavy_att(0.5, hwnd_id=hwnd_id)
#
#             # next_normal_move_must_sleep_time = lucy_e_att_p2(hwnd_id)
#             # next_normal_move_must_sleep_time = lucy_double_e(hwnd_id)
#             # next_normal_move_must_sleep_time,ult_need_wait = lucy_double_heavy_p2(hwnd_id)
#             # time.sleep(ult_need_wait)
#             # next_normal_move_must_sleep_time = lucy_ult(hwnd_id)
#             # shore_keeper_e(hwnd_id,auto_att=True,test_index=i)
#             # shore_keeper_normal_att_5(hwnd_id)
#             # build_shore_keeper_forte(hwnd_id)
#             # shore_keeper_heavy_att(hwnd_id,test_index=i)
#             # after_heavy_sleep_time = 1.2-0.02*i
#             # time.sleep(after_heavy_sleep_time)
#             # print("after_heavy_sleep_time",after_heavy_sleep_time)
#             # shore_keeper_normal_att_5(hwnd_id)
#             # l1,l2,l3 = shore_keeper_normal_att_5(hwnd_id)
#             # after_normal_sleep_time_heavy = 0
#             # if after_normal_sleep_time_heavy <0:
#             #     after_normal_sleep_time_heavy = 0
#             # time.sleep(after_normal_sleep_time_heavy)
#             # print("after_heavy_sleep_time", after_normal_sleep_time_heavy)
#             # l1,l2,l3 =shore_keeper_heavy_att(hwnd_id)
#             # loop_sleep = l1
#             # build_up_ult(hwnd_id)
#             # 测试大招后放e然后重复构建大招
#             # w1,w2,w3 =shore_keep_use_ult(hwnd_id)
#             # time_sleep = w2
#             # time.sleep(time_sleep)
#             # print("sleep time",str(time_sleep))
#             # w1,w2,w3 = shore_keeper_e(hwnd_id, auto_att=False)
#             # time.sleep(w1)
#             # print("over all over")
#             # build_up_ult(hwnd_id)
#             # #测试e后普工重击
#             # w1, w2, w3 = shore_keeper_e(hwnd_id, auto_att=False)
#             # time.sleep(w1)
#             # shore_keeper_normal_att_after_e(hwnd_id,i)
#             # time.sleep(0.05)
#             # w1, w2, w3 = shore_keeper_heavy_att(hwnd_id)
#             # time.sleep(w1)
#             # continuous_press_some_key("w", 1, hwnd_id)
#             # lucy_light_att_p2_with_heavy(hwnd_id=hwnd_id)
#             # time.sleep(next_normal_move_must_sleep_time)
#             print("loop over all over", (i + 1), "/", loop_time)
#             time.sleep(loop_sleep)
#             # if i == 5 :
#             #     send_key("2", hwnd_id=hwnd_id)
#     finally:
#         send_key("1", hwnd_id=hwnd_id)
#
#
# if __name__ == '__main__':
#     main()
