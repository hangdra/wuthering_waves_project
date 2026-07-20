# @Author  : liuha
# @Time    : 2026/7/12 17:38
# @File    : switch_action.py




from src.characters.actions.char_action import CharAction,ActionMethod,ActionType


class SwitchAction(CharAction):

    def __init__(self, step: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = step


    def next_action_move(self,action: CharAction,wait_time: float):
        self.wait_to_cast_next_action_dic[action.actionName] = wait_time


    # def next_action_max_wait_time(self,action: CharAction,wait_time: float):
    #     self.max_wait_time_to_cast_next_action[action.actionName] = wait_time

    def __str__(self):
        result = "SwitchAction("
        result = result + str(vars(self))
        return result + ")"

    def __repr__(self):
        return self.__str__()

switch_a = SwitchAction(step=1, char_name="lucy", action_name="switch", action_type=ActionType.SWITCH,
                    action_method=ActionMethod.SEND_KEY, animation_time=-1.0)

