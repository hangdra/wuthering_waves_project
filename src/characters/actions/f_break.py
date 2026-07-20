# @Author  : liuha
# @Time    : 2026/7/12 20:21
# @File    : f_break.py


# @Author  : liuha
# @Time    : 2026/7/12 04:18
# @File    : e_action.py
# @Author  : liuha
# @Time    : 2026/7/12 04:18
# @File    : r_action.py


# @Author  : liuha
# @Time    : 2026/7/12 00:35
# @File    : heavy_action.py

from src.characters.actions.char_action import CharAction,ActionMethod,ActionType


class FBreakAction(CharAction):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.force_time_stop_time = 0.5 #强制时停


    # def next_action_move(self,action: CharAction,wait_time: float):
    #     self.wait_to_cast_next_action_dic[action.actionName] = wait_time


    # def next_action_max_wait_time(self,action: CharAction,wait_time: float):
    #     self.max_wait_time_to_cast_next_action[action.actionName] = wait_time

    def __str__(self):
        result = "FBreakAction("
        result = result + str(vars(self))
        return result + ")"

    def __repr__(self):
        return self.__str__()

# e_a = FBreakAction(char_name="lucy", action_name="break", action_type=ActionType.BREAK,
#                     action_method=ActionMethod.SEND_KEY)

