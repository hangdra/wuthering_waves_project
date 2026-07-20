# @Author  : liuha
# @Time    : 2026/7/12 17:03
# @File    : combo.py

from src.core.input.input_sim import input_instance
from src.characters.actions.char_action import CharAction,ActionType

class Combo:


    def __init__(self):
        self.my_input_sim = input_instance
        self.last_switch_in_time = -1
        self.default_sleep_time_each_action_begin = 0.03  # 每个动作执行前最小睡眠时间
        self.w_light = 0.0  # 普攻之前等待时间
        self.w_heavy = 0.0  # 重击之前等待时间
        self.w_e = 0.0  # 共鸣技能之前等待时间
        self.w_r = 0.0  # 共鸣解放之前等待时间
        self.w_switch = 0.0  # 切人之前等待时间（一般用于动画的动作确认，例如奥古斯塔的强化重击，不可以一触发后退就切人,会丢重击的二段)

        self.last_update_w_time = -1
        self.default_sleep_time_switch_in_from_ground = 0.6
        # self.last_action_type = ActionType.LIGHT_ATT  # 用处待定 #todo
        # self.last_action_time = -1  # 最后动作时间

        self.try_sleep_call_back_after_sleep_function = None

        self.next_light_step_p1 = -1  # 下一次普攻的段数 p1 (1-4)
        self.next_light_step_p2 = -1  # 下一次普攻的段数 p2 (1-4)
        self.next_heavy_step_p1 = -1
        self.next_heavy_step_p2 = -1

        self.prevent_switch_dead_time = -1

        self.last_action = None
        self.last_action_cast_time = -1

        self.last_att_action = None
        self.last_att_action_cast_time = -1
        self.next_light_att_action_ready = None
        self.next_heavy_att_action_ready = None
        self.cast_max_away_from_previous_action_time = 0.0 #下一次技能距离此次技能释放最大可以连招时间



    # def sleep_before_next_action(self):
    #     last_att_action = self.last_att_action
    #     if last_att_action is not None:
    #         if self.actionType