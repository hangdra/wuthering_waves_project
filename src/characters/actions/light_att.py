# @Author  : liuha
# @Time    : 2026/7/12 00:38
# @File    : light_action].py

from src.characters.actions.char_action import CharAction,ActionMethod,ActionType
import time

class LightAttAction(CharAction):

    def __init__(self, step: int, next_light_att_max_wait_time:float=0.0,click_time_default:int=2,click_time_interval:float=0.01, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step
        self.click_time_default = click_time_default #默认点击次数
        self.click_time_interval = click_time_interval #默认点击间隔时间
        self.next_light_att_max_wait_time = next_light_att_max_wait_time
        # self.cast_max_away_from_previous_action =
        self.wait_to_cast_next_action_dic = {}


    def next_action_move(self,action: CharAction,wait_time: float):
        self.wait_to_cast_next_action_dic[action.actionName] = wait_time


    # def next_action_max_wait_time(self,action: CharAction,wait_time: float):
    #     self.max_wait_time_to_cast_next_action[action.actionName] = wait_time

    def __str__(self):
        result = "LightAttAction("
        result = result + str(vars(self))
        return result + ")"

    def __repr__(self):
        return self.__str__()

    def do_action(self):
        #todo sleep before att
        super().do_action()
        if self.actionMethod == ActionMethod.CLICK:
            for i in range(self.click_time_default):
                self.my_input_sim.click()
                if self.click_time_default > 1 and i < self.click_time_default:
                    time.sleep(self.click_time_interval)
        if self.force_time_stop_time > 0:
            time.sleep(self.force_time_stop_time)

    def sleep_before_next_action(self,last_action: CharAction=None):
        if last_action is not None:
            sleep_time = last_action.w_light




    # def sleep_before_action(self,last_action: CharAction):
    #

p1_l1 = LightAttAction(step=1, char_name="lucy", action_name="p1_light_att1", action_phase=1,
                                    action_type=ActionType.LIGHT_ATT,
                                    action_method=ActionMethod.CLICK, animation_time=0.18, w_light=0.18,
                                    next_light_att_max_wait_time=1.8, is_combo=False)
print(p1_l1)