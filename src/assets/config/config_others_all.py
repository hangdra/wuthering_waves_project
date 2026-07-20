# @Author  : liuha
# @Time    : 2026/7/18 21:43
# @File    : config_others_all.py


white_color = {  # 用于检测UI元素可用状态的白色颜色范围。
    'r': (253, 255),  # Red range
    'g': (253, 255),  # Green range
    'b': (253, 255)  # Blue range
}

con_colors = {  # 不同角色属性的协奏值能量环的颜色范围列表。
    "spectro": {
        'r': (205, 235),
        'g': (190, 222),  # for yellow spectro
        'b': (90, 130)
    },
    "electric": {
        'r': (150, 190),  # Red range
        'g': (95, 140),  # Green range for purple electric
        'b': (210, 249)  # Blue range
    },
    "fire": {
        'r': (200, 230),  # Red range
        'g': (100, 130),  # Green range    for red fire
        'b': (75, 105)  # Blue range
    },
    "ice": {
        'r': (60, 95),  # Red range
        'g': (150, 180),  # Green range    for blue ice
        'b': (210, 245)  # Blue range
    },
    "wind": {
        'r': (70, 110),  # Red range
        'g': (215, 250),  # Green range    for green wind
        'b': (155, 190)  # Blue range
    },
    "havoc": {
        'r': (190, 220),  # Red range
        'g': (65, 105),  # Green range    for havoc
        'b': (145, 175)  # Blue range
    }
}

con_colors_hsv = {  # 不同角色属性的协奏值能量环的颜色范围列表。
    "spectro": {
        'h': (23, 32),
        's': (52, 255),
        'v': (0, 255)
    },
    "electric": {
        'h': (133, 146),
        's': (85, 153),
        'v': (130, 255)
    },
    "fire": {
        'h': (5, 12),
        's': (68, 179),
        'v': (175, 255)
    },
    "ice": {
        'h': (90, 104),
        's': (52, 193),
        'v': (165, 255)
    },
    "wind": {
        'h': (73, 82),
        's': (125, 255),
        'v': (151, 255)
    },
    "havoc": {
        'h': (161, 170),
        's': (130, 231),
        'v': (78, 255)
    }
}


con_info = {
    "tem_window_w": 1600,
    "tem_window_h": 900,
    "tem_target_x": 600,
    "tem_target_y": 813,
    "tem_w": 45,
    "tem_h": 45,
    "position_group":"center_bottom",
}
