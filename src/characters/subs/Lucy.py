from src.characters.base_char import Character
from src.characters.actions.char_action import ActionType
import time


class Lucy(Character):

    def __init__(self, *args, **kwargs):
        super().__init__()

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

    def lucy_heavy2_after_light3(self, index=0, learning_rate=0.0):
        # fixed 10/10
        duration_time = 1.15  # +index*learning_rate
        # if learning_rate>0.0:
        #     print("lucy_heavy2_after_light3  duration_time", duration_time)
        print(self.w_light)
        self.try_sleep_before_action(ActionType.HEAVY_ATT)
        self.heavy_att(duration_time)
        # fixed 18/20
        w_light = 2.0  # +index*learning_rate
        self.update_wait_time(w_light=w_light)
        # if learning_rate>0.0:
        #     print("w_light", w_light)
        # print("w_light=", w_light)

    def lucy_p1_light_att(self, start_index=0, end_index=-1, test_index=0, test_learning_rate=0.0):
        # 10/10 index 0
        # 10/10 index 1
        # 10/10 index 2
        # 10/10 index 3   lucy.test_light_all(end=5,index=i,test_learning_rate=-0.00)
        animation_duration = self.light_att_animation_p1
        # change_index = end_index - 2 if (end_index - 2) < len(animation_duration) else len(animation_duration)
        # animation_duration[change_index] = animation_duration[change_index] + test_index * test_learning_rate
        if test_learning_rate != 0.0:
            print("end_index -1 duration", animation_duration[end_index - 2])
        if end_index == -1 or end_index > len(animation_duration):
            end_index = len(animation_duration)
        if start_index > len(animation_duration):
            start_index = len(animation_duration)
        if end_index < start_index:
            end_index = start_index
        if start_index > end_index:
            start_index = end_index
        print("light att start_index", start_index, "end_index", end_index)
        for i in range(start_index, end_index):
            # print("____________i",i)
            self.try_light_att(w_light=animation_duration[i])
            self.last_light_att_index_p1 = i

    def check_combo_time_valid(self):
        return time.time() - self.last_action_time < self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed

    def lucy_light_default(self, end_index=-1, must_combo=False):
        """
        :param end_index:
        :param must_combo:  True 只执行初始 普攻计数不为-1的行为，False 所有行为都支持 并且普攻
        :return:
        """
        if self.e_phase in [0, 1, 2]:
            phase = 1
            light_att_animation = self.light_att_animation_p1
        else:
            phase = 2
            light_att_animation = self.light_att_animation_p2
        if end_index == -1 or end_index > len(light_att_animation):
            end_index = len(light_att_animation)

        if must_combo:
            if phase == 1:
                if self.next_light_step_p1 in [0,4]:
                    return False

        start_index = 0
        if self.last_action_type in [ActionType.LIGHT_ATT, ActionType.E_ATT,
                                     ActionType.SWITCH] and self.check_combo_time_valid():
            if phase == 1:
                start_index = self.last_light_att_index_p1 + 1
            else:
                start_index = self.last_light_att_index_p2 + 1
            if start_index >= len(light_att_animation):
                start_index = 0

        for i in range(start_index, end_index):
            self.try_light_att(w_light=light_att_animation[i])
            if phase == 1:
                self.last_light_att_index_p1 = i
            else:
                self.last_light_att_index_p2 = i

        return True

    def test_random_light_att(self, index=0):
        # fixed 10/10
        # le1 = index
        # print("test_random_light_att", le1)
        # self.lucy_normal_att(end_index=le1)
        # self.lucy_normal_att(start_index=le1)
        # self.lucy_normal_att()
        le1 = index
        print("test_random_light_att", le1)
        self.lucy_p1_light_att(end_index=le1)
        self.lucy_p1_light_att(start_index=le1)
        self.lucy_p1_light_att()

    # def get_animation_duration_list(self,duration_list):

    def test_light_all(self, end=-1, index=0, test_learning_rate=0.0):
        # self.lucy_p1_light_att(end_index=end, test_index=index,test_learning_rate=test_learning_rate)
        self.lucy_p1_light_att(end_index=4)
        self.lucy_p1_light_att(end_index=4)

    def lucy_heavy12_for_switch_in_or_light2(self, index=0, learning_rate=0.0):
        # fixed 10/10 lucy.test_light2_and_heavy(index=i,test_learning_rate=0)
        duration_time = 1.45 + index * learning_rate
        if learning_rate > 0.0:
            print("lucy_heavy2_att_just_after_light3  duration_time", duration_time)
        if not self.last_action_type == ActionType.LIGHT_ATT:
            print("last action type", self.last_action_type)
        self.try_sleep_before_action(ActionType.HEAVY_ATT)
        self.heavy_att(duration_time)
        w_light = 2.0  # +index*learning_rate
        self.update_wait_time(w_light=w_light)

    def test_light2_and_heavy(self, index=0, test_learning_rate=0.0):
        self.lucy_p1_light_att(end_index=1)
        self.lucy_p1_light_att(start_index=1, end_index=2)
        # checked duration_time and w_light
        self.lucy_heavy_default(duration_time=1.5, w_light=2.0)

    def test_heavy2_for_switch_in(self, index=0, test_learning_rate=0.0):
        # 丽贝卡变奏入场
        self.lucy_p1_light_att(end_index=1)

        # real happend
        self.lucy_p1_light_att(start_index=1, end_index=2)

    # def lucy_heavy_p1_default(self,duration_time,wait_time = 0.0):
    #     self.try_sleep_before_action(ActionType.HEAVY_ATT)
    #     self.heavy_att(duration_time)
    #     # w_light = 2.0  # +index*learning_rate
    #     self.update_wait_time(w_light=wait_time)

    def reset_data(self):
        # 退出压缩算法状态
        if self.e_phase == 3:
            self.e_phase = 0
        # 一定要设置为None 要么 第二次进入压缩哦阶段， 任何攻击都会触发 此函数
        self.try_sleep_call_back_after_sleep_function = None

    def check_data_before_each_action_sleep(self):
        # print("in here function[check_data_before_each_action_sleep]")
        if self.e_phase != 3:
            # 大招改变状态
            self.reset_data()
            return
        # 如果阶段2 打出强化重击后8s内没有攻击动作，则退回阶段一
        if self.last_action_time - self.last_p2_forte_heavy2_cast_time > self.phase2_after_heavy2_no_action_back_to_phase1_time:
            print(" self.e_phase", self.e_phase, "reset to 0")
            self.reset_data()
        else:
            # 如果8s 内有动作，更新阶段2重击最后动作时间
            self.last_p2_forte_heavy2_cast_time = self.last_action_time

    def lucy_heavy_default(self, duration_time, w_light=0.0, w_heavy=0.0, w_e=0.0, w_r=0.0, w_switch=0.0):
        self.try_sleep_before_action(ActionType.HEAVY_ATT)
        self.heavy_att(duration_time)
        if self.e_phase == 3:
            self.try_sleep_call_back_after_sleep_function = self.check_data_before_each_action_sleep
            self.last_p2_forte_heavy2_cast_time = time.time()
        if self.e_phase in [0, 1, 2]:
            self.last_p1_heavy2_cast_time = time.time()
        # w_light = 2.0  # +index*learning_rate
        self.update_wait_time(w_light=w_light, w_heavy=w_heavy, w_e=w_e, w_r=w_r, w_switch=w_switch)

    def lucy_ult(self):
        self.try_sleep_before_action(ActionType.R_ATT)
        self.continuous_press_some_key("r", 0.1)
        # 释放共鸣解放 重置死锁cd
        self.last_forte_e_cast_time = -1
        # todo 再次判定 大招是否释放成功再睡觉
        # todo 若大招放成功 变灰
        self.reset_data()
        time.sleep(3.4)
        self.heavy_att(1.1)
        # todo 确认等待时间 也可以先放着 （反正预输入重击）
        self.update_wait_time()

    def lucy_cast_e_p2(self):
        # done
        self.try_sleep_before_action(ActionType.E_ATT)
        self.continuous_press_some_key("e", 0.1)
        self.last_forte_e_cast_time = time.time()
        # todo self.last_enter_p2_time 有啥用？
        if self.e_phase == 2:
            self.last_enter_p2_time = self.last_forte_e_cast_time
        self.e_phase = 3
        # 阶段2 e技能 时停且不可切人
        time.sleep(2.5)
        self.update_wait_time(next_light_step_p2=2)

    def lucy_cast_e_p1(self, wait_time=0.0):
        # print("_________________________lucy_cast_e_p1 self.e_phase", self.e_phase)
        # todo 检查e是否可以释放 是否阶段1
        self.try_sleep_before_action(ActionType.E_ATT)
        self.continuous_press_some_key("e", 0.1)
        if self.e_phase == 0:
            w_light = 0.7
            w_heavy = 0.0
            w_e = 0.6  # check
            w_r = 0.6
            next_light_p1 = 2
            next_heavy_p1 = 2
            self.e_phase = 1
            self.last_p1_e1_cast_time = time.time()
        elif self.e_phase == 1:
            w_light = 0.0
            w_heavy = 0.0
            w_e = 0.0
            w_r = 0.0
            next_light_p1 = 2
            next_heavy_p1 = 0
            self.e_phase = 2
            self.last_p1_e2_cast_time = time.time()
        else:
            raise Exception("不支持的 self.e_phase" + str(self.e_phase))
        # todo  e_phase == 1
        self.update_wait_time(w_light=w_light, w_heavy=w_heavy, w_e=w_e, w_r=w_r, next_light_step_p1=next_light_p1,
                              next_heavy_step_p1=next_heavy_p1)

    def lucy_p2_light_att(self, start_index=0, end_index=-1, test_index=0, test_learning_rate=0.0):
        # 10/10 index 0 lucy.lucy_p2_light_att(end_index=2,test_index=i,test_learning_rate=0.01)
        # 10/10 index 1  lucy.lucy_p2_light_att(end_index=3,test_index=i,test_learning_rate=0.01)
        # 10/10 index 2 lucy.lucy_p2_light_att(end_index=4,test_index=i,test_learning_rate=0.01)
        # 10/10 index 3  lucy.lucy_p2_light_att(end_index=5,test_index=i,test_learning_rate=0)
        #               lucy.lucy_p2_light_att(end_index=4)
        animation_duration = [0.17, 0.82, 1.06, 1.03]
        change_index = end_index - 2 if (end_index - 2) < len(animation_duration) else len(animation_duration)
        animation_duration[change_index] = animation_duration[change_index] + test_index * test_learning_rate
        if test_learning_rate != 0.0:
            print("end_index -1 duration", animation_duration[end_index - 2])
        if end_index == -1 or end_index > len(animation_duration):
            end_index = len(animation_duration)
        if start_index > len(animation_duration):
            start_index = len(animation_duration)
        if end_index < start_index:
            end_index = start_index
        if start_index > end_index:
            start_index = end_index
        # print("start_index", start_index, "end_index", end_index)
        for i in range(start_index, end_index):
            # print("____________i", i)
            self.try_light_att(w_light=animation_duration[i])

    def test_ult_and_heavy2(self, pre_input_heavy2_duration_time=1.4):
        # 测试露西大招重击
        self.lucy_ult()
        self.heavy_att(pre_input_heavy2_duration_time)

    # def test_lucy_p1_e1_ult_not_ready_rotation(self,duration_time):
    #     self.lucy_cast_e_p1()
    #     self.lucy_heavy2_only(duration_time=duration_time)

    # def lucy_p2_heavy12(self,test_wait_time=0.0):
    #     #done
    #     self.try_sleep_before_action(ActionType.HEAVY_ATT)
    #     self.heavy_att(2)
    #     #等待2段重击出伤后可以使用e或者r
    #     #done w_light
    #     # self.update_wait_time(w_light=0.5,w_e=0.68,w_r=0.68)
    #     self.update_wait_time(w_light=0.71, w_e=0.71, w_r=0.71)

    def test_lucy_p2_light4_and_heavy2_and_e_and_light4(self, wait_time=0.0):
        """
        压缩阶段普攻1-4 接重击1，2 接普攻1-4
        :param wait_time:
        :return:
        """
        # done test code
        # time_d = 0.68#+0.05*i
        # lucy.test_lucy_p2_light4_and_heavy2_and_e_and_light4(time_d) #2.2ok
        # print("露西进入阶段2 普攻后重击 等待重击出伤 后马上大招 等待时间",time_d)
        # time_here = time.time()
        # while time.time() -time_here <10:
        #     lucy.lucy_p2_light_att(end_index=4)
        self.lucy_p2_light4_and_heavy2()
        # self.lucy_p2_light_att(end_index=4)
        # self.lucy_heavy_default(duration_time=2,w_light=0.71, w_e=0.71, w_r=0.71)
        # self.lucy_p2_heavy12(wait_time)
        self.continuous_press_some_key("e", 0.1)
        self.lucy_p2_light_att(end_index=4)

    # def lucy_heavy_after_ult(self,wait_time=0.0):
    #     self.try_sleep_before_action(ActionType.HEAVY_ATT)
    #     self.heavy_att(1.4)
    #     self.update_wait_time(w_light=2.0, w_e=wait_time, w_r=0.0)
    def lucy_p2_light4_and_heavy2(self):
        # 露西压缩 阶段普攻4下然后重击
        self.lucy_p2_light_att(end_index=4)
        print(" lucy_p2_light4_and_heavy2 普攻4下结束")
        # w_light=0.71, w_e=0.71, w_r=0.71 checked
        self.lucy_heavy_default(duration_time=2, w_light=0.71, w_e=0.71, w_r=0.71)

    def lucy_ult_and_pre_heavy2(self):
        # todo  前置确认，大招就绪？
        self.lucy_ult()
        self.lucy_heavy_default(duration_time=1.4, w_light=2.0, w_e=1.6)

    def lucy_quick_p2_and_ult(self, wait_time=2.0):
        # todo 确认是否e_forte_ready
        self.lucy_cast_e_p2()
        # todo  前置确认，大招就绪？
        self.lucy_p2_light4_and_heavy2()
        # todo  如果重击没满 或者 大招没满，一直普攻
        self.lucy_ult_and_pre_heavy2()
        # self.lucy_p2_light_att(end_index=4)
        # self.lucy_p2_heavy12()
        # self.lucy_heavy_after_ult(wait_time)

    def build_ult(self):
        # self.lucy_cast_e_p2()
        # self.lucy_cast_e_p1()
        if self.e_phase == 0:
            self.lucy_cast_e_p1()
            self.lucy_cast_e_p1()
        elif self.e_phase == 1:
            self.lucy_cast_e_p1()
        for i in range(13):
            self.lucy_p1_light3_heavy2()
            # self.lucy_p1_light_att()

    def back_to_p1_e0(self):
        if self.e_phase in [1, 2]:
            print("in here ", self.e_phase)
            for i in range(7 - self.e_phase * 3):
                self.lucy_p1_light3_heavy2()
            self.lucy_cast_e_p2()
            print(" e p2 casted~~~~~~~~~~~~~~~~~~~~~~~~~~")
            self.lucy_p2_light4_and_heavy2()
            time.sleep(self.phase2_after_heavy2_no_action_back_to_phase1_time)
        elif self.e_phase == 3:
            print("in here ", self.e_phase)
            self.lucy_p2_light4_and_heavy2()
            time.sleep(self.phase2_after_heavy2_no_action_back_to_phase1_time)
        print("back to p1 over ~~~")

    def lucy_e1_light2_4(self, light_end_index=4):
        """ 露西放e1 并且衔接普攻2-4"""
        if self.e_phase == 0:
            self.lucy_cast_e_p1()
            self.lucy_p1_light_att(start_index=1, end_index=light_end_index)

    def lucy_e1_e2(self):
        if self.e_phase == 0:
            self.lucy_cast_e_p1()
            self.lucy_cast_e_p1()

    def lucy_e1_heavy2(self, wait_time=0.0):
        """
        露西 E1 接重2
        :param wait_time:
        :return:
        """
        self.lucy_cast_e_p1()
        # done 测定各个攻击行为等待时间
        # w_light = 1.8 done
        # w_e = 1.2 done 出伤之后立马接2段e
        self.try_heavy2()
        # self.lucy_heavy_default(duration_time=0.76, w_light=1.8, w_e=1.2, w_r=1.2)

    def lucy_e2_heavy2(self, time_in=0.0):
        """
        露西 E2 接重击12
        不推荐使用 露西E2后应该直接切人
        :param time_in:
        :return:
        """
        self.lucy_cast_e_p1()
        # 测试E2 后多久能接上重击的时间 求最大
        # todo 测定各个攻击行为等待时间
        self.try_heavy2(time_in=time_in)

    def lucy_p1_light3_heavy2(self, time_in=0.0):
        # todo 循环有问题 单独循环没问题 接E1 或者 E2都不太行
        self.lucy_p1_light_att(end_index=3)
        self.lucy_heavy_default(duration_time=1.15, w_light=2.0, w_e=time_in, w_r=time_in)

    def try_heavy2(self, time_in=0.0):
        # todo
        if self.last_action_type == ActionType.E_ATT:
            if self.e_phase == 2:
                if time.time() < self.last_p1_e2_cast_time + self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed:
                    # duration_time=2.5 done 2.4 is ok too
                    self.lucy_heavy_default(duration_time=2.5, w_light=1.9, w_e=time_in, w_r=time_in)
            elif self.e_phase == 1:
                if time.time() < self.last_p1_e1_cast_time + self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed:
                    self.lucy_heavy_default(duration_time=0.76, w_light=1.8, w_e=1.2, w_r=1.2)

        if self.last_action_type == ActionType.LIGHT_ATT:
            if self.last_action_time + self.e2_max_wait_time_heavy_charge_if_lucy_is_on_the_filed > time.time():
                if self.e_phase in [0, 1, 2]:
                    # todo 如果有rebecca buff 从普攻1，2，开始长按重击 不要普攻3
                    if self.prevent_switch_dead_time > time.time():
                        if self.last_light_att_index_p1 == 0:
                            self.lucy_light_default(end_index=3)
                    else:
                        # 阶段1普攻3+重击
                        self.lucy_light_default(end_index=3)
                        self.lucy_heavy_default(duration_time=1.15, w_light=2.0)
                else:
                    # 阶段2普攻4+重击
                    self.lucy_light_default(end_index=4)
                    self.lucy_heavy_default(duration_time=2, w_light=0.71, w_e=0.71, w_r=0.71)

    # def lucy_p2_light4_and_heavy2(self):
    #     # 露西压缩 阶段普攻4下然后重击
    #     self.lucy_p2_light_att(end_index=4)
    #     print(" lucy_p2_light4_and_heavy2 普攻4下结束")
    #     # w_light=0.71, w_e=0.71, w_r=0.71 checked
    #     self.lucy_heavy_default(duration_time=2, w_light=0.71, w_e=0.71, w_r=0.71)


