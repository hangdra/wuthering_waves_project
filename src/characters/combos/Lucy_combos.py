# @Author  : liuha
# @Time    : 2026/7/12 17:07
# @File    : Lucy_combos.py
from src.characters.combos.combo import Combo
from src.characters.actions.heavy_att import HeavyAttAction
from src.characters.actions.light_att import LightAttAction
from src.characters.actions.e_skill import EAttAction
from src.characters.actions.r_skill import RAttAction
from src.characters.actions.switch_role import SwitchAction
from src.characters.actions.f_break import FBreakAction
from src.characters.actions.char_action import ActionMethod, ActionType

import time


def get_next_action_from_list_by_step(step, actions):
    for action in actions:
        if action.step == step:
            return action
    return None


def init_next_action_ready_by_step(action_list):
    for ac in action_list:
        step_this = ac.step
        for ac2 in action_list:
            if ac2.step == step_this:
                ac.next_action_ready.append(ac2)


class LucyCombos(Combo):

    def __init__(self):
        super().__init__()

        self.p1_l1 = LightAttAction(step=1, char_name="lucy", action_name="p1_light_att1", action_phase=1,
                                    action_type=ActionType.LIGHT_ATT,
                                    action_method=ActionMethod.CLICK, animation_time=0.18, w_light=0.18,
                                    next_light_att_max_wait_time=1.8, is_combo=False)
        self.p1_l2 = LightAttAction(step=2, char_name="lucy", action_name="p1_light_att2", action_phase=1,
                                    action_type=ActionType.LIGHT_ATT,
                                    action_method=ActionMethod.CLICK, animation_time=0.59, w_light=0.59,
                                    next_light_att_max_wait_time=1.3, is_combo=True)
        self.p1_l3 = LightAttAction(step=3, char_name="lucy", action_name="p1_light_att3", action_phase=1,
                                    action_type=ActionType.LIGHT_ATT,
                                    action_method=ActionMethod.CLICK, animation_time=0.97, w_light=0.97,
                                    next_light_att_max_wait_time=1.9, is_combo=True)
        self.p1_l4 = LightAttAction(step=4, char_name="lucy", action_name="p1_light_att4", action_phase=1,
                                    action_type=ActionType.LIGHT_ATT,
                                    action_method=ActionMethod.CLICK, animation_time=1.38, w_light=1.38, is_combo=False)

        self.p2_l1 = LightAttAction(step=1, char_name="lucy", action_name="p2_light_att1", action_phase=2,
                                    action_type=ActionType.LIGHT_ATT,
                                    action_method=ActionMethod.CLICK, animation_time=0.17,
                                    next_light_att_max_wait_time=1.3, is_combo=False)
        self.p2_l2 = LightAttAction(step=2, char_name="lucy", action_name="p2_light_att2", action_phase=2,
                                    action_type=ActionType.LIGHT_ATT,
                                    action_method=ActionMethod.CLICK, animation_time=0.82,
                                    next_light_att_max_wait_time=2.1, is_combo=True)
        self.p2_l3 = LightAttAction(step=3, char_name="lucy", action_name="p2_light_att3", action_phase=2,
                                    action_type=ActionType.LIGHT_ATT,
                                    action_method=ActionMethod.CLICK, animation_time=1.06,
                                    next_light_att_max_wait_time=3.1, is_combo=False)
        self.p2_l4 = LightAttAction(step=4, char_name="lucy", action_name="p2_light_att4", action_phase=2,
                                    action_type=ActionType.LIGHT_ATT,
                                    action_method=ActionMethod.CLICK, animation_time=1.03, is_combo=False)

        self.p1_h_p = HeavyAttAction(char_name="lucy", action_name="p1_heavy_att0", action_phase=1,
                                     action_type=ActionType.LIGHT_ATT,
                                     action_method=ActionMethod.HOLD, animation_time=-1.0, minimal_trigger_time=0.5,
                                     maximum_trigger_time=1.2)
        self.p1_h1 = HeavyAttAction(char_name="lucy", action_name="p1_heavy_att1", action_phase=1,
                                    action_type=ActionType.HEAVY_ATT,
                                    action_method=ActionMethod.HOLD, animation_time=-1.0, minimal_trigger_time=1.3,
                                    maximum_trigger_time=2.0, last_dmg_time=2.2)
        self.p1_h2 = HeavyAttAction(char_name="lucy", action_name="p1_heavy_att2", action_phase=1,
                                    action_type=ActionType.HEAVY_ATT,
                                    action_method=ActionMethod.HOLD, animation_time=-1.0, minimal_trigger_time=2.1,
                                    maximum_trigger_time=8.9, last_dmg_time=3.5)

        self.p1_heavy2_after_e1 = HeavyAttAction(char_name="lucy", action_name="p1_heavy_after_e1", action_phase=1,
                                                 minimal_trigger_time=0.76, w_light=1.8, w_e=1.2, w_r=1.2,
                                                 last_dmg_time=1.2)

        # todo 测试p1 e2 重击后 最后出伤时间  last_dmg_time w_e=time_in, w_r=time_in
        self.p1_heavy12_after_e2 = HeavyAttAction(char_name="lucy", action_name="p1_heavy_after_e2", action_phase=1,
                                                  minimal_trigger_time=2.5, w_light=1.9)
        # todo 测试p1 e2 重击后 最后出伤时间 last_dmg_time w_e=time_in, w_r=time_in
        self.p2_heavy12_after_p2_light3 = HeavyAttAction(char_name="lucy", action_name="p2_heavy12_after_p2_light3",
                                                         action_phase=2,
                                                         minimal_trigger_time=1.15, w_light=2.0)
        # todo 重击 后 最短普攻触发等待时间 确认是否为2.0
        # 2阶段 普攻4下后 重击
        self.p2_heavy12_after_p2_light4 = HeavyAttAction(char_name="lucy", action_name="p2_heavy12_after_p2_light4",
                                                         action_phase=2,
                                                         minimal_trigger_time=2, w_light=2.0, w_e=0.71, w_r=0.71,
                                                         last_dmg_time=0.71)

        self.p2_heavy12_after_ult = HeavyAttAction(char_name="lucy", action_name="p2_heavy12_after_ult",
                                                         action_phase=2,
                                                         minimal_trigger_time=2, w_light=2.0, w_e=0.71, w_r=0.71,
                                                         last_dmg_time=0.71)

        self.e1_p1_a = EAttAction(step=1, char_name="lucy", action_name="e_att", action_type=ActionType.E_ATT,
                                  action_phase=1,
                                  action_method=ActionMethod.SEND_KEY, animation_time=-1.0)
        self.e2_p1_a = EAttAction(step=1, char_name="lucy", action_name="e_att", action_type=ActionType.E_ATT,
                                  action_phase=1,
                                  action_method=ActionMethod.SEND_KEY, animation_time=-1.0)
        self.e_p2_a = EAttAction(step=1, char_name="lucy", action_name="e_att", action_type=ActionType.E_ATT,
                                 action_phase=2,
                                 action_method=ActionMethod.SEND_KEY, animation_time=-1.0, force_time_stop_time=2.5)

        self.r_a = RAttAction(step=1, char_name="lucy", action_name="r_att", action_type=ActionType.R_ATT,
                              action_method=ActionMethod.SEND_KEY, animation_time=-1.0, force_time_stop_time=3.4)
        self.f_break = FBreakAction(char_name="lucy", action_name="break", action_type=ActionType.BREAK,
                                    action_method=ActionMethod.SEND_KEY)
        self.switch_a = SwitchAction(step=1, char_name="lucy", action_name="switch", action_type=ActionType.SWITCH,
                                     action_method=ActionMethod.SEND_KEY, animation_time=-1.0)

        # 给所有行动添加 后续行动
        self.add_all_lucy_action_next_action_ready()

        self.light_p1_actions = [self.p1_l1, self.p1_l2, self.p1_l3, self.p1_l4]
        self.light_p2_actions = [self.p2_l1, self.p2_l2, self.p2_l3, self.p2_l4]
        self.heavy_actions = [self.p1_h_p, self.p1_h1, self.p1_h2]

        self.e_phase = 0
        self.last_p1_e1_cast_time = -1
        self.last_p1_e2_cast_time = -1
        self.last_enter_p2_time = -1
        self.last_forte_e_cast_time = -1
        self.last_p1_heavy2_cast_time = -1  # 最后一次阶段一 2段重击释放时间
        self.last_p2_forte_heavy2_cast_time = -1  # 最后一次阶段2 露西强化2段重击释放时间

        self.phase2_after_heavy2_no_action_back_to_phase1_time = 8 + 1  # 防止延迟出伤 多1秒
        self.light_att_animation_p1 = [0.18, 0.59, 0.97, 1.38]
        self.light_att_animation_p2 = [0.17, 0.82, 1.06, 1.03]
        self.last_light_att_index_p1 = -1  # 最后执行普攻段数 p1
        self.last_light_att_index_p2 = -1  # 最后执行普攻段数 p2

        # self.next_light_att_index_p1 = -1 #下一次普攻的段数 p1
        # self.next_light_att_index_p2 = -1 #下一次普攻的段数 p2
        # self.next_heavy_att_index_p1 = -1
        # self.next_heavy_att_index_p2 = -1
        # todo 切人情况需要测试
        self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed = 2.6  # 露西E2后能等待最多多久重击开始蓄力还能接上重击（必须在场）
        self.max_wait_time_p1_light = 2.6
        # todo 切露西进来 自动普攻2段后接普通时间，接重击时间
        self.ground_switch_in_wait_time_to_normal_att = 0.4
        self.ground_switch_in_wait_time_to_heavy_att = 0.4
        # todo 地面切露西进场 等待的最长可接重击1，2的时间
        self.ground_switch_in_max_wait_time_to_lance_heavy_att = 3.5


    def add_all_lucy_action_next_action_ready(self):
        # 露西普攻添加后续准备就绪行动
        init_next_action_ready_by_step(self.light_p1_actions)
        init_next_action_ready_by_step(self.light_p2_actions)

        #普攻添加重击后续



    def check_att_combo_time_valid(self, action_type: ActionType):
        # 轻攻击重击 确认是否在连招中
        if action_type in [ActionType.LIGHT_ATT, ActionType.HEAVY_ATT]:
            if action_type == ActionType.LIGHT_ATT and self.next_light_att_action_ready is not None and self.next_light_att_action_ready.step in [
                0, 4]:
                return False
            if action_type == ActionType.HEAVY_ATT and self.next_heavy_att_action_ready is not None and self.next_heavy_att_action_ready.step in [
                0]:
                return False
            if self.last_att_action_cast_time + self.cast_max_away_from_previous_action_time > time.time():
                return True
            else:
                return False
        else:
            return False

    def get_next_light_att_action(self):
        if self.next_light_att_action_ready is not None and self.last_att_action_cast_time + self.cast_max_away_from_previous_action_time > time.time():
            return self.next_light_att_action_ready
        else:
            # 连招中断 从头开打
            if self.e_phase in [0, 1, 2]:
                return self.light_p1_actions[0]
            else:
                return self.light_p2_actions[0]

    def lucy_light_default(self, end_step=-1, must_combo=False):
        next_light_action = self.get_next_light_att_action()
        if self.e_phase in [0, 1, 2]:
            phase = 1
            light_actions = self.light_p1_actions
            # light_att_animation = self.light_att_animation_p1
        else:
            phase = 2
            light_actions = self.light_p1_actions
        if end_step == -1 or end_step > len(light_actions):
            end_step = len(light_actions)

        next_light_action = self.get_next_light_att_action()
        if must_combo and not next_light_action.is_combo:
            return False

        if next_light_action.step > end_step:
            print("下一步普攻 大于传入最终普攻顺序", next_light_action, " end_step", end_step)
            return False
        step_now = next_light_action.step
        while step_now != end_step:
            # todo sleep

            next_light_action.do_action()

            # todo update

            step_now = step_now + 1
            next_light_action = get_next_action_from_list_by_step(step_now, light_actions)

        return True
