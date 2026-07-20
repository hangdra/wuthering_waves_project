from src.core.input.input_sim import InputUtils
from src.utils.get_game_window_id import GetGameWindowId
from src.utils.load_all_template import my_LoadAllTemplate_instance
from src.core.vision.wgc import ZBLWindowGrabber

class OverAllProgram:

    def __init__(self):
        self.my_template = my_LoadAllTemplate_instance.template_info_list
        self.window_name = "鸣潮"
        self.game_window_instance = GetGameWindowId(window_name=self.window_name)
        self.input_instance = InputUtils(self.game_window_instance)
        self.window_capture = ZBLWindowGrabber(self.game_window_instance)


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
