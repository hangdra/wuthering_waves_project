# @Author  : liuha
# @Time    : 2026/7/12 04:18
# @File    : r_action.py


# @Author  : liuha
# @Time    : 2026/7/12 00:35
# @File    : heavy_action.py

from src.characters.actions.char_action import CharAction,ActionMethod,ActionType
class RAttAction(CharAction):

    def __init__(self, step: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step
        self.wait_to_cast_next_action_dic = {}


    def next_action_move(self,action: CharAction,wait_time: float):
        self.wait_to_cast_next_action_dic[action.actionName] = wait_time


    # def next_action_max_wait_time(self,action: CharAction,wait_time: float):
    #     self.max_wait_time_to_cast_next_action[action.actionName] = wait_time

    def __str__(self):
        result = "RAttAction("
        result = result + str(vars(self))
        return result + ")"

    def __repr__(self):
        return self.__str__()

r_a = RAttAction(step=1, char_name="lucy", action_name="r_att", action_type=ActionType.R_ATT,
                    action_method=ActionMethod.SEND_KEY, animation_time=-1.0)

print(r_a)