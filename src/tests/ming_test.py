import json
import re

# 将您提供的表格文本按行分割（这里省略，实际可从文件读取）
lines = """
Virtual-Key 代码
下表显示了系统使用的虚拟键代码的符号常量名称、十六进制值和鼠标或键盘等效项。 这些代码按数字顺序列出。

不断	价值	描述
VK_LBUTTON	0x01	鼠标左键
VK_RBUTTON	0x02	鼠标右键
VK_CANCEL	0x03	控制中断处理
VK_MBUTTON	0x04	鼠标中间按钮
VK_XBUTTON1	0x05	X1 鼠标按钮
VK_XBUTTON2	0x06	X2 鼠标按钮
0x07	保留
VK_BACK	0x08	Backspace 键
VK_TAB	0x09	Tab 键
0x0A-0B	保留
VK_CLEAR	0x0C	清除键
VK_RETURN	0x0D	输入键
0x0E-0F	未分配
VK_SHIFT	0x10	换档键
VK_CONTROL	0x11	Ctrl 键
VK_MENU	0x12	Alt 键
VK_PAUSE	0x13	暂停键
VK_CAPITAL	0x14	Caps lock 键
VK_KANA	0x15	IME 假名模式
VK_HANGUL	0x15	IME 朝鲜文模式
VK_IME_ON	0x16	IME On
VK_JUNJA	0x17	IME Junja 模式
VK_FINAL	0x18	IME 最终模式
VK_HANJA	0x19	IME Hanja 模式
VK_KANJI	0x19	IME 汉字模式
VK_IME_OFF	0x1A	IME 关闭
VK_ESCAPE	0x1B	Esc 键
VK_CONVERT	0x1C	IME 转换
VK_NONCONVERT	0x1D	IME 非转换
VK_ACCEPT	0x1E	IME 接受
VK_MODECHANGE	0x1F	IME 模式更改请求
VK_SPACE	0x20	空格键
VK_PRIOR	0x21	Page up 键
VK_NEXT	0x22	Page down 键
VK_END	0x23	结束键
VK_HOME	0x24	主键
VK_LEFT	0x25	向左键
VK_UP	0x26	向上键
VK_RIGHT	0x27	向右键
VK_DOWN	0x28	向下键
VK_SELECT	0x29	选择密钥
VK_PRINT	0x2A	打印键
VK_EXECUTE	0x2B	执行键
VK_SNAPSHOT	0x2C	打印屏幕键
VK_INSERT	0x2D	插入键
VK_DELETE	0x2E	删除密钥
VK_HELP	0x2F	帮助密钥
0	0x30	0 键
1	0x31	1 个键
2	0x32	2 键
3	0x33	3 个键
4	0x34	4 键
5	0x35	5 个键
6	0x36	6 个键
7	0x37	7 键
8	0x38	8 键
9	0x39	9 键
0x3A-40	定义
A	0x41	密钥
B	0x42	B 键
C	0x43	C 键
D	0x44	D 键
E	0x45	E 键
F	0x46	F 键
G	0x47	G 键
H	0x48	H 键
I	0x49	I 键
J	0x4A	J 键
K	0x4B	K 键
L	0x4C	L 键
M	0x4D	M 键
N	0x4E	N 键
O	0x4F	O 键
P	0x50	P 键
Q	0x51	Q 键
R	0x52	R 键
S	0x53	S 键
T	0x54	T 键
U	0x55	U 键
V	0x56	V 键
W	0x57	W 键
X	0x58	X 键
Y	0x59	Y 键
Z	0x5A	Z 键
VK_LWIN	0x5B	左 Windows 徽标键
VK_RWIN	0x5C	右 Windows 徽标键
VK_APPS	0x5D	应用程序密钥
0x5E	保留
VK_SLEEP	0x5F	计算机睡眠键
VK_NUMPAD0	0x60	数字键盘 0 键
VK_NUMPAD1	0x61	数字键盘 1 键
VK_NUMPAD2	0x62	数字键盘 2 键
VK_NUMPAD3	0x63	数字键盘 3 键
VK_NUMPAD4	0x64	数字键盘 4 键
VK_NUMPAD5	0x65	数字键盘 5 键
VK_NUMPAD6	0x66	数字键盘 6 键
VK_NUMPAD7	0x67	数字键盘 7 键
VK_NUMPAD8	0x68	数字键盘 8 键
VK_NUMPAD9	0x69	数字键盘 9 键
VK_MULTIPLY	0x6A	相乘键
VK_ADD	0x6B	添加密钥
VK_SEPARATOR	0x6C	分隔符键
VK_SUBTRACT	0x6D	减去键
VK_DECIMAL	0x6E	十进制键
VK_DIVIDE	0x6F	除键
VK_F1	0x70	F1 键
VK_F2	0x71	F2 键
VK_F3	0x72	F3 键
VK_F4	0x73	F4 键
VK_F5	0x74	F5 键
VK_F6	0x75	F6 键
VK_F7	0x76	F7 键
VK_F8	0x77	F8 键
VK_F9	0x78	F9 键
VK_F10	0x79	F10 键
VK_F11	0x7A	F11 键
VK_F12	0x7B	F12 键
VK_F13	0x7C	F13 键
VK_F14	0x7D	F14 键
VK_F15	0x7E	F15 键
VK_F16	0x7F	F16 键
VK_F17	0x80	F17 键
VK_F18	0x81	F18 键
VK_F19	0x82	F19 键
VK_F20	0x83	F20 键
VK_F21	0x84	F21 键
VK_F22	0x85	F22 键
VK_F23	0x86	F23 键
VK_F24	0x87	F24 键
0x88-8F	保留
VK_NUMLOCK	0x90	Num lock 键
VK_SCROLL	0x91	滚动锁键
0x92-96	OEM 特定
0x97-9F	未分配
VK_LSHIFT	0xA0	左移键
VK_RSHIFT	0xA1	右移键
VK_LCONTROL	0xA2	左 Ctrl 键
VK_RCONTROL	0xA3	右 Ctrl 键
VK_LMENU	0xA4	左 Alt 键
VK_RMENU	0xA5	右 Alt 键
VK_BROWSER_BACK	0xA6	浏览器后退键
VK_BROWSER_FORWARD	0xA7	浏览器转发密钥
VK_BROWSER_REFRESH	0xA8	浏览器刷新密钥
VK_BROWSER_STOP	0xA9	浏览器停止键
VK_BROWSER_SEARCH	0xAA	浏览器搜索键
VK_BROWSER_FAVORITES	0xAB	浏览器收藏夹密钥
VK_BROWSER_HOME	0xAC	浏览器“开始”和“开始”键
VK_VOLUME_MUTE	0xAD	音量静音键
VK_VOLUME_DOWN	0xAE	调低音量键
VK_VOLUME_UP	0xAF	调高音量键
VK_MEDIA_NEXT_TRACK	0xB0	下一个 Track 键
VK_MEDIA_PREV_TRACK	0xB1	上一曲目键
VK_MEDIA_STOP	0xB2	停止媒体键
VK_MEDIA_PLAY_PAUSE	0xB3	播放/暂停媒体键
VK_LAUNCH_MAIL	0xB4	启动邮件密钥
VK_LAUNCH_MEDIA_SELECT	0xB5	选择媒体键
VK_LAUNCH_APP1	0xB6	启动应用程序 1 密钥
VK_LAUNCH_APP2	0xB7	启动应用程序 2 密钥
0xB8-B9	保留
VK_OEM_1	0xBA	它可能因键盘而异。 对于 US ANSI 键盘，使用 Semiсolon 和冒号键
VK_OEM_PLUS	0xBB	对于任何国家/地区，“等于”和“加号”键
VK_OEM_COMMA	0xBC	对于任何国家/地区，逗号和小于键
VK_OEM_MINUS	0xBD	对于任何国家/地区，短划线和下划线键
VK_OEM_PERIOD	0xBE	对于任何国家/地区，“时间段”和“大于”键
VK_OEM_2	0xBF	它可能因键盘而异。 对于 US ANSI 键盘，“正斜杠”和“问号”键
VK_OEM_3	0xC0	它可能因键盘而异。 对于 US ANSI 键盘，“严重重音”和“波形符”键
0xC1-C2	保留
VK_GAMEPAD_A	0xC3	游戏板 A 按钮
VK_GAMEPAD_B	0xC4	游戏板 B 按钮
VK_GAMEPAD_X	0xC5	游戏板 X 按钮
VK_GAMEPAD_Y	0xC6	游戏板 Y 按钮
VK_GAMEPAD_RIGHT_SHOULDER	0xC7	游戏板右肩按钮
VK_GAMEPAD_LEFT_SHOULDER	0xC8	游戏板左肩按钮
VK_GAMEPAD_LEFT_TRIGGER	0xC9	游戏板左侧触发器按钮
VK_GAMEPAD_RIGHT_TRIGGER	0xCA	游戏板右触发器按钮
VK_GAMEPAD_DPAD_UP	0xCB	游戏板 D-pad 向上按钮
VK_GAMEPAD_DPAD_DOWN	0xCC	游戏板 D 板向下按钮
VK_GAMEPAD_DPAD_LEFT	0xCD	游戏板 D 键向左按钮
VK_GAMEPAD_DPAD_RIGHT	0xCE	游戏板 D 板向右按钮
VK_GAMEPAD_MENU	0xCF	游戏板菜单/“开始”按钮
VK_GAMEPAD_VIEW	0xD0	游戏板视图/后退按钮
VK_GAMEPAD_LEFT_THUMBSTICK_BUTTON	0xD1	游戏板左摇杆按钮
VK_GAMEPAD_RIGHT_THUMBSTICK_BUTTON	0xD2	游戏板右纵杆按钮
VK_GAMEPAD_LEFT_THUMBSTICK_UP	0xD3	游戏板左摇杆向上
VK_GAMEPAD_LEFT_THUMBSTICK_DOWN	0xD4	游戏板左摇杆向下键
VK_GAMEPAD_LEFT_THUMBSTICK_RIGHT	0xD5	游戏板左纵杆向右
VK_GAMEPAD_LEFT_THUMBSTICK_LEFT	0xD6	游戏板左摇杆左
VK_GAMEPAD_RIGHT_THUMBSTICK_UP	0xD7	游戏板右纵杆向上
VK_GAMEPAD_RIGHT_THUMBSTICK_DOWN	0xD8	游戏板右纵杆向下键
VK_GAMEPAD_RIGHT_THUMBSTICK_RIGHT	0xD9	游戏板右纵杆向右
VK_GAMEPAD_RIGHT_THUMBSTICK_LEFT	0xDA	游戏板向左摇杆
VK_OEM_4	0xDB	它可能因键盘而异。 对于 US ANSI 键盘，左大括号键
VK_OEM_5	0xDC	它可能因键盘而异。 对于 US ANSI 键盘，反斜杠和管道键
VK_OEM_6	0xDD	它可能因键盘而异。 对于 US ANSI 键盘，右大括号键
VK_OEM_7	0xDE	它可能因键盘而异。 对于 US ANSI 键盘，“撇号”和“双引号”键
VK_OEM_8	0xDF	它可能因键盘而异。 对于加拿大 CSA 键盘，为右 Ctrl 键
0xE0	保留
0xE1	OEM 特定
VK_OEM_102	0xE2	它可能因键盘而异。 对于欧洲 ISO 键盘，反斜杠和管道键
0xE3-E4	OEM 特定
VK_PROCESSKEY	0xE5	IME PROCESS 密钥
0xE6	OEM 特定
VK_PACKET	0xE7	用于传递 Unicode 字符，就像是击键一样。 VK_PACKET 键是用于非键盘输入方法的 32 位虚拟键值的低字。 有关详细信息，请参阅 KEYBDINPUT、SendInput、WM_KEYDOWN和 WM_KEYUP 中的备注
0xE8	未分配
0xE9-F5	OEM 特定
VK_ATTN	0xF6	Attn 键
VK_CRSEL	0xF7	CrSel 键
VK_EXSEL	0xF8	ExSel 密钥
VK_EREOF	0xF9	擦除 EOF 密钥
VK_PLAY	0xFA	播放键
VK_ZOOM	0xFB	缩放键
VK_NONAME	0xFC	保留
VK_PA1	0xFD	PA1 密钥
VK_OEM_CLEAR	0xFE	清除键
""".strip().split('\n')

data = []
for line in lines:
    parts = re.split(r'\t+', line)
    if len(parts) >= 3:
        const, val, desc = parts[0], parts[1], ' '.join(parts[2:])
        # 处理空常量名（如保留行）
        if not const.strip():
            const = "Reserved" if "保留" in desc else "Unassigned"
        data.append({
            "constant": const,
            "value": val,
            "description": desc
        })

with open('../assets/config/virtual_keys.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)