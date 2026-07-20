# @Author  : liuha
# @Time    : 2026/7/12 00:41
# @File    : lucy_test.py
import win32con
import win32gui
import win32ui, win32api
import time
from time import sleep
import threading
from src.characters.subs.Lucy import Lucy






def main():
    # print('auto_action scaffold: run perception -> planner -> executor')
    # list_window_names()
    window_name = "鸣潮  "
    hwnd_id = win32gui.FindWindow(None, window_name)
    print(window_name, hwnd_id)

    lucy = Lucy()
    # #冷启动
    lucy.my_input_sim.send_key("SHIFT")
    time.sleep(1)
    loop_time = 10
    loop_sleep = 6
    first_time_in = True
    key_shift = "SHIFT"
    key_e = "e"
    key_r = "r"
    # todo 重击之后 接e3
    for i in range(3, 4):
        print(i)
    try:
        for i in range(loop_time):
            # if first_time_in:
            #     first_time_in = False
            #     lucy.e_phase = 0
            # lucy.back_to_p1_e0()

           #  from tests.heavy_action import p1_h_p,p1_h1,p1_h2
           #  from tests.light_action import p1_l1, p1_l2, p1_l3,p1_l4
           # # 测试露西重击 最后出伤时间
           #  target_action = p1_l1
           #  time_in = target_action.w_light
           #  delay_time = time_in+i*0.1
           #  t = threading.Thread(target=lucy.my_input_sim.task_send_key, args=(delay_time,key_shift,))
           #  t.start()
           #  # print("heavy_ start time ",time.time())
           #  # time_in = 0.3#+0.1*i
           #  print("duration",time_in," dodge time: ", delay_time)
            # time.sleep(time_in)
            # lucy.send_key("SHIFT")


            lucy.lucy_p1_light3_heavy2()
            lucy.lucy_e1_heavy2()

            # 测试露西e1 重击 e2重击 出伤之后 e3  需要等待时间
            # lucy.lucy_p1_light3_heavy2()
            # lucy.lucy_e1_heavy2()
            # duration = 1.3 + 0.2 * i  # 1.0 失败 1.9 ok
            # print("__________________________duration", duration)
            # lucy.lucy_e2_heavy2(time_in=duration)
            # print("e2 should be cast now")
            # lucy.lucy_cast_e_p2()
            # print(" done test+++++++++++++++++++++++++++++++++++++++++++++++++")
            # break

            # lucy.build_ult()
            #
            # # 测试露西进入二阶段并直接进入大招流程并且大招后预输入重击
            # # todo 预输入重击后，测试 普攻合e 技能可以释放时机。
            # wait_time = 1.6
            # print("----------------------------------wait_time", wait_time)
            # lucy.lucy_quick_p2_and_ult(wait_time = wait_time)
            # lucy.lucy_cast_e_p1()
            # # lucy.lucy_p2_light_att(end_index=4)
            # # lucy.test_ult_and_heavy2(pre_input_heavy2_duration_time=1.4)#成功次数1
            # # break
            # #测试露西 p1 or p2 大招 预输入重击 #todo

            # # # 测试露西 阶段1 e1 接重2 #todo
            #
            # lucy.lucy_e2_heavy2() # 2.4 不够   2.6多了
            # break
            # 测试露西 阶段1 e2 接重2 #todo

            # 测试p1普攻间隔 done
            # target_step = 4
            # # self.light_att_animation_p1 = [0.18, 0.59, 0.97, 1.38]
            # # self.light_att_animation_p2 = [0.17, 0.82, 1.06, 1.03]
            # lucy.lucy_p2_light_att(end_index=target_step - 1)
            # # l1-l2 1.8 l2-l3 1.3
            # time_sleep = 3.1  # -i*0.1
            # print("_____________________time_sleep", time_sleep)
            # time.sleep(time_sleep)
            # lucy.lucy_p2_light_att(start_index=target_step - 1, end_index=target_step)

            # 测试露西e1 重击 e2重击 之后普攻需要等待时间 done
            # duration = 1.9 + 0.2 * i  # 1.0 失败 1.9 ok
            # lucy.lucy_e1_heavy2()
            # print("__________________________duration", duration)
            # lucy.lucy_e2_heavy2(time_in=duration)
            # lucy.lucy_p1_light_att()
            # print(" done test+++++++++++++++++++++++++++++++++++++++++++++++++")

            # 测试露西e1 重击 e2重击 e2后最大等待时间能接上 重击 done
            # time_wait = 2.6  # 2ok 3失败 2.5 ok 2.8 失败
            # lucy.lucy_e1_heavy2()
            # print("__________________________time_wait", time_wait)
            # lucy.lucy_e2_heavy2(wait_time=time_wait)
            # print(" done test")

            # done 测试露西e1 普攻
            # time_wait = 0.7  # + 0.05*i #0.6不行 0.7ok
            # print("__________________________time_wait", time_wait)
            # lucy.lucy_cast_e_p1(wait_time=time_wait)
            # lucy.lucy_p1_light_att(start_index=1, end_index=4)
            # print(" done test")

            # done 测试露西e1 e2连放时间 done
            # time_wait = 0.6  # + 0.2*i #0.3 no 0.6ok
            # print("time_wait", time_wait)
            # lucy.lucy_cast_e_p1(wait_time=time_wait)
            # lucy.lucy_cast_e_p1()

            # 露西e1 重击 之后等待时间普攻 done
            # wait_light = 1.2  # done
            # print("____________________wait_light", wait_light)
            # lucy.lucy_e1_heavy2(wait_light)
            # lucy.lucy_cast_e_p1()  # done

            # time_d = 0.68#+0.05*i
            # lucy.test_lucy_p2_light4_and_heavy2_and_e_and_light4(time_d) #2.2ok
            # print("露西进入阶段2 普攻后重击 等待重击出伤 后马上大招 等待时间",time_d)
            # time_here = time.time()
            # while time.time() -time_here <10:
            #     lucy.lucy_p2_light_att(end_index=4)
            # break
            # 露西进入阶段2 普攻后重击 之后普攻需要等待时间 #done

            # lucy.lucy_cast_e_p2(0.0)#ok 0.0可以4段普攻
            # lucy.lucy_p2_light_att(end_index=4)
            # break
            # 露西进入阶段2 测试进入后普攻 间隔 #done

            # lucy.lucy_p2_light_att(end_index=5,test_index=i,test_learning_rate=0)
            # lucy.lucy_p2_light_att(end_index=4)
            # 测试露西阶段2 普攻  #done

            # lucy.test_light2_and_heavy(index=i,test_learning_rate=0)
            # lucy.test_light_all(end=5,index=i,test_learning_rate=-0.00)
            # lucy.lucy_p1_light3_heavy2(index=i,test_learning_rate=0.00)
            # lucy.test_light1_3_heavy2_light1_4(index=i)
            # lucy.test_light1_4_and_light1_4_wait_time(index=0)
            # lucy.test_random_light_att(index=i)
            # #测试地面切换守岸人后普攻直到攒满重击能量
            # send_key("3", hwnd_id=hwnd_id)
            # time.sleep(1.1)
            # send_key("1", hwnd_id=hwnd_id)
            #
            # time_sleep_after_switch_in = 0.4-0.05*i
            # if time_sleep_after_switch_in <= 0:
            #     time_sleep_after_switch_in = 0
            # time.sleep(time_sleep_after_switch_in)
            # print("time_sleep_after_switch_in",time_sleep_after_switch_in)
            # shore_keeper_in_auto_att(hwnd_id,i)
            # time.sleep(0.05)
            # w1, w2, w3 = shore_keeper_heavy_att(hwnd_id)
            # time.sleep(0.5)
            # send_key("SHIFT", hwnd_id=hwnd_id)
            # continuous_press_some_key("w", 1, hwnd_id)
            #
            # # 测试空中切换守岸人后普攻直到攒满重击能量
            # send_key("3", hwnd_id=hwnd_id)
            # time.sleep(1.1)
            # send_key("SPACE", hwnd_id=hwnd_id)
            # time.sleep(0.23)
            # send_key("1", hwnd_id=hwnd_id)
            #
            # time_sleep_after_switch_in = 0.85
            # if time_sleep_after_switch_in <= 0:
            #     time_sleep_after_switch_in = 0
            # time.sleep(time_sleep_after_switch_in)
            # print("time_sleep_after_switch_in", time_sleep_after_switch_in)
            # shore_keeper_in_auto_att(hwnd_id, i)
            # time.sleep(0.05)
            # w1, w2, w3 = shore_keeper_heavy_att(hwnd_id)
            # time.sleep(0.5)
            # send_key("SHIFT", hwnd_id=hwnd_id)
            # continuous_press_some_key("w", 1, hwnd_id)

            # continuous_att(0.9, hwnd_id)
            # heavy_att(0.5, hwnd_id=hwnd_id)

            # next_normal_move_must_sleep_time = lucy_e_att_p2(hwnd_id)
            # next_normal_move_must_sleep_time = lucy_double_e(hwnd_id)
            # next_normal_move_must_sleep_time,ult_need_wait = lucy_double_heavy_p2(hwnd_id)
            # time.sleep(ult_need_wait)
            # next_normal_move_must_sleep_time = lucy_ult(hwnd_id)
            # shore_keeper_e(hwnd_id,auto_att=True,test_index=i)
            # shore_keeper_normal_att_5(hwnd_id)
            # build_shore_keeper_forte(hwnd_id)
            # shore_keeper_heavy_att(hwnd_id,test_index=i)
            # after_heavy_sleep_time = 1.2-0.02*i
            # time.sleep(after_heavy_sleep_time)
            # print("after_heavy_sleep_time",after_heavy_sleep_time)
            # shore_keeper_normal_att_5(hwnd_id)
            # l1,l2,l3 = shore_keeper_normal_att_5(hwnd_id)
            # after_normal_sleep_time_heavy = 0
            # if after_normal_sleep_time_heavy <0:
            #     after_normal_sleep_time_heavy = 0
            # time.sleep(after_normal_sleep_time_heavy)
            # print("after_heavy_sleep_time", after_normal_sleep_time_heavy)
            # l1,l2,l3 =shore_keeper_heavy_att(hwnd_id)
            # loop_sleep = l1
            # build_up_ult(hwnd_id)
            # 测试大招后放e然后重复构建大招
            # w1,w2,w3 =shore_keep_use_ult(hwnd_id)
            # time_sleep = w2
            # time.sleep(time_sleep)
            # print("sleep time",str(time_sleep))
            # w1,w2,w3 = shore_keeper_e(hwnd_id, auto_att=False)
            # time.sleep(w1)
            # print("over all over")
            # build_up_ult(hwnd_id)
            # #测试e后普工重击
            # w1, w2, w3 = shore_keeper_e(hwnd_id, auto_att=False)
            # time.sleep(w1)
            # shore_keeper_normal_att_after_e(hwnd_id,i)
            # time.sleep(0.05)
            # w1, w2, w3 = shore_keeper_heavy_att(hwnd_id)
            # time.sleep(w1)
            # continuous_press_some_key("w", 1, hwnd_id)
            # lucy_light_att_p2_with_heavy(hwnd_id=hwnd_id)
            # time.sleep(next_normal_move_must_sleep_time)
            print("loop over all over", (i + 1), "/", loop_time)
            time.sleep(loop_sleep)
            # if i == 5 :
            #     send_key("2", hwnd_id=hwnd_id)
    finally:
        lucy.my_input_sim.send_key("1")

# def list_window_names():
#     def winEnumHandler(hwnd_id, ctx):
#         if win32gui.IsWindowVisible(hwnd_id):
#             print(hex(hwnd_id), '"' + win32gui.GetWindowText(hwnd_id) + '"')
#             list_inner_windows(hwnd_id)
#
#     win32gui.EnumWindows(winEnumHandler, None)
#     print("------------over------------------")
#
#
# def list_inner_windows(whndl):
#     def callback(hwnd_id, hwnds):
#         if win32gui.IsWindowVisible(hwnd_id) and win32gui.IsWindowEnabled(hwnd_id):
#             hwnds[win32gui.GetClassName(hwnd_id)] = hwnd_id
#             return True
#
#     hwnds = {}
#     win32gui.EnumChildWindows(whndl, callback, hwnds)
#     if hwnds:
#         print(str(whndl), "child", hwnds)
#
#     print("------------over------------------")
#     return hwnds

if __name__ == '__main__':
    main()