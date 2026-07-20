# @Author  : liuha
# @Time    : 2026/7/13 01:11
# @File    : all_lucy_combos.py
from src.characters.actions.heavy_att import HeavyAttAction
from src.characters.actions.light_att import LightAttAction
from src.characters.actions.e_skill import EAttAction
from src.characters.actions.r_skill import RAttAction
from src.characters.actions.switch_role import SwitchAction
from src.characters.actions.f_break import FBreakAction
from src.characters.actions.char_action import CharAction, ActionMethod, ActionType

p1_l1 = LightAttAction(step=1, char_name="lucy", action_name="p1_light_att1", action_phase=1,
                       action_type=ActionType.LIGHT_ATT,
                       action_method=ActionMethod.CLICK, animation_time=0.18, w_light=0.18,
                       next_light_att_max_wait_time=1.8, is_combo=False)
p1_l2 = LightAttAction(step=2, char_name="lucy", action_name="p1_light_att2", action_phase=1,
                       action_type=ActionType.LIGHT_ATT,
                       action_method=ActionMethod.CLICK, animation_time=0.59, w_light=0.59,
                       next_light_att_max_wait_time=1.3, is_combo=True)
p1_l3 = LightAttAction(step=3, char_name="lucy", action_name="p1_light_att3", action_phase=1,
                       action_type=ActionType.LIGHT_ATT,
                       action_method=ActionMethod.CLICK, animation_time=0.97, w_light=0.97,
                       next_light_att_max_wait_time=1.9, is_combo=True)
p1_l4 = LightAttAction(step=4, char_name="lucy", action_name="p1_light_att4", action_phase=1,
                       action_type=ActionType.LIGHT_ATT,
                       action_method=ActionMethod.CLICK, animation_time=1.38, w_light=1.38, is_combo=False)

p2_l1 = LightAttAction(step=1, char_name="lucy", action_name="p2_light_att1", action_phase=2,
                       action_type=ActionType.LIGHT_ATT,
                       action_method=ActionMethod.CLICK, animation_time=0.17,
                       next_light_att_max_wait_time=1.3, is_combo=False)
p2_l2 = LightAttAction(step=2, char_name="lucy", action_name="p2_light_att2", action_phase=2,
                       action_type=ActionType.LIGHT_ATT,
                       action_method=ActionMethod.CLICK, animation_time=0.82,
                       next_light_att_max_wait_time=2.1, is_combo=True)
p2_l3 = LightAttAction(step=3, char_name="lucy", action_name="p2_light_att3", action_phase=2,
                       action_type=ActionType.LIGHT_ATT,
                       action_method=ActionMethod.CLICK, animation_time=1.06,
                       next_light_att_max_wait_time=3.1, is_combo=False)
p2_l4 = LightAttAction(step=4, char_name="lucy", action_name="p2_light_att4", action_phase=2,
                       action_type=ActionType.LIGHT_ATT,
                       action_method=ActionMethod.CLICK, animation_time=1.03, is_combo=False)

p1_h_p = HeavyAttAction(char_name="lucy", action_name="p1_heavy_att0", action_phase=1,
                        action_type=ActionType.LIGHT_ATT,
                        action_method=ActionMethod.HOLD, animation_time=-1.0, minimal_trigger_time=0.5,
                        maximum_trigger_time=1.2)
p1_h1 = HeavyAttAction(char_name="lucy", action_name="p1_heavy_att1", action_phase=1,
                       action_type=ActionType.HEAVY_ATT,
                       action_method=ActionMethod.HOLD, animation_time=-1.0, minimal_trigger_time=1.3,
                       maximum_trigger_time=2.0, last_dmg_time=2.2)
p1_h2 = HeavyAttAction(char_name="lucy", action_name="p1_heavy_att2", action_phase=1,
                       action_type=ActionType.HEAVY_ATT,
                       action_method=ActionMethod.HOLD, animation_time=-1.0, minimal_trigger_time=2.1,
                       maximum_trigger_time=8.9, last_dmg_time=3.5)

# done 露西p1 e1 后重2
p1_heavy2_after_e1 = HeavyAttAction(char_name="lucy", action_name="p1_heavy_after_e1", action_phase=1,
                                    minimal_trigger_time=0.76, w_light=1.8, w_e=1.2, w_r=1.2,
                                    last_dmg_time=1.2)

# todo 测试p1 e2 重击后 最后出伤时间  last_dmg_time w_e=time_in, w_r=time_in
p1_heavy12_after_e2 = HeavyAttAction(char_name="lucy", action_name="p1_heavy_after_e2", action_phase=1,
                                     minimal_trigger_time=2.5, w_light=1.9)
# todo 测试p2 3普攻后重击  重击后 最后出伤时间 last_dmg_time w_e=time_in, w_r=time_in
p2_heavy12_after_p2_light3 = HeavyAttAction(char_name="lucy", action_name="p2_heavy12_after_p2_light3",
                                            action_phase=2,
                                            minimal_trigger_time=1.15, w_light=2.0)
# todo 测试p2 4普攻后重击 重击后 最短普攻触发等待时间 确认是否为2.0
# 2阶段 普攻4下后 重击
p2_heavy12_after_p2_light4 = HeavyAttAction(char_name="lucy", action_name="p2_heavy12_after_p2_light4",
                                            action_phase=2,
                                            minimal_trigger_time=2, w_light=2.0, w_e=0.71, w_r=0.71,
                                            last_dmg_time=0.71)

e1_p1_a = EAttAction(step=1, char_name="lucy", action_name="e_att", action_type=ActionType.E_ATT,
                     action_phase=1,
                     action_method=ActionMethod.SEND_KEY, animation_time=-1.0)
e2_p1_a = EAttAction(step=1, char_name="lucy", action_name="e_att", action_type=ActionType.E_ATT,
                     action_phase=1,
                     action_method=ActionMethod.SEND_KEY, animation_time=-1.0)
e_p2_a = EAttAction(step=1, char_name="lucy", action_name="e_att", action_type=ActionType.E_ATT,
                    action_phase=2,
                    action_method=ActionMethod.SEND_KEY, animation_time=-1.0, force_time_stop_time=2.5)

r_a = RAttAction(step=1, char_name="lucy", action_name="r_att", action_type=ActionType.R_ATT,
                 action_method=ActionMethod.SEND_KEY, animation_time=-1.0, force_time_stop_time=3.4)
f_break = FBreakAction(char_name="lucy", action_name="break", action_type=ActionType.BREAK,
                       action_method=ActionMethod.SEND_KEY)
switch_a = SwitchAction(step=1, char_name="lucy", action_name="switch", action_type=ActionType.SWITCH,
                        action_method=ActionMethod.SEND_KEY, animation_time=-1.0)

light_p1_actions = [p1_l1, p1_l2, p1_l3, p1_l4]
light_p2_actions = [p2_l1, p2_l2, p2_l3, p2_l4]
heavy_actions = [p1_h_p, p1_h1, p1_h2]

all_actions_list = [p1_l1, p1_l2, p1_l3, p1_l4, p2_l1, p2_l2, p2_l3, p2_l4, p1_h_p, p1_h1, p1_h2, p1_heavy2_after_e1,
                    p1_heavy12_after_e2, p2_heavy12_after_p2_light3, p2_heavy12_after_p2_light4]


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


def add_all_lucy_action_next_action_ready():
    # 露西普攻添加后续准备就绪行动
    init_next_action_ready_by_step(light_p1_actions)
    init_next_action_ready_by_step(light_p2_actions)


add_all_lucy_action_next_action_ready()
