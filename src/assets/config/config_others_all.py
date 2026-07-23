# @Author  : liuha
# @Time    : 2026/7/18 21:43
# @File    : config_others_all.py

init_set = {"lazy_init": False, "img_show": False}

white_color = {  # 用于检测UI元素可用状态的白色颜色范围。
    'r': (253, 255),  # Red range
    'g': (253, 255),  # Green range
    'b': (253, 255)  # Blue range
}

mask_colors = {  # 不同角色属性的协奏值能量环的颜色范围列表。
    # "spectro": {
    #     'h': (23, 32),
    #     's': (52, 255),
    #     'v': (0, 255)
    # },
    "spectro": {
        'h': (26, 29),
        's': (0, 255),#fixed
        'v': (135, 255)
    },
    "electric": {
        'h': (124, 146),
        's': (13, 255),#fixed
        'v': (0, 255)
    },
    "fire": {
        'h': (7, 10),
        's': (142, 172),#fixed
        'v': (211, 255)
    },
    "ice": {
        'h': (100, 104),
        's': (0, 255),#fixed
        'v': (0, 255)
    },
    "wind": {
        'h': (73, 82),
        's': (125, 255),
        'v': (0, 255)
    },
    "havoc": {
        'h': (161, 170),
        's': (130, 231),
        'v': (78, 255)
    },
    "lock_on":{
        'h': (0, 32),
        's': (0, 255),
        'v': (132, 255)
    },
    "lock_off":{
        # 'h': (29, 30),
        'h': (0, 95),
        's': (0, 6),
        'v': (0, 255)
    },
    "char_active":{
        'h': (119, 120),
        's': (0, 36),
        'v': (88, 201)
    }
}

con_info = {
    "tem_window_w": 1600,
    "tem_window_h": 900,
    "tem_target_x": 600,
    "tem_target_y": 813,
    "tem_w": 45,
    "tem_h": 45,
    "position_group": "center_bottom",
}
