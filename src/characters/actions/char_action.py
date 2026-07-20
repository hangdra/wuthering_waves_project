# @Author  : liuha
# @Time    : 2026/7/11 22:26
# @File    : char_action.py

from enum import IntEnum
from src.utils.log import logger
import time


class ActionMethod(IntEnum):
    CLICK = 0
    HOLD = 1
    SEND_KEY = 2


class ActionType(IntEnum):
    LIGHT_ATT = 0
    HEAVY_ATT = 1
    E_ATT = 2
    R_ATT = 3
    SWITCH = 4
    BREAK = 5


class CharAction:

    def __init__(self, char_name: str, action_name: str, action_type: ActionType, action_method: ActionMethod,
                 animation_time: float = -1.0, last_dmg_time: float = -1.0, w_light: float = 0.0, w_heavy: float = 0.0,
                 w_e: float = 0.0, w_r: float = 0.0, w_switch: float = 0.0, is_combo: bool = False, action_phase=1,
                 force_time_stop_time=0.0, next_action_ready=None, animation_duration_multiplier=1, animation_duration_add_time_value=0.0):

        if next_action_ready is None:
            next_action_ready = []
        else:
            next_action_ready = next_action_ready

        self.charName = char_name
        self.logger = logger
        self.charName = char_name
        self.actionName = action_name
        self.actionType = action_type
        self.actionMethod = action_method
        self.animationTime = animation_time
        self.action_phase = action_phase  # 普攻阶段，对于露西这种多普攻阶段的 有1，2 2种
        self.is_combo = is_combo
        self.force_time_stop_time = force_time_stop_time
        # self.trigger_time = trigger_time
        self.last_dmg_time = last_dmg_time  # 多段出伤的话，最后一段出伤时间
        self.w_light = w_light #最短触发下一次普攻时间
        self.w_heavy = w_heavy #最短触发下一次重击时间 重击可以预输入
        self.w_e = w_e #最短触发下一次共鸣技能时间 大部分共鸣技能可以打断 普攻和重击
        self.w_r = w_r #最短触发下一次大招时间 可以打断普攻重击 和 无时停的共鸣技能
        self.w_switch = w_switch #最短触发下一次切人时间，  如果当前技能无时停效果，默认为last_dmg_time
        if self.w_e == 0.0 and self.last_dmg_time > 0:
            self.w_e = self.last_dmg_time
        if self.w_r == 0.0 and self.last_dmg_time > 0:
            self.w_r = self.last_dmg_time

        # 影响所有 动作 间隔时间，参数越大，连招之间 越不流畅， 1 和 0 最 流畅，更小也会导致连招失败概率大幅增加
        self.animation_duration_multiplier = animation_duration_multiplier  # 动作 时间 倍数器，电脑卡顿，连招放不出来，提高倍数 默认角色使用更长时间完成动作，尽量不要大于1.5
        self.animation_duration_add_time_value = animation_duration_add_time_value  # 动作时间 绝对值 增加修正数， 每一个动作时间绝对值增加
        if self.animation_duration_multiplier < 1:
            self.animation_duration_multiplier = 1
        if self.animation_duration_add_time_value < 0.0:
            self.animation_duration_add_time_value = 0.0

    def do_action(self):
        self.logger.info(self.charName + " 释放 " +self.actionName)
        pass

    def sleep_before_action(self,last_action):
        pass
