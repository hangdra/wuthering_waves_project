# @Author  : liuha
# @Time    : 2026/7/12 00:35
# @File    : heavy_action.py

from src.characters.actions.char_action import CharAction,ActionMethod,ActionType

class HeavyAttAction(CharAction):

    def __init__(self,  minimal_trigger_time:float, maximum_trigger_time:float=-1.0,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minimal_trigger_time = minimal_trigger_time
        self.maximum_trigger_time = maximum_trigger_time

        self.wait_to_cast_next_action_dic = {}


    def next_action_move(self,action: CharAction,wait_time: float):
        self.wait_to_cast_next_action_dic[action.actionName] = wait_time


    # def next_action_max_wait_time(self,action: CharAction,wait_time: float):
    #     self.max_wait_time_to_cast_next_action[action.actionName] = wait_time

    def __str__(self):
        result = "HeavyAttAction("
        result = result + str(vars(self))
        return result + ")"

    def __repr__(self):
        return self.__str__()

p1_h_p = HeavyAttAction(char_name="lucy", action_name="p1_heavy_att0", action_type=ActionType.LIGHT_ATT,
                    action_method=ActionMethod.HOLD, animation_time=-1.0,minimal_trigger_time=0.5,maximum_trigger_time=1.2)
p1_h1 = HeavyAttAction( char_name="lucy", action_name="p1_heavy_att1", action_type=ActionType.HEAVY_ATT,
                    action_method=ActionMethod.HOLD, animation_time=-1.0,minimal_trigger_time=1.3,maximum_trigger_time=2.0,last_dmg_time=2.2)
p1_h2 = HeavyAttAction(char_name="lucy", action_name="p1_heavy_att2", action_type=ActionType.HEAVY_ATT,
                    action_method=ActionMethod.HOLD, animation_time=-1.0,minimal_trigger_time=2.1,maximum_trigger_time=8.9,last_dmg_time=3.5)

# p2_h1 = HeavyAttAction(step=1, char_name="lucy", action_name="p2_heavy_att1", action_type=ActionType.HEAVY_ATT,
#                     action_method=ActionMethod.HOLD, animation_time=-1.0,minimal_trigger_time=1.8)
# p2_h2 = HeavyAttAction(step=2, char_name="lucy", action_name="p2_heavy_att2", action_type=ActionType.HEAVY_ATT,
#                     action_method=ActionMethod.HOLD, animation_time=-1.0,minimal_trigger_time=1.3)
