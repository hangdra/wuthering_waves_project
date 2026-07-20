
import time
from src.characters.actions.char_action import CharAction,ActionType
from src.characters.actions.light_att import LightAttAction


class Character:

    def __init__(self):
        # self.my_input_sim = input_instance
        self.last_switch_in_time = -1
        self.default_sleep_time_each_action_begin = 0.03  # 每个动作执行前最小睡眠时间
        self.w_light = 0.0  # 普攻之前等待时间
        self.w_heavy = 0.0  # 重击之前等待时间
        self.w_e = 0.0  # 共鸣技能之前等待时间
        self.w_r = 0.0  # 共鸣解放之前等待时间
        self.w_switch = 0.0  # 切人之前等待时间（一般用于动画的动作确认，例如奥古斯塔的强化重击，不可以一触发后退就切人,会丢重击的二段)

        self.last_update_w_time = -1
        self.default_sleep_time_switch_in_from_ground = 0.6
        self.last_action_type = ActionType.LIGHT_ATT  # 用处待定 #todo
        self.last_action_time = -1  # 最后动作时间

        self.try_sleep_call_back_after_sleep_function = None

        self.next_light_step_p1 = -1  # 下一次普攻的段数 p1 (1-4)
        self.next_light_step_p2 = -1  # 下一次普攻的段数 p2 (1-4)
        self.next_heavy_step_p1 = -1
        self.next_heavy_step_p2 = -1

        self.prevent_switch_dead_time = -1

        self.last_action = None
        self.last_action_update_time = -1

    def try_sleep_before_action(self, action_type: ActionType, force_minimum_sleep=True):
        self.last_action_type = action_type
        if action_type == ActionType.LIGHT_ATT:
            sleep_time = max(self.w_light, self.w_heavy, self.w_e, self.w_r)
        elif action_type == ActionType.HEAVY_ATT:
            sleep_time = max(self.w_heavy, self.w_e, self.w_r)
        elif action_type == ActionType.E_ATT:
            sleep_time = max(self.w_e, self.w_r)
        elif action_type == ActionType.R_ATT:
            sleep_time = self.w_r
        else:
            sleep_time = self.w_switch
        if sleep_time > 0.0:
            # 电脑卡顿玩家修正
            sleep_time = sleep_time * self.animation_duration_multiplier + self.animation_duration_add_time_value
        if force_minimum_sleep:
            if sleep_time < self.default_sleep_time_each_action_begin:
                sleep_time = self.default_sleep_time_each_action_begin
        time_sleep_need = self.last_update_w_time + sleep_time - time.time()
        if time_sleep_need > 0.0:
            # print("sleep_time",str(time_sleep_need)[:4])
            time.sleep(time_sleep_need)
        self.last_action_time = time.time()
        if self.try_sleep_call_back_after_sleep_function is not None:
            # print("__________self.try_sleep_call_back_after_sleep_function ",self.try_sleep_call_back_after_sleep_function)
            self.try_sleep_call_back_after_sleep_function()
        # if self.last_p2_forte_heavy2_cast_time!=-1 and time.time()-self.last_p2_forte_heavy2_cast_time>5:


    def update_wait_time(self, w_light=0.0, w_heavy=0.0, w_e=0.0, w_r=0.0, w_switch=0.0, next_light_step_p1=0,
                         next_heavy_step_p1=0, next_light_step_p2=0, next_heavy_step_p2=0):
        # if w_light != self.w_light or w_heavy != self.w_heavy or w_e != self.w_e or w_r != self.w_r:
        max_time = max(w_light, w_heavy, w_e, w_r)
        if max_time > 4.0:
            print("error max wait time above 4", w_light, w_heavy, w_e, w_r)
        self.last_update_w_time = time.time()
        self.w_light = w_light
        self.w_heavy = w_heavy
        self.w_e = w_e
        self.w_r = w_r
        self.w_switch = w_switch
        self.next_light_step_p1 = next_light_step_p1
        self.next_heavy_step_p1 = next_heavy_step_p1
        self.next_light_step_p2 = next_light_step_p2
        self.next_heavy_step_p2 = next_heavy_step_p2

    def heavy_att(self, duration):
        print("heavy att", duration)
        try:
            self.my_input_sim.mouse_down()
            time.sleep(duration)
        finally:
            self.my_input_sim.mouse_up()

    def continuous_att(self, duration, interval=0.03, only_click_in_begin_duration=True,
                       begin_duration_time_length=0.15):
        duration_click = duration
        if only_click_in_begin_duration:
            if duration > begin_duration_time_length:
                duration_click = begin_duration_time_length
            else:
                duration_click = duration
        click_time = int(duration_click / interval)
        if click_time == 0:
            click_time = 1
        for i in range(click_time):
            self.my_input_sim.click()
            time.sleep(interval)
        sleep_time = duration - click_time * interval
        if sleep_time > 0:
            time.sleep(sleep_time)

    def continuous_press_some_key(self, key, duration, interval=0.03):
        press_time = int(duration / interval)
        for i in range(press_time):
            self.my_input_sim.send_key(key)
            time.sleep(interval)
        time.sleep(duration - press_time * interval)

    def try_light_att(self, w_light=0.0, w_heavy=0.0, w_e=0.0, w_r=0.0, w_switch=0.0, click_time_default=2,
                      click_time_interval=0.01):
        self.try_sleep_before_action(ActionType.LIGHT_ATT)
        for i in range(click_time_default):
            self.my_input_sim.click()
            if click_time_default > 1 and i < click_time_default:
                time.sleep(click_time_interval)
        self.update_wait_time(w_light=w_light, w_heavy=w_heavy, w_e=w_e, w_r=w_r, w_switch=w_switch)



    def switch_in_action_update_info(self):
        if time.time() - self.last_switch_in_time < 0.3:
            self.update_wait_time(
                w_light=self.default_sleep_time_switch_in_from_ground - (time.time() - self.last_switch_in_time))

    def task_send_key(self,delay,key):
        time.sleep(delay)
        self.my_input_sim.send_key(key)



    def try_wait_before_action(self, action: CharAction,force_minimum_sleep=True):
        # self.last_action_type = action_type
        action_type = action.actionType
        if action_type == ActionType.LIGHT_ATT:
            sleep_time = max(self.w_light, self.w_heavy, self.w_e, self.w_r)
        elif action_type == ActionType.HEAVY_ATT:
            sleep_time = max(self.w_heavy, self.w_e, self.w_r)
        elif action_type == ActionType.E_ATT:
            sleep_time = max(self.w_e, self.w_r)
        elif action_type == ActionType.R_ATT:
            sleep_time = self.w_r
        else:
            sleep_time = action
        if sleep_time > 0.0:
            # 电脑卡顿玩家修正
            sleep_time = sleep_time * self.my_input_sim.animation_duration_multiplier + self.my_input_sim.animation_duration_add_time_value
        if force_minimum_sleep:
            if sleep_time < self.default_sleep_time_each_action_begin:
                sleep_time = self.default_sleep_time_each_action_begin
        time_sleep_need = self.last_update_w_time + sleep_time - time.time()
        if time_sleep_need > 0.0:
            # print("sleep_time",str(time_sleep_need)[:4])
            time.sleep(time_sleep_need)
        self.last_action_time = time.time()
        if self.try_sleep_call_back_after_sleep_function is not None:
            # print("__________self.try_sleep_call_back_after_sleep_function ",self.try_sleep_call_back_after_sleep_function)
            self.try_sleep_call_back_after_sleep_function()

    def update_last_action(self, action: CharAction):
        self.last_action = action
        self.last_action_update_time = time.time()

    def try_click_action(self, action: LightAttAction):
        self.try_wait_before_action(action)
        for i in range(action.click_time_default):
            self.my_input_sim.click()
            if action.click_time_default > 1 and i < action.click_time_default:
                time.sleep(action.click_time_interval)
        self.update_last_action(action)

    def do_action(self,action:CharAction):
        print(isinstance(action, CharAction))
        if action.actionType == ActionType.LIGHT_ATT:
            self.try_click_action(action)


    def do_action_list(self,action_list):
        for action in action_list:
            self.do_action(action)